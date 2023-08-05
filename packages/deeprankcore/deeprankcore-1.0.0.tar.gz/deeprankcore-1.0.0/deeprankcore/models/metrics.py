import lzma
import os
import csv
from typing import List, Tuple, Any, Dict, Optional
from math import sqrt
import logging
import random
from matplotlib import pyplot
from torch import argmax, tensor
from torch.nn.functional import cross_entropy
from torch.utils.tensorboard import SummaryWriter
from sklearn.metrics import roc_auc_score
import pandas as pd

_log = logging.getLogger(__name__)


class MetricsExporter:
    "The class implements an object, to be called when a neural network generates output"

    def __enter__(self):
        "overridable"
        return self

    def __exit__(self, exception_type, exception, traceback):
        "overridable"
        pass # pylint: disable=unnecessary-pass

    def process(self, pass_name: str, epoch_number: int, # pylint: disable=too-many-arguments
                entry_names: List[str], output_values: List[Any], target_values: List[Any]):
        "the entry_names, output_values, target_values MUST have the same length"
        pass # pylint: disable=unnecessary-pass

    def is_compatible_with(self, output_data_shape: int, target_data_shape: Optional[int]) -> bool:  # pylint: disable=unused-argument
        "true if this exporter can work with the given data shapes"

        return True


class MetricsExporterCollection:
    "allows a series of metrics exporters to be used at the same time"

    def __init__(self, *args: Tuple[MetricsExporter]):
        self._metrics_exporters = args

    def __enter__(self):
        for metrics_exporter in self._metrics_exporters:
            metrics_exporter.__enter__()

        return self

    def __exit__(self, exception_type, exception, traceback):
        for metrics_exporter in self._metrics_exporters:
            metrics_exporter.__exit__(exception_type, exception, traceback)

    def process(self, pass_name: str, epoch_number: int, # pylint: disable=too-many-arguments
                entry_names: List[str], output_values: List[Any], target_values: List[Any]):
        for metrics_exporter in self._metrics_exporters:
            metrics_exporter.process(pass_name, epoch_number, entry_names, output_values, target_values)

    def __iter__(self):
        return iter(self._metrics_exporters)


class TensorboardBinaryClassificationExporter(MetricsExporter):
    """ Exports to tensorboard, works for binary classification only.

        Currently outputs to tensorboard:
         - Mathews Correlation Coefficient (MCC)
         - Accuracy
         - ROC area under the curve

        Outputs are done per epoch.
    """

    def __init__(self, directory_path: str):
        self._directory_path = directory_path
        self._writer = SummaryWriter(log_dir=directory_path)

    def __enter__(self):
        self._writer.__enter__()
        return self

    def __exit__(self, exception_type, exception, traceback):
        self._writer.__exit__(exception_type, exception, traceback)

    def process(self, pass_name: str, epoch_number: int, # pylint: disable=too-many-arguments, too-many-locals
                entry_names: List[str], output_values: List[Any], target_values: List[Any]):
        "write to tensorboard"

        loss = cross_entropy(tensor(output_values), tensor(target_values)).item()
        self._writer.add_scalar(f"{pass_name} cross entropy loss", loss, epoch_number)

        probabilities = []
        fp, fn, tp, tn = 0, 0, 0, 0
        for entry_index, _ in enumerate(entry_names):
            probability = output_values[entry_index][1]
            probabilities.append(probability)

            prediction_value = argmax(tensor(output_values[entry_index]))
            target_value = target_values[entry_index]

            if prediction_value > 0.0 and target_value > 0.0:
                tp += 1

            elif prediction_value <= 0.0 and target_value <= 0.0:
                tn += 1

            elif prediction_value > 0.0 and target_value <= 0.0: # pylint: disable=chained-comparison
                fp += 1

            elif prediction_value <= 0.0 and target_value > 0.0: # pylint: disable=chained-comparison
                fn += 1

        mcc_numerator = tn * tp - fp * fn
        if mcc_numerator == 0.0:
            self._writer.add_scalar(f"{pass_name} MCC", 0.0, epoch_number)
        else:
            mcc_denominator = sqrt((tn + fn) * (fp + tp) * (tn + fp) * (fn + tp))

            if mcc_denominator != 0.0:
                mcc = mcc_numerator / mcc_denominator
                self._writer.add_scalar(f"{pass_name} MCC", mcc, epoch_number)

        accuracy = (tp + tn) / (tp + tn + fp + fn)
        self._writer.add_scalar(f"{pass_name} accuracy", accuracy, epoch_number)

        # for ROC curves to work, we need both class values in the set
        if len(set(target_values)) == 2:
            roc_auc = roc_auc_score(target_values, probabilities)
            self._writer.add_scalar(f"{pass_name} ROC AUC", roc_auc, epoch_number)

    def is_compatible_with(self, output_data_shape: int, target_data_shape: Optional[int]) -> bool:
        "for regression, target data is needed and output data must be a list of two-dimensional values"

        return output_data_shape == 2 and target_data_shape == 1


class OutputExporter(MetricsExporter):
    """ A metrics exporter that writes CSV output tables, containing every single data point.

        Included are:
            - entry names
            - output values
            - target values

        The user can load these output tables in excel.

        Outputs are done per epoch.
    """

    def __init__(self, directory_path: str):
        self._directory_path = directory_path

    def get_filename(self, pass_name, epoch_number):
        "returns the filename for the table"
        return os.path.join(self._directory_path, f"output-{pass_name}-epoch-{epoch_number}.csv.xz")

    def process(self, pass_name: str, epoch_number: int, # pylint: disable=too-many-arguments
                entry_names: List[str], output_values: List[Any], target_values: List[Any]):
        "write the output to the table"

        with lzma.open(self.get_filename(pass_name, epoch_number), 'wt', newline='\n') as f:
            w = csv.writer(f, delimiter=',')

            w.writerow(["entry", "output", "target"])

            for entry_index, entry_name in enumerate(entry_names):
                output_value = output_values[entry_index]
                target_value = target_values[entry_index]

                _log.debug(f"writerow [{entry_name}, {output_value}, {target_value}]") # pylint: disable=logging-fstring-interpolation

                w.writerow([entry_name, str(output_value), str(target_value)])


class ScatterPlotExporter(MetricsExporter):
    """ A metrics exporter that ocasionally makes scatter plots, containing every single data point.

        On the X-axis: targets values
        On the Y-axis: output values
    """

    def __init__(self, directory_path: str, epoch_interval: int = 1):
        """ Args:
                directory_path: where to store the plots
                epoch_interval: how often to make a plot, 5 means: every 5 epochs
        """

        self._epoch_interval = epoch_interval
        self._directory_path = directory_path

    def __enter__(self):
        self._plot_data = {}
        return self

    def __exit__(self, exception_type, exception, traceback):
        self._plot_data.clear()

    def get_filename(self, epoch_number):
        "returns the filename for the table"
        return os.path.join(self._directory_path, f"scatter-{epoch_number}.png")

    @staticmethod
    def _get_color(pass_name):

        pass_name = pass_name.lower().strip()

        if pass_name in ("train", "training"):
            return "blue"

        if pass_name in ("eval", "valid", "validation"):
            return "red"

        if pass_name == ("test", "testing"):
            return "green"

        return random.choice(["yellow", "cyan", "magenta"])


    @staticmethod
    def _plot(epoch_number: int, data: Dict[str, Tuple[List[float], List[float]]], png_path: str):

        pyplot.title(f"Epoch {epoch_number}")

        for pass_name, (truth_values, prediction_values) in data.items():
            pyplot.scatter(truth_values, prediction_values, color=ScatterPlotExporter._get_color(pass_name), label=pass_name)

        pyplot.xlabel("truth")
        pyplot.ylabel("prediction")

        pyplot.legend()
        pyplot.savefig(png_path)
        pyplot.close()

    def process(self, pass_name: str, epoch_number: int, # pylint: disable=too-many-arguments
                entry_names: List[str], output_values: List[Any], target_values: List[Any]):
        "make the plot, if the epoch matches with the interval"

        if epoch_number % self._epoch_interval == 0:

            if epoch_number not in self._plot_data:
                self._plot_data[epoch_number] = {}

            self._plot_data[epoch_number][pass_name] = (target_values, output_values)

            path = self.get_filename(epoch_number)
            self._plot(epoch_number, self._plot_data[epoch_number], path)

    def is_compatible_with(self, output_data_shape: int, target_data_shape: Optional[int]) -> bool:
        "for regression, target data is needed and output data must be a list of one-dimensional values"

        return output_data_shape == 1 and target_data_shape == 1

class ConciseOutputExporter(MetricsExporter):
    # tbd: if either we want to uniform it with MetricsExporter interface, or if we want to delete the other exporters
    """ A metrics exporter that writes a CSV output table, containing every single data point.

        Included are:
            - phase (train/valid/test)
            - epoch
            - entry names
            - output values
            - target values
            - loss per epoch

        The user can then load the csv table into a Pandas df, and plotting metrics
    """

    def __init__(
        self,
        directory_path: str):

        self._directory_path = directory_path
        d = {'phase': [], 'epoch': [], 'entry': [], 'output': [], 'target': [], 'loss': []}
        self.df = pd.DataFrame(data=d)

    def epoch_process( # pylint: disable=too-many-arguments
        self,
        pass_name: str,
        epoch_number: int, 
        entry_names: List[str],
        output_values: List[Any],
        target_values: List[Any],
        loss: float):

        pass_name = [pass_name] * len(output_values)
        loss = [loss] * len(output_values)
        epoch_number = [epoch_number] * len(output_values)

        d_epoch = {'phase': pass_name, 'epoch': epoch_number, 'entry': entry_names, 'output': output_values, 'target': target_values, 'loss': loss}
        df_epoch = pd.DataFrame(data=d_epoch)

        self.df = pd.concat([self.df, df_epoch])

    def save_all_metrics(self):

        self.df.to_hdf(
            os.path.join(self._directory_path, 'metrics.hdf5'),
            key='metrics',
            mode='w')

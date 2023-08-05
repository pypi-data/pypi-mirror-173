from dataclasses import asdict

from torch.utils.data import DataLoader

from QGCN.params import GraphsDataParams, ExternalParams, ModelParams, ActivatorParams
from QGCN.dataset.dataset_graphs_model import GraphsDataset
from QGCN.dataset.dataset_external_data import ExternalData
from QGCN.QGCN_model.qgcn_activator import QGCNActivator
from QGCN.QGCN_model.QGCN import QGCN


class QGCNDataSet:
    def __init__(self, dataset_name: str,
                 graph_data_params: GraphsDataParams,
                 external_params: ExternalParams):

        self.params = {
            "dataset_name": dataset_name,
            "external": asdict(external_params),
            "graphs_data": asdict(graph_data_params)
        }

        ext_train = ExternalData(self.params)
        self.dataset = GraphsDataset(self.params, external_data=ext_train)

    def get_dataset(self):
        return self.dataset


class QGCNModel:
    def __init__(self, dataset_name: str,
                 graph_data_params: GraphsDataParams,
                 external_params: ExternalParams,
                 model_params: ModelParams,
                 activator_params: ActivatorParams,
                 device="cpu"):

        self.params = {
            "dataset_name": dataset_name,
            "external": asdict(external_params),
            "graphs_data": asdict(graph_data_params),
            "model": asdict(model_params),
            "activator": asdict(activator_params)
        }

        self.ext_train = ExternalData(self.params)
        self.ds = GraphsDataset(self.params, external_data=self.ext_train)
        qgcn = QGCN(self.params, self.ds.len_features, self.ext_train.len_embed())
        self.activator = QGCNActivator(qgcn, self.params, self.ds, device=device)

    def get_dataset(self):
        return self.ds

    def train(self, should_print=True):
        self.activator.train(should_print=should_print)

    def predictl(self, dataloader: DataLoader):
        outputs = []
        model = self.activator.model
        model.eval()
        for _, (A, x0, embed) in enumerate(dataloader):
            outputs.append(model(A, x0, embed))

        return outputs

    def predict(self, A, x0, embed):
        model = self.activator.model
        model.eval()
        return model(A, x0, embed)

    def get_model(self):
        return self.activator.model

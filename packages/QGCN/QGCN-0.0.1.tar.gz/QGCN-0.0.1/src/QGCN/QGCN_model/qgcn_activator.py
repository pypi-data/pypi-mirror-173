import json
from sys import stdout
# import nni
from time import sleep
from dataclasses import asdict

# import pylab as pl
from bokeh.io import output_file

# f = open("curr_pwd", "wt")
# f.write(cwd)# cwd = os.getcwd()
# f.close()

# sys.path.insert(1, os.path.join(".."))
# sys.path.insert(1, os.path.join(cwd, "..", "..", "graph-measures"))
# sys.path.insert(1, os.path.join(cwd, "..", "..", "graph-measures", "features_algorithms"))
# sys.path.insert(1, os.path.join(cwd, "..", "..", "graph-measures", "graph_infra"))
# sys.path.insert(1, os.path.join(cwd, "..", "..", "graph-measures", "features_infra"))
# sys.path.insert(1, os.path.join(cwd, "..", "..", "graph-measures", "features_meta"))
# sys.path.insert(1, os.path.join(cwd, "..", "..", "graph-measures", "features_algorithms", "vertices"))

# sys.path.insert(1, os.path.join("..", "..", "graphs-package", "features_processor"))
# sys.path.insert(1, os.path.join("..", "..", "graphs-package", "multi_graph"))
# sys.path.insert(1, os.path.join("..", "..", "graphs-package", "temporal_graphs"))
# sys.path.insert(1, os.path.join("..", "..", "graphs-package", "features_processor", "motif_variations"))
# sys.path.insert(1, os.path.join("..", "..", "graphs-package"))


# this is instead of sign graphs_package as root source TODO
# sys.path.insert(1, os.path.join(os.path.dirname(sys.path[0]), "graphs_package"))
# sys.path.insert(1, os.path.dirname(sys.path[0]))


# sys.path.insert(1, os.path.join("..", "graphs-package", "multi_graph"))
# sys.path.insert(1, os.path.join("..", "graphs-package", "temporal_graphs"))
# sys.path.insert(1, os.path.join("..", "graphs-package", "features_processor", "motif_variations"))
# sys.path.insert(1, os.path.join("..", "graphs-package"))
# sys.path.insert(1, os.path.join(".."))
# sys.path[0] = "."
# sys.path[1] = "."

# sys.path.insert(1, os.path.join("..", "..", "dataset"))
# print(sys.path)

import torch
from sklearn.metrics import roc_auc_score
from bokeh.plotting import figure, show
from torch.nn.functional import binary_cross_entropy_with_logits, cross_entropy
from torch.utils.data import DataLoader, random_split
from collections import Counter
import numpy as np
from QGCN.QGCN_model.QGCN import QGCN
from QGCN.params import GraphsDataParams, ExternalParams, ModelParams, ActivatorParams
from QGCN.dataset.dataset_graphs_model import GraphsDataset
from QGCN.dataset.dataset_external_data import ExternalData

TRAIN_JOB = "TRAIN"
DEV_JOB = "DEV"
TEST_JOB = "TEST"
VALIDATE_JOB = "VALIDATE"
LOSS_PLOT = "loss"
AUC_PLOT = "AUC"
ACCURACY_PLOT = "accuracy"

binary_cross_entropy_with_logits_ = binary_cross_entropy_with_logits
cross_entropy_ = cross_entropy


def clip_grads(model, clip_c):
    """
    Apply gradient clipping as the writers did in the paper's implementation:
    If a gradient is larger than clip_c ** 2, divide it by the 2-norm of all gradients vector times clip_c
    """
    total_norm = 0
    for p in filter(lambda x: x.requires_grad, model.parameters()):
        total_norm += (p.grad.data ** 2).sum()
    total_norm = total_norm ** 0.5
    for p in filter(lambda x: x.requires_grad, model.parameters()):
        p.grad.data = torch.where(p.grad.data > clip_c ** 2, p.grad.data.mul(1 / (clip_c * total_norm)), p.grad.data)


class QGCNActivator:
    def __init__(self, model: QGCN, params, train_data: GraphsDataset, nni=False, device="cuda:0", grid=False):
        self._nni = nni
        self.grid = grid
        self._params = params if type(params) is dict else json.load(open(params, "rt"))
        self._dataset_name = self._params["dataset_name"]
        self._is_binary = True if self._params["model"]["label_type"] == "binary" else False
        self._params = self._params["activator"]

        self._gpu = torch.cuda.is_available()
        # self._gpu = True
        self._device = torch.device(device if self._gpu else "cpu")
        print(self._device)
        self._model = model.to(device=self._device)
        self._epochs = self._params["epochs"]
        self._batch_size = self._params["batch_size"]
        self._loss_func = globals()[self._params["loss_func"]]
        self._load_data(train_data, self._params["train"], self._params["dev"], self._params["test"], self._batch_size)
        self._init_loss_and_acc_vec()
        self._init_print_att()

    # init loss and accuracy vectors (as function of epochs)
    def _init_loss_and_acc_vec(self):
        self._loss_vec_train = []
        self._loss_vec_dev = []
        self._loss_vec_test = []

        self._bar = 0.5
        self._accuracy_vec_train = []
        self._accuracy_vec_dev = []
        self._accuracy_vec_test = []

        self._auc_vec_train = []
        self._auc_vec_dev = []
        self._auc_vec_test = []

    # init variables that holds the last update for loss and accuracy
    def _init_print_att(self):
        self._print_train_accuracy = 0
        self._print_train_loss = 0
        self._print_train_auc = 0

        self._print_dev_accuracy = 0
        self._print_dev_loss = 0
        self._print_dev_auc = 0

        self._print_test_accuracy = 0
        self._print_test_loss = 0
        self._print_test_auc = 0

    # update loss after validating
    def _update_loss(self, loss, job=TRAIN_JOB):
        if job == TRAIN_JOB:
            self._loss_vec_train.append(loss)
            self._print_train_loss = loss
        elif job == DEV_JOB:
            self._loss_vec_dev.append(loss)
            self._print_dev_loss = loss
        elif job == TEST_JOB:
            self._loss_vec_test.append(loss)
            self._print_test_loss = loss

    # update accuracy after validating
    def _update_auc(self, pred, true, job=TRAIN_JOB):
        pred_ = [-1 if np.isnan(x) else x for x in pred]
        num_classes = len(Counter(true))
        if num_classes < 2:
            auc = 0.5
        # calculate acc
        else:
            auc = roc_auc_score(true, pred_)
        if job == TRAIN_JOB:
            self._print_train_auc = auc
            self._auc_vec_train.append(auc)
            return auc
        elif job == DEV_JOB:
            self._print_dev_auc = auc
            self._auc_vec_dev.append(auc)
            return auc
        elif job == TEST_JOB:
            self._print_test_auc = auc
            self._auc_vec_test.append(auc)
            return auc

    # update accuracy after validating
    def _update_accuracy_binary(self, pred, true, job=TRAIN_JOB):
        # calculate acc
        if job == TRAIN_JOB:
            max_acc = 0
            best_bar = self._bar
            for bar in [i * 0.01 for i in range(100)]:
                acc = sum([1 if (0 if i < bar else 1) == int(j) else 0 for i, j in zip(pred, true)]) / len(pred)
                if acc > max_acc:
                    best_bar = bar
                    max_acc = acc
            self._bar = best_bar

            self._print_train_accuracy = max_acc
            self._accuracy_vec_train.append(max_acc)
            return max_acc

        acc = sum([1 if (0 if i < self._bar else 1) == int(j) else 0 for i, j in zip(pred, true)]) / len(pred)

        if job == DEV_JOB:
            self._print_dev_accuracy = acc
            self._accuracy_vec_dev.append(acc)
            return acc
        elif job == TEST_JOB:
            self._print_test_accuracy = acc
            self._accuracy_vec_test.append(acc)
            return acc

    def _update_accuracy_multiclass(self, pred, true, job=TRAIN_JOB):
        pred = np.asarray(pred).argmax(axis=1).tolist()
        # calculate acc
        acc = sum([1 if int(i) == int(j) else 0 for i, j in zip(pred, true)]) / len(pred)
        if job == TRAIN_JOB:
            self._print_train_accuracy = acc
            self._accuracy_vec_train.append(acc)
            return acc
        elif job == DEV_JOB:
            self._print_dev_accuracy = acc
            self._accuracy_vec_dev.append(acc)
            return acc
        elif job == TEST_JOB:
            self._print_test_accuracy = acc
            self._accuracy_vec_test.append(acc)
            return acc

    # print progress of a single epoch as a percentage
    def _print_progress(self, batch_index, len_data, job=""):
        prog = int(100 * (batch_index + 1) / len_data)
        stdout.write("\r\r\r\r\r\r\r\r" + job + " %d" % prog + "%")
        print("", end="\n" if prog == 100 else "")
        stdout.flush()

    # print last loss and accuracy
    def _print_info(self, jobs=()):
        if self._is_binary:
            if TRAIN_JOB in jobs:
                print("Acc_Train: " + '{:{width}.{prec}f}'.format(self._print_train_accuracy, width=6, prec=4) +
                      " || AUC_Train: " + '{:{width}.{prec}f}'.format(self._print_train_auc, width=6, prec=4) +
                      " || Loss_Train: " + '{:{width}.{prec}f}'.format(self._print_train_loss, width=6, prec=4),
                      end=" || ")
            if DEV_JOB in jobs:
                print("Acc_Dev: " + '{:{width}.{prec}f}'.format(self._print_dev_accuracy, width=6, prec=4) +
                      " || AUC_Dev: " + '{:{width}.{prec}f}'.format(self._print_dev_auc, width=6, prec=4) +
                      " || Loss_Dev: " + '{:{width}.{prec}f}'.format(self._print_dev_loss, width=6, prec=4),
                      end=" || ")
            if TEST_JOB in jobs:
                print("Acc_Test: " + '{:{width}.{prec}f}'.format(self._print_test_accuracy, width=6, prec=4) +
                      " || AUC_Test: " + '{:{width}.{prec}f}'.format(self._print_test_auc, width=6, prec=4) +
                      " || Loss_Test: " + '{:{width}.{prec}f}'.format(self._print_test_loss, width=6, prec=4),
                      end=" || ")
            print("")
        else:
            if TRAIN_JOB in jobs:
                print("Acc_Train: " + '{:{width}.{prec}f}'.format(self._print_train_accuracy, width=6, prec=4) +
                      " || Loss_Train: " + '{:{width}.{prec}f}'.format(self._print_train_loss, width=6, prec=4),
                      end=" || ")
            if DEV_JOB in jobs:
                print("Acc_Dev: " + '{:{width}.{prec}f}'.format(self._print_dev_accuracy, width=6, prec=4) +
                      " || Loss_Dev: " + '{:{width}.{prec}f}'.format(self._print_dev_loss, width=6, prec=4),
                      end=" || ")
            if TEST_JOB in jobs:
                print("Acc_Test: " + '{:{width}.{prec}f}'.format(self._print_test_accuracy, width=6, prec=4) +
                      " || Loss_Test: " + '{:{width}.{prec}f}'.format(self._print_test_loss, width=6, prec=4),
                      end=" || ")
            print("")

    # plot loss / accuracy graph
    def plot_line(self, job=LOSS_PLOT, show_plot=True):
        p = figure(plot_width=600, plot_height=250, title=self._dataset_name + " - Dataset - " + job,
                   x_axis_label="epochs", y_axis_label=job)
        color1, color2, color3 = ("yellow", "orange", "red") if job == LOSS_PLOT else ("black", "green", "blue")
        if job == LOSS_PLOT:
            y_axis_train = self._loss_vec_train
            y_axis_dev = self._loss_vec_dev
            y_axis_test = self._loss_vec_test
        elif job == AUC_PLOT:
            y_axis_train = self._auc_vec_train
            y_axis_dev = self._auc_vec_dev
            y_axis_test = self._auc_vec_test
        elif job == ACCURACY_PLOT:
            y_axis_train = self._accuracy_vec_train
            y_axis_dev = self._accuracy_vec_dev
            y_axis_test = self._accuracy_vec_test

        x_axis = list(range(len(y_axis_dev)))
        p.line(x_axis, y_axis_train, line_color=color1, legend="train")
        p.line(x_axis, y_axis_dev, line_color=color2, legend="dev")
        p.line(x_axis, y_axis_test, line_color=color3, legend="test")
        if show_plot:
            output_file("foo.html")
            show(p)
        return p

    def _plot_acc_dev(self):
        self.plot_line(ACCURACY_PLOT)
        sleep(1)
        self.plot_line(ACCURACY_PLOT)
        sleep(1)
        self.plot_line(ACCURACY_PLOT)

    # def output_experiment_detail(self, res_path):
    #     exp = nni.get_experiment_id()
    #     trail = nni.get_trial_id()
    #     trail_path = os.path.join(res_path, exp, trail)
    #     if not os.path.exists(os.path.join(res_path, exp)):
    #         os.mkdir(os.path.join(res_path, exp))
    #     if not os.path.exists(trail_path):
    #         os.mkdir(trail_path)
    #
    #     # TODO whatever you want
    #     p_loss = self.plot_line(LOSS_PLOT, show_plot=False)
    #     p_acc = self.plot_line(ACCURACY_PLOT, show_plot=False)
    #     p_auc = self.plot_line(AUC_PLOT, show_plot=False)
    #
    #     measures_table = [
    #         ["train_loss_vec"] + [str(x) for x in self.loss_train_vec],
    #         ["train_acc_vec"] + [str(x) for x in self.accuracy_train_vec],
    #         ["train_auc_vec"] + [str(x) for x in self.auc_train_vec],
    #         ["dev_loss_vec"] + [str(x) for x in self.loss_dev_vec],
    #         ["dev_acc_vec"] + [str(x) for x in self.accuracy_dev_vec],
    #         ["dev_auc_vec"] + [str(x) for x in self.auc_dev_vec],
    #         ["test_loss_vec"] + [str(x) for x in self.loss_test_vec],
    #         ["test_acc_vec"] + [str(x) for x in self.accuracy_test_vec],
    #         ["test_auc_vec"] + [str(x) for x in self.auc_test_vec]
    #     ]
    #     with open(os.path.join(res_path, exp, trail, "measures_by_epochs.csv", "wt"), newline="") as f:
    #         writer = csv.writer(f)
    #         writer.writerows(measures_table)

    @property
    def model(self):
        return self._model

    @property
    def loss_train_vec(self):
        return self._loss_vec_train

    @property
    def accuracy_train_vec(self):
        return self._accuracy_vec_train

    @property
    def auc_train_vec(self):
        return self._auc_vec_train

    @property
    def loss_dev_vec(self):
        return self._loss_vec_dev

    @property
    def accuracy_dev_vec(self):
        return self._accuracy_vec_dev

    @property
    def auc_dev_vec(self):
        return self._auc_vec_dev

    @property
    def loss_test_vec(self):
        return self._loss_vec_test

    @property
    def accuracy_test_vec(self):
        return self._accuracy_vec_test

    @property
    def auc_test_vec(self):
        return self._auc_vec_test

    # load dataset
    def _load_data(self, dataset, train_size, dev_size, test_size, batch_size):
        # calculate lengths off train and dev according to split ~ (0,1)
        len_train = int(len(dataset) * train_size)
        len_dev = int(len(dataset) * dev_size)
        len_test = len(dataset) - len_train - len_dev

        # split dataset
        train, dev, test = random_split(dataset, (len_train, len_dev, len_test))

        # set train loader
        self._train_loader = DataLoader(
            train,
            batch_size=batch_size,
            collate_fn=train.dataset.collate_fn,
            shuffle=True
        )
        self._loss_weights = torch.Tensor([1 / count for label, count in
                                           sorted(list(dataset.label_count.items()), key=lambda x: x[0])])
        # set validation loader
        self._dev_loader = DataLoader(
            dev,
            batch_size=batch_size,
            collate_fn=dev.dataset.collate_fn,
        )

        # set test loader
        self._test_loader = DataLoader(
            test,
            batch_size=batch_size,
            collate_fn=test.dataset.collate_fn,
        )

    # train a model, input is the enum of the model type
    def train(self, show_plot=False, early_stop=False, wait=10, mul=0.5, stop_sign=8, norm_type=1, wd=0.001):
        lr = self._model._params["lr"]
        print(lr)
        wait_counter = 0
        bad_counter = 0
        self._init_loss_and_acc_vec()
        # calc number of iteration in current epoch
        len_data = len(self._train_loader)
        for epoch_num in range(self._epochs):
            if not self._nni:
                if not self.grid:
                    print("epoch" + str(epoch_num))

            # calc number of iteration in current epoch
            for batch_index, (A, x0, embed, label) in enumerate(self._train_loader):
                if self._gpu:
                    A, x0, embed, label = A.to(self._device), x0.to(self._device), embed.to(self._device), label.to(
                        self._device)

                # print progress
                self._model.train()

                output = self._model(A, x0, embed, test=False)  # calc output of current model on the current batch
                loss = self._loss_func(output, label.unsqueeze(dim=1).float(),
                                       weight=torch.Tensor([self._loss_weights[i].item() for i in label]).unsqueeze(
                                           dim=1).to(device=self._device)) \
                    if self._is_binary else self._loss_func(output, label,
                                                            weight=self._loss_weights.to(device=self._device))
                reg_loss = 0
                for param in self._model._qgcn_last_layer.parameters():
                    reg_loss += param.norm(norm_type)
                loss += wd * reg_loss
                # calculate loss
                loss.backward()  # back propagation
                # clip_grads(self._model, 10)

                # if (batch_index + 1) % self._batch_size == 0 or (batch_index + 1) == len_data:  # batching
                self._model.optimizer.step()  # update weights
                self._model.zero_grad()  # zero gradients

                if not self._nni:
                    if not self.grid:
                        self._print_progress(batch_index, len_data, job=TRAIN_JOB)
            # validate and print progress
            self._validate(self._train_loader, job=TRAIN_JOB)
            self._validate(self._dev_loader, job=DEV_JOB)
            self._validate(self._test_loader, job=TEST_JOB)
            if not self._nni:
                if not self.grid:
                    self._print_info(jobs=[TRAIN_JOB, DEV_JOB, TEST_JOB])

            # /----------------------  FOR NNI  -------------------------
            # if epoch_num % 1 == 0 and self._nni:
            #     dev_acc = self._print_dev_accuracy
            #     train_acc = self._print_train_accuracy
            #     nni.report_intermediate_result(min(dev_acc, train_acc))

            if early_stop and epoch_num > 10 and self._print_test_loss > np.mean(self._loss_vec_train[-10:]):
                break

            dev_acc = self._print_dev_accuracy
            if dev_acc > max(self._accuracy_vec_dev):
                wait_counter = 0
            elif dev_acc < max(self._accuracy_vec_dev):
                wait_counter += 1
            if wait_counter >= wait:
                bad_counter += 1
                wait_counter = 0
                lr *= mul
                print(f"current lr is {lr}")
                for param_group in self._model.optimizer.param_groups:
                    param_group['lr'] = lr
            if bad_counter > stop_sign:
                print("early stopping")
                break

            test_acc1 = self._print_test_accuracy

        # if self._nni:
        #     dev_acc_index = np.argmax(self._accuracy_vec_dev)
        #     dev_acc = self.accuracy_dev_vec[dev_acc_index]
        #     train_acc = self.accuracy_train_vec[dev_acc_index]
        #     print("index: ", dev_acc_index, "dev: ", dev_acc, "train: ", train_acc)
        #     # dev_auc = self._print_dev_accuracy
        #     # train_auc = self._print_train_accuracy
        #     nni.report_final_result(min(dev_acc, train_acc))
        # -----------------------  FOR NNI  -------------------------/

        if show_plot and not self._nni:
            if not self.grid:
                self._plot_acc_dev()

        return test_acc1

    # validation function only the model and the data are important for input, the others are just for print
    def _validate(self, data_loader, job=""):
        # for calculating total loss and accuracy
        loss_count = 0
        true_labels = []
        pred = []

        self._model.eval()
        # calc number of iteration in current epoch
        len_data = len(data_loader)
        for batch_index, (A, x0, embed, label) in enumerate(data_loader):
            if self._gpu:
                A, x0, embed, label = A.to(self._device), x0.to(self._device), embed.to(self._device), label.to(
                    self._device)
            # print progress
            if not self._nni:
                if not self.grid:
                    self._print_progress(batch_index, len_data, job=VALIDATE_JOB)
            output = self._model(A, x0, embed, test=False)
            # calculate total loss
            loss_count += self._loss_func(output, label.unsqueeze(dim=1).float()) if self._is_binary else \
                self._loss_func(output, label)
            true_labels += label.tolist()
            pred += output.squeeze(dim=1).tolist()

        # update loss accuracy
        loss = float(loss_count / len(data_loader))
        # pred_labels = [0 if np.isnan(i) else i for i in pred_labels]
        self._update_loss(loss, job=job)
        self._update_accuracy_binary(pred, true_labels, job=job) if self._is_binary else \
            self._update_accuracy_multiclass(pred, true_labels, job=job)
        if self._is_binary:
            self._update_auc(pred, true_labels, job=job)
        return loss


def create_data_set(dataset_name: str,
                    graph_data_params: GraphsDataParams,
                    external_params: ExternalParams):
    params = {
        "dataset_name": dataset_name,
        "external": asdict(external_params),
        "graphs_data": asdict(graph_data_params)
    }
    ext_train = ExternalData(params)
    ds = GraphsDataset(params, external_data=ext_train)
    return ds


def train_qgcn_model(dataset_name: str,
                     graph_data_params: GraphsDataParams,
                     external_params: ExternalParams,
                     model_params: ModelParams,
                     activator_params: ActivatorParams,
                     device="cpu"):
    params = {
        "dataset_name": dataset_name,
        "external": asdict(external_params),
        "graphs_data": asdict(graph_data_params),
        "model": asdict(model_params),
        "activator": asdict(activator_params)
    }

    ext_train = ExternalData(params)
    ds = GraphsDataset(params, external_data=ext_train)
    model = QGCN(params, ds.len_features, ext_train.len_embed())
    activator = QGCNActivator(model, params, ds, device=device)
    acc = activator.train()

    activator.model.eval()
    return activator.model
    # return TrainedModel(activator.model)


class TrainedModel:
    def __init__(self, model: QGCN):
        self.model = model
        self.model.eval()

    def predict(self, loader):
        outputs = []
        # why??? this is stupid!
        for _, (A, x0, embed, label) in enumerate(loader):
            output = self.model(A, x0, embed)
            outputs.append(output)

        return outputs


if __name__ == '__main__':
    from src.QGCN.dataset import ExternalData
    from src.QGCN.dataset import GraphsDataset
    from statistics import mean

    test_acc = []
    device = "cpu"

    for i in range(1):
        # params_file = "../params/mutagen_params.json"
        params_file = "../../../test/params/default_binary_params.json"
        # params_file = "../params/grec_params.json"
        # params_file = "./params/default_binary_params.json"
        ext_train = ExternalData(params_file)
        ds = GraphsDataset(params_file, external_data=ext_train)
        model = QGCN(params_file, ds.len_features, ext_train.len_embed())
        # model = QGCN(params_file, ds.len_features, [10])
        activator = QGCNActivator(model, params_file, ds, device=device)
        acc = activator.train()
        test_acc.append(acc)
        print(acc)

    # std_ = round(np.std(test_acc), 3)
    # avg = round(mean(test_acc), 3)
    # print(std_)
    # print(avg)

    # with open('mutagen_c_x1.txt', 'w') as f:
    #   for _string in test_acc:
    #      f.write(str(_string) + ' ')
    # f.write("\n")
    # f.write(str(std_))
    # f.write("\n")
    # f.write(str(avg))

    # params_file = "../params_regular/NCI109_params.json"
    # params_file = "../params/NCI1_params.json"
    # ext_train = ExternalData(params_file)
    # ds = GraphsDataset(params_file, external_data=None)
    # model = QGCN(params_file, ds.len_features, [10])
    # model = QGCN(params_file, ds.len_features, ext_train.len_embed())

    # activator = QGCNActivator(model, params_file, ds)
    # activator.train()

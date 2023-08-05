from project.model.sequential import SpatioTemporalConvolutionGru, SpatioTemporalConvolutionLstm, TemporalGru, SpatialGNN
from project.model.linear import Linear
from pytorch_lightning.loggers import NeptuneLogger
from project.data.loader import PhenomenaDataLoader, GraphDatasetIterator
from pytorch_lightning.callbacks.early_stopping import EarlyStopping
import pytorch_lightning as pl
import yaml
from pydoc import locate
import argparse

parser = argparse.ArgumentParser(description='Evaluation of neural model')
parser.add_argument('config', metavar='config path', type=str, help='The path of the configuration file')
parser.add_argument('-p', '--data-path', type=str, help='The path of the data to load for the training part')
parser.add_argument('-d', '--data-size', type=int, help='How many simulations should the system consider')
parser.add_argument('-e', '--max-epochs', type=str, help='Max number of epochs performed by the traning loop')
parser.add_argument('-a', '--accelerator', type=str, help="Accelerator used for the training loop", choices=['cpu', 'cuda', 'tpu'])

args = parser.parse_args()

with open(args.config) as file: # todo add as parameter
    configuration = yaml.load(file, Loader=yaml.FullLoader)
    metadata = configuration['metadata']
    simulations = configuration['simulations']
    for simulation in simulations:

        print("Training of " + simulation['name'])
        forecast_size = simulation['args'][1] ## forecast_size from args
        data_size = args.data_size or metadata['data_size']
        loader = PhenomenaDataLoader(args.data_path or metadata["data_path"], data_size, forecast_size)
        loader.clean_position()
        torch_graph_data = loader.data

        split_test = 0.8
        split_validation = 0.8

        split_index = int(data_size * split_test)
        torch_graph_train, torch_graph_test = torch_graph_data[:split_index], torch_graph_data[split_index:]
        split_index_val = int(len(torch_graph_train) * split_validation)
        torch_graph_train, torch_graph_validation = torch_graph_train[:split_index_val], torch_graph_train[
                                                                                         split_index_val:]

        full_classpath = simulation['module'] + "." + simulation['class_name']
        init = locate(full_classpath)
        network = init(*simulation['args'])

        neptune_logger = NeptuneLogger(
            api_key="eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vYXBwLm5lcHR1bmUuYWkiLCJhcGlfdXJsIjoiaHR0cHM6Ly9hcHAubmVwdHVuZS5haSIsImFwaV9rZXkiOiJkZjMyMzc3Ni0yZDc4LTQzMWMtYTIzMi0wMDVlMDU5MWRiMDEifQ==",
            project="PS-Lab/gnn-forecast",
            name = simulation['name'],
            description = simulation['description'],
            tags = simulation['tags']
        )

        early_stop_callback = EarlyStopping(
            monitor='val_loss',
            min_delta=0.0001,
            patience=5,
            verbose=True,
            mode='min'
        )

        trainer = pl.Trainer(
            callbacks=[early_stop_callback],
            accelerator=args.accelerator or metadata['accelerator'],
            devices=1,
            logger=neptune_logger,
            max_epochs=args.max_epochs or metadata['max_epochs']
        )

        lr_finder = trainer.tuner.lr_find(
            network,
            GraphDatasetIterator(torch_graph_train[:1]),
            GraphDatasetIterator(torch_graph_validation[:1]),
            mode="linear"
        )

        new_lr = lr_finder.suggestion()
        # update hparams of the model
        network.hparams.learning_rate = new_lr
        print("tuning ...")
        trainer.fit(network, GraphDatasetIterator(torch_graph_train), GraphDatasetIterator(torch_graph_validation))
        neptune_logger.finalize("success")
        del neptune_logger
        del loader.data

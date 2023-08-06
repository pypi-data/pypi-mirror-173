"""Pretraining DenseNet models and schedulers.

Reference: https://arxiv.org/abs/1608.06993
"""

import importlib
import os
import sys
from copy import deepcopy
from dataclasses import dataclass

import torch
import torch.nn.functional as F
from PIL import Image
from torch import nn
from torch.optim import Adam, Optimizer
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms

from ... import logger
from ...auto_ml.cvat.annotation import ImageAnnotationUtils
from ..auto_model import AutoMeta, AutoModel, DatasetMode
from ..exceptions import ConfigError
from .auto_model_cv import AutoMetaImageInput, Preprocessor

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

__all__ = [
    'AutoDenseNet',
    'DenseNet121',
    'DenseNet169',
    'DenseNet201',
    'DenseNet161',
    'DENSENET121_FED_AVG',

]


DenseNet121 = 'densenet121'
DenseNet169 = 'densenet169'
DenseNet201 = 'densenet201'
DenseNet161 = 'densenet161'
DenseNet121FedAvg = 'densenet121-fed-avg'
DenseNet169_FED_AVG = 'densenet169-fed-avg'
DenseNet201_FED_AVG = 'densenet201-fed-avg'
DenseNet161_FED_AVG = 'densenet161-fed-avg'


class DenseNetPreprocessor(Preprocessor):

    def __init__(self, mode: DatasetMode) -> None:
        self. _transformer = (
            transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.RandomAffine(degrees=10, translate=(0.02, 0.02)),
                transforms.RandomHorizontalFlip(),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            ])
            if mode == DatasetMode.TRAINING else
            transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            ])
        )

    def transform(self, image_file: str) -> torch.Tensor:
        """Transform an image object into an input tensor."""
        image = Image.open(image_file).convert('RGB')
        return self._transformer(image)


class DenseNetDataset(Dataset):

    def __init__(self, image_dir: str, annotation_file: str, mode: DatasetMode) -> None:
        """Init a dataset instance for DenseNet auto model families.

        Args:
            image_dir:
                The directory including image files.
            annotation_file:
                The file including annotation information.
            mode:
                One of training or validation or testing.
        """
        super().__init__()
        if not image_dir or not isinstance(image_dir, str):
            raise ConfigError(f'Invalid image directory: {image_dir}.')
        if not annotation_file or not isinstance(annotation_file, str):
            raise ConfigError(f'Invalid annotation file path: {annotation_file}.')
        assert mode and isinstance(mode, DatasetMode), f'Invalid dataset mode: {mode}.'
        if not os.path.exists(image_dir) or not os.path.isdir(image_dir):
            raise ConfigError(f'{image_dir} does not exist or is not a directory.')
        if not os.path.exists(annotation_file) or not os.path.isfile(annotation_file):
            raise ConfigError(f'{annotation_file} does not exist or is not a file.')

        self.image_dir = image_dir
        self.annotation_file = annotation_file
        self.transformer = DenseNetPreprocessor(mode=mode)

        self.images = ImageAnnotationUtils.parse_single_category_annotation(
            annotation_file=self.annotation_file, mode=mode
        )

    def __getitem__(self, index: int):
        _item = self.images[index]
        return self.transformer(_item.image_file), _item.class_label

    def __len__(self):
        return len(self.images)


@dataclass
class AutoMetaDenseNet(AutoMeta):

    input_meta: AutoMetaImageInput
    param_file: str
    model_class: str
    epochs: int
    batch_size: int
    lr: float
    model_file: str = None
    module_dir: str = None

    @classmethod
    def from_json(cls, data: dict) -> 'AutoMetaDenseNet':
        assert data and isinstance(data, dict), f'Invalid meta data: {data}.'

        name = data.get('name')
        input_meta = data.get('input_meta')
        model_file = data.get('model_file')
        module_dir = data.get('module_dir')
        param_file = data.get('param_file')
        model_class = data.get('model_class')
        epochs = data.get('epochs')
        batch_size = data.get('batch_size')
        lr = data.get('lr')
        if (
            not name or not isinstance(name, str)
            or not input_meta or not isinstance(input_meta, dict)
            or (not model_file and not module_dir)
            or (model_file and not isinstance(model_file, str))
            or (module_dir and not isinstance(module_dir, str))
            or not param_file or not isinstance(param_file, str)
            or not model_class or not isinstance(model_class, str)
            or not epochs or not isinstance(epochs, int) or epochs < 1
            or not batch_size or not isinstance(batch_size, int) or batch_size < 1
            or not lr or not isinstance(lr, float) or lr <= 0
        ):
            raise ConfigError(f'Invalid meta data: {data}.')
        if (
            module_dir
            and (not os.path.exists(module_dir) or not os.path.isdir(module_dir))
        ):
            err_msg = f"Module directory doesn't exist or is not a directory: {module_dir}."
            raise ConfigError(err_msg)
        if (
            not module_dir and model_file
            and (not os.path.exists(model_file) or not os.path.isfile(model_file))
        ):
            err_msg = f"Model file doesn't exist or is not a file: {model_file}."
            raise ConfigError(err_msg)
        if not os.path.exists(param_file) or not os.path.isfile(param_file):
            err_msg = f"Param file doesn't exist or is not a file: {param_file}."
            raise ConfigError(err_msg)

        return AutoMetaDenseNet(name=name,
                                input_meta=AutoMetaImageInput.from_json(input_meta),
                                param_file=param_file,
                                epochs=epochs,
                                batch_size=batch_size,
                                lr=lr,
                                model_class=model_class,
                                model_file=model_file,
                                module_dir=module_dir)


class AutoDenseNet(AutoModel):

    def __init__(self,
                 meta_data: dict,
                 resource_dir: str,
                 dataset_dir: str,
                 **kwargs) -> None:
        super().__init__(meta_data=meta_data,
                         resource_dir=resource_dir,
                         dataset_dir=dataset_dir)
        self._init_meta()
        self.epochs = self.meta.epochs
        self.batch_size = self.meta.batch_size
        self._lr = self.meta.lr
        self._epoch = 0
        self.is_cuda = torch.cuda.is_available()

        self._init_dataset()
        self._model = self._build_model()
        self._best_loss = float('inf')
        self._best_state = None
        self._overfit_index = 0

    def _init_dataset(self):
        self.num_classes = ImageAnnotationUtils.parse_num_classes(self.annotation_file)
        self.training_loader
        self.validation_loader
        self.testing_loader

    @property
    def training_loader(self) -> DataLoader:
        """Return a dataloader instance of training data."""
        if not hasattr(self, "_training_loader"):
            self._training_loader = self._build_training_data_loader()
        return self._training_loader

    def _build_training_data_loader(self) -> DataLoader:
        dataset = DenseNetDataset(image_dir=self.dataset_dir,
                                  annotation_file=self.annotation_file,
                                  mode=DatasetMode.TRAINING)
        return DataLoader(dataset=dataset,
                          batch_size=self.batch_size,
                          shuffle=True)

    @property
    def validation_loader(self) -> DataLoader:
        """Return a dataloader instance of validation data."""
        if not hasattr(self, "_validation_loader"):
            self._validation_loader = self._build_validation_data_loader()
        return self._validation_loader

    def _build_validation_data_loader(self) -> DataLoader:
        dataset = DenseNetDataset(image_dir=self.dataset_dir,
                                  annotation_file=self.annotation_file,
                                  mode=DatasetMode.VALIDATION)
        return DataLoader(dataset=dataset, batch_size=self.batch_size)

    @property
    def testing_loader(self) -> DataLoader:
        """Return a dataloader instance of testing data."""
        if not hasattr(self, "_testing_loader"):
            self._testing_loader = self._build_testing_data_loader()
        return self._testing_loader

    def _build_testing_data_loader(self) -> DataLoader:
        dataset = DenseNetDataset(image_dir=self.dataset_dir,
                                  annotation_file=self.annotation_file,
                                  mode=DatasetMode.TESTING)
        return DataLoader(dataset=dataset, batch_size=self.batch_size)

    def _build_model(self):
        sys.path.insert(0, self.resource_dir)
        if self.meta.module_dir:
            module = importlib.import_module(os.path.basename(self.meta.module_dir),
                                             self.meta.module_dir)
        else:
            module = importlib.import_module(os.path.basename(self.meta.model_file)[:-3],
                                             self.meta.model_file[:-3])
        model_class = getattr(module, self.meta.model_class)
        _model: nn.Module = model_class(num_classes=self.num_classes)
        with open(self.meta.param_file, 'rb') as f:
            state_dict = torch.load(f)
            if self.num_classes != 1000:  # num_classes different to pretrained
                state_dict.pop('classifier.weight')
                state_dict.pop('classifier.bias')
            _model.load_state_dict(state_dict, strict=False)
        return _model

    def _init_meta(self):
        model_file = self.meta_data.get('model_file')
        module_dir = self.meta_data.get('module_dir')
        param_file = self.meta_data.get('param_file')
        assert (
            (model_file and isinstance(model_file, str))
            or (module_dir and isinstance(module_dir, str))
        ), f'Invalid meta data: {self.meta_data}'
        assert param_file and isinstance(param_file, str), f'Invalid meta data: {self.meta_data}'
        if module_dir:
            self.meta_data['module_dir'] = os.path.join(self.resource_dir, module_dir)
        else:
            self.meta_data['model_file'] = os.path.join(self.resource_dir, model_file)
        self.meta_data['param_file'] = os.path.join(self.resource_dir, param_file)
        self.meta = AutoMetaDenseNet.from_json(self.meta_data)

    @property
    def optimizer(self) -> Optimizer:
        assert self._model, 'Must initialize the model at first.'
        if not hasattr(self, '_optimizer'):
            self._optimizer = Adam(self._model.parameters(),
                                   lr=self.lr,
                                   betas=(0.9, 0.999),
                                   weight_decay=5e-4)
        else:
            # update lr
            latest_lr = self.lr
            for param_group in self._optimizer.param_groups:
                param_group['lr'] = latest_lr
        return self._optimizer

    @property
    def lr(self) -> float:
        return self._lr * 0.95**((self._epoch - 1) // 5)

    def train(self):
        self._model.train()

    def eval(self):
        self._model.eval()

    def forward(self, input: torch.Tensor):
        return self._model(input)

    def fine_tune(self):
        self._epoch = 1
        while not self._is_finished():
            self._train_an_epoch()
            self._epoch += 1

        self._save_fine_tuned()
        self._run_test()

    def _train_an_epoch(self):
        self.train()
        for images, targets in self.training_loader:
            if self.is_cuda:
                images, targets = images.cuda(), targets.cuda()
            output = self._model(images)
            output = F.log_softmax(output, dim=-1)
            loss = F.nll_loss(output, targets)
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

    def _is_finished(self) -> bool:
        """Decide if stop training.

        If there are validation dataset, decide depending on validatation results. If
        the validation result of current epoch is below the best record for 3 continuous
        times, then stop training.
        If there are no validation dataset, run for `epochs` (default 20) times.
        """
        if not self.validation_loader or len(self.validation_loader) == 0:
            if self._epoch > self.epochs:
                self._best_state = deepcopy(self._model.state_dict())
            return self._epoch > self.epochs
        # make a validation
        self.eval()
        total_loss = 0
        for images, targets in self.validation_loader:
            if self.is_cuda:
                images, targets = images.cuda(), targets.cuda()
            output = self._model(images)
            output = F.log_softmax(output, dim=-1)
            total_loss += F.nll_loss(output, targets, reduction='sum').item()
        if total_loss < self._best_loss:
            self._best_loss = total_loss
            self._best_state = deepcopy(self._model.state_dict())
            return False
        else:
            self._overfit_index += 1
            return self._overfit_index > 2

    def _save_fine_tuned(self):
        """Save the best or final state of fine tuning. TODO."""
        with open('FedIRM.pt', 'wb') as f:
            torch.save(self._best_state, f)

    def _run_test(self):
        """Run a test and report the result."""
        self.eval()
        total_loss = 0
        total_correct = 0
        for images, targets in self.testing_loader:
            if self.is_cuda:
                images, targets = images.cuda(), targets.cuda()
            output = self._model(images)
            output = F.log_softmax(output, dim=-1)
            total_loss += F.nll_loss(output, targets, reduction='sum').item()
            pred = output.max(1, keepdim=True)[1]
            total_correct += pred.eq(targets.view_as(pred)).sum().item()

        avg_loss = total_loss / len(self.testing_loader.dataset)
        correct_rate = total_correct / len(self.testing_loader.dataset) * 100
        logger.info(f'Average Loss: {avg_loss:.4f}')
        logger.info(f'Correct rate: {correct_rate:.2f}')

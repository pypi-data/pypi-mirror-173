"""Define base AutoModel interfaces."""

import os
from abc import ABC, ABCMeta, abstractmethod
from dataclasses import dataclass
from enum import Enum, unique
from typing import Any


@unique
class TaskMode(int, Enum):

    LOCAL = 1
    FED_AVG = 2
    HETERO_NN_HOST = 3
    HETERO_NN_COLLABORATOR = 4


@unique
class DatasetMode(int, Enum):

    TRAINING = 1
    VALIDATION = 2
    TESTING = 3


@dataclass
class Meta(ABC):
    ...


@dataclass
class AutoMeta(Meta, metaclass=ABCMeta):
    """Manage meta data of a auto model."""

    name: str


class AutoModel(ABC):
    """An model which supports alphamed AutoML process."""

    def __init__(self,
                 meta_data: dict,
                 resource_dir: str,
                 dataset_dir: str,
                 **kwargs) -> None:
        super().__init__()
        self.meta_data = meta_data
        self.resource_dir = resource_dir
        self.dataset_dir = dataset_dir
        self.annotation_file = os.path.join(dataset_dir, 'annotation.json')

    @abstractmethod
    def train(self):
        """Go into `train` mode as of torch.nn.Module."""

    @abstractmethod
    def eval(self):
        """Go into `eval` mode as of torch.nn.Module."""

    @abstractmethod
    def forward(self, *args, **kwargs):
        """Do a forward propagation as of torch.nn.Module."""

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.forward(*args, **kwargs)

    @abstractmethod
    def fine_tune(self):
        """Begin to fine-tune on dataset."""

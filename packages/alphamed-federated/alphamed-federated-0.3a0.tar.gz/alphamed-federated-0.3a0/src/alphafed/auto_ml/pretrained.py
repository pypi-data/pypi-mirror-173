"""An easy way to get pretrained auto models."""

from typing import Dict, Type
from .exceptions import ConfigError
from .cv import *  # noqa: F403
from .auto_model import AutoModel


AUTO_MODEL_MAP: Dict[str, Type[AutoModel]] = {
    DenseNet121: AutoDenseNet,  # noqa: F405
    DenseNet169: AutoDenseNet,  # noqa: F405
    DenseNet201: AutoDenseNet,  # noqa: F405
    DenseNet161: AutoDenseNet,  # noqa: F405
}


def from_pretrained(name: str,
                    meta_data: dict,
                    resource_dir: str,
                    dataset_dir: str,
                    **kwargs) -> AutoModel:
    """Initiate an AutoModel instance from pretrained models.

    Args:
        meta_data:
            The metadata of the pretrained model.
        resource_dir:
            The root dir of the resource for setup process, i.e. parameter files.
        dataset_dir:
            The root dir of the dataset staff.
        kwargs:
            Other keyword arguments.
    """
    if not name:
        raise ConfigError('Must specify the name of auto model.')
    if not AUTO_MODEL_MAP.get(name):
        raise ConfigError(f'No auto model found for name: {name}.')
    return AUTO_MODEL_MAP[name](meta_data=meta_data,
                                resource_dir=resource_dir,
                                dataset_dir=dataset_dir,
                                **kwargs)

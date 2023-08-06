"""CVAT annotation utils."""

import json
import os
from dataclasses import dataclass
from typing import Dict, List

import torch
import torch.nn.functional as F

from ... import logger
from ..auto_model import DatasetMode
from ..exceptions import AutoModelError, ConfigError


class ParseError(AutoModelError):
    ...


@dataclass
class ImageAnnotation:

    image_file: str


@dataclass
class ImageSingleCategoryAnnotation(ImageAnnotation):

    class_label: torch.LongTensor


@dataclass
class ImageMultiCategoryAnnotation(ImageAnnotation):

    class_labels: torch.LongTensor


class ImageAnnotationUtils:

    @classmethod
    def parse_num_classes(cls, annotation_file: str) -> int:
        """Parse annotation file to find out the number of classes."""
        if not annotation_file or not isinstance(annotation_file, str):
            raise ConfigError(f'Invalid annotation file: {annotation_file}.')
        if not os.path.exists(annotation_file) or not os.path.isfile(annotation_file):
            raise ConfigError(f'Annotation file {annotation_file} doesn\'t exist or is not a file.')

        try:
            with open(annotation_file, 'r') as f:
                annotations: dict = json.load(f)
        except json.JSONDecodeError:
            logger.exception('Failed to parse annotation file.')
            raise ParseError('Failed to parse annotation file.')
        labels: list = annotations.get('labels')
        if not labels or len(labels) < 1:
            raise ParseError('Missing labels.')
        return len(labels)

    @classmethod
    def parse_single_category_annotation(
        cls, annotation_file: str, mode: DatasetMode
    ) -> List[ImageSingleCategoryAnnotation]:
        """Parse annotation file for single category classification."""
        if not annotation_file or not isinstance(annotation_file, str):
            raise ConfigError(f'Invalid annotation file: {annotation_file}.')
        assert mode and isinstance(mode, DatasetMode), f'Invalid dataset mode: {mode}.'
        if not os.path.exists(annotation_file) or not os.path.isfile(annotation_file):
            raise ConfigError(f'Annotation file {annotation_file} doesn\'t exist or is not a file.')

        try:
            with open(annotation_file, 'r') as f:
                annotations: dict = json.load(f)
        except json.JSONDecodeError:
            logger.exception('Failed to parse annotation file.')
            raise ParseError('Failed to parse annotation file.')
        labels: list = annotations.get('labels')
        if not labels or len(labels) < 1:
            raise ParseError('Missing labels.')

        if mode == DatasetMode.TRAINING:
            dataset: List[Dict] = annotations.get('Train')
            if not dataset or len(dataset) < 1:
                raise ParseError('Missing training dataset.')
        elif mode == DatasetMode.VALIDATION:
            dataset: List[Dict] = annotations.get('Validation', [])
        elif mode == DatasetMode.TESTING:
            dataset: List[Dict] = annotations.get('Test')
            if not dataset or len(dataset) < 1:
                raise ParseError('Missing testing dataset.')
        else:
            raise ParseError(f'Invalid dataset mode: {mode}.')

        annotation_objs: List[ImageSingleCategoryAnnotation] = []
        for _data in dataset:
            path = _data.get('path')
            tags = _data.get('tags')
            # filter invalid samples
            if (
                not path or not isinstance(path, str)
                or not os.path.exists(path)
                or not os.path.isfile(path)
                or not tags or not isinstance(tags, list)
                or len(tags) != 1 or not isinstance(tags[0], dict)
                or not tags[0].get('label') in labels
            ):
                continue

            image_class = labels.index(tags[0]['label'])
            image_class = torch.LongTensor([image_class]).squeeze()
            annotation_objs.append(
                ImageSingleCategoryAnnotation(image_file=path, class_label=image_class))

        return annotation_objs

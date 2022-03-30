# Copyright (C) 2021-2022 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
#
import numpy as np
from typing import Dict, List, Optional, Tuple

from ote_sdk.entities.annotation import (
    Annotation,
    AnnotationSceneEntity,
    AnnotationSceneKind,
)

from ote_sdk.entities.dataset_item import DatasetItemEntity
from ote_sdk.entities.datasets import DatasetEntity
from ote_sdk.entities.label import Domain, LabelEntity
from ote_sdk.entities.scored_label import ScoredLabel
from ote_sdk.entities.subset import Subset
from ote_sdk.entities.shapes.rectangle import Rectangle
from ote_sdk.entities.text import Text

from .text_mel_dataset import parse_ljspeech_dataset


class OTETextToSpeechDataset(DatasetEntity):
    """Dataloader for LJSpeech To Text Task.

    Args:
        csv_path (str): csv file in ljspeech format.
        data_path (str): path to media files.
    """

    def __init__(
        self,
        csv_path: str = None,
        data_path: str = None,
    ):

        items: List[DatasetItemEntity] = []

        subset = Subset.TRAINING
        if "_val" in csv_path:
            subset = Subset.VALIDATION
        elif "_test" in csv_path:
            subset = Subset.TESTING

        items.extend(
            self.get_dataset_items(
                csv_path=csv_path,
                data_path=data_path,
                subset=subset
            )
        )

        super().__init__(items=items)

    @staticmethod
    def get_dataset_items(
        csv_path: str, data_path: str, subset: Subset
    ) -> List[DatasetItemEntity]:
        """Loads dataset based on the csv file.

        Args:
            csv_path (str): csv file in ljspeech format.
            data_path (str): path to media files.
            subset (Subset): Subset of the dataset (train, val, test).

        Returns:
            List[DatasetItemEntity]: List containing subset dataset.
        """
        dataset_items = []

        data = parse_ljspeech_dataset(csv_path, data_path)
        for sample in data:
            input_data = Text(file_path=sample["text"])
            label = LabelEntity(name=sample["audio_path"], domain=Domain.TEXT_TO_SPEECH)
            labels = [ScoredLabel(label)]
            annotations = [Annotation(shape=Rectangle(x1=0, y1=0, x2=1, y2=1), labels=labels)]
            annotation_scene = AnnotationSceneEntity(
                annotations=annotations, kind=AnnotationSceneKind.ANNOTATION
            )
            dataset_item = DatasetItemEntity(
                media=input_data, annotation_scene=annotation_scene, subset=subset
            )
            # Add to dataset items
            dataset_items.append(dataset_item)

        return dataset_items

import json
import logging
import uuid
from copy import deepcopy
from datetime import datetime
from functools import partial
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional, Tuple, Union, cast

import cv2
import numpy as np
import pandas as pd
import pycocotools.mask as mask_utils
import pytz
from encord import Project
from pandas import Series
from tqdm import tqdm

from encord_active.common.iterator import Iterator

logger = logging.getLogger(__name__)
GMT_TIMEZONE = pytz.timezone("GMT")
DATETIME_STRING_FORMAT = "%a, %d %b %Y %H:%M:%S %Z"
BBOX_KEYS = {"x", "y", "h", "w"}


# === UTILITIES === #
def get_timestamp():
    now = datetime.now()
    new_timezone_timestamp = now.astimezone(GMT_TIMEZONE)
    return new_timezone_timestamp.strftime(DATETIME_STRING_FORMAT)


def lower_snake_case(s: str):
    return "_".join(s.lower().split())


class PredictionIterator(Iterator):
    def __init__(self, project: Project, cache_dir: Path, use_images: bool = False, subset_size: int = -1, **kwargs):
        super().__init__(project, cache_dir, use_images, subset_size, **kwargs)
        label_hashes = set(self.label_rows.keys())

        # Predictions
        predictions_file = cache_dir / "predictions" / "predictions.csv"
        predictions = pd.read_csv(predictions_file, index_col=0)
        self.length = predictions["img_id"].unique().shape[0]

        identifiers = predictions["identifier"].str.split("_", expand=True)
        identifiers.columns = ["label_hash", "du_hash", "frame"][: len(identifiers.columns)]
        identifiers["frame"] = pd.to_numeric(identifiers["frame"])

        predictions = pd.concat([predictions, identifiers], axis=1)
        predictions["pidx"] = predictions.index

        self.predictions = predictions[predictions["label_hash"].isin(label_hashes)]

        # Class index
        class_idx_file = cache_dir / "predictions" / "class_idx.json"
        with class_idx_file.open("r", encoding="utf-8") as f:
            class_idx = json.load(f)

        self.ontology_objects = {
            int(k): next(o for o in self.project.ontology["objects"] if v["featureHash"] == o["featureNodeHash"])
            for k, v in class_idx.items()
        }

        self.uuids: Dict[str, int] = {}

    def __get_unique_object_hash(self, pred: Series):
        object_hash = str(uuid.uuid4())[:8]
        while object_hash in self.uuids:
            object_hash = str(uuid.uuid4())[:8]
        self.uuids[object_hash] = pred["pidx"]
        return object_hash

    def get_image_path(self, pred: Series) -> Optional[Path]:
        img_folder = self.cache_dir / "data" / pred["label_hash"] / "images"
        du_hash = pred["du_hash"]
        image_options = list(img_folder.glob(f"{du_hash}.*"))
        if len(image_options) == 1:
            return image_options[0]
        elif len(image_options) > 1:
            re_matches = [frame_file for frame_file in image_options if frame_file.stem == f"{du_hash}_{pred['frame']}"]
            if re_matches:
                return re_matches[0]
        return None

    def get_encord_object(self, pred: Tuple[Any, Series], width: int, height: int):
        # Note: Currently, track ids are not considered.

        _pred = pred[1]
        ontology_object: dict = self.ontology_objects[_pred["class_id"]]
        if ontology_object["shape"] == "bounding_box":
            x1, y1, x2, y2 = _pred["x1"], _pred["y1"], _pred["x2"], _pred["y2"]
            object_data = {
                "x": x1 / width,
                "y": y1 / height,
                "w": (x2 - x1) / width,
                "h": (y2 - y1) / height,
            }
        else:
            mask = mask_utils.decode(eval(_pred["rle"]))
            contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
            if len(contours) > 1:
                max_idx = np.argmax(list(map(cv2.contourArea, contours)))
                contour = contours[max_idx].reshape((-1, 2))
            else:
                contour = contours[0].reshape((-1, 2))

            if contour.shape[0] < 3:
                pass
                # logger.warning("Skipping contour with less than 3 vertices.")
            object_data = {
                str(i): {"x": round(c[0] / width, 4), "y": round(c[1] / height, 4)} for i, c in enumerate(contour)
            }

        object_hash = self.__get_unique_object_hash(_pred)
        timestamp: str = get_timestamp()
        shape: str = ontology_object["shape"]

        object_dict = {
            "name": ontology_object["name"],
            "color": ontology_object["color"],
            "value": lower_snake_case(ontology_object["name"]),
            "createdAt": timestamp,
            "createdBy": "model_predictions@encord.com",
            "confidence": _pred["confidence"],
            "objectHash": object_hash,
            "featureHash": ontology_object["featureNodeHash"],
            "lastEditedAt": timestamp,
            "lastEditedBy": "model_predictions@encord.com",
            "shape": shape,
            "manualAnnotation": False,
            "reviews": [],
        }

        if shape == "bounding_box":
            object_dict["boundingBox"] = {k: round(v, 4) for k, v in object_data.items()}
        elif shape == "polygon":
            object_dict["polygon"] = object_data

        return object_dict

    def iterate(self, desc: str = "") -> Generator[Tuple[dict, Optional[Path]], None, None]:
        pbar = tqdm(total=self.length, desc=desc, leave=False)
        for label_hash, lh_group in self.predictions.groupby("label_hash"):
            if label_hash not in self.label_rows:
                continue

            self.label_hash = label_hash
            label_row = self.label_rows[label_hash]
            self.dataset_title = label_row["dataset_title"]

            for frame, fr_preds in lh_group.groupby("frame"):
                self.du_hash = fr_preds.iloc[0]["du_hash"]
                self.frame = frame

                du = deepcopy(label_row["data_units"][self.du_hash])
                width = int(du["width"])
                height = int(du["height"])

                du["labels"] = {
                    "objects": list(
                        map(partial(self.get_encord_object, width=width, height=height), fr_preds.iterrows())
                    ),
                    "classifications": [],
                }
                yield du, self.get_image_path(fr_preds.iloc[0])
                pbar.update(1)

    def __len__(self):
        return self.length

    def get_identifier(self, object: Union[dict, list[dict], None] = None, frame: Optional[int] = None) -> Any:
        """
        Note that this only makes sense for scoring each object individually.
        """
        if object is None:
            raise NotImplementedError("Prediction iterator doesn't support associating one score each frame.")

        if isinstance(object, list):
            raise NotImplementedError("Prediction iterator doesn't support associating one score to multiple objects.")

        _obj = cast(dict, object)
        return self.uuids[_obj["objectHash"]]

    def get_data_url(self):
        # No need for the url as it is in the predictions.csv file already
        return ""

    def get_label_logs(self, object_hash: Optional[str] = None, refresh: bool = False) -> List[dict]:
        # Fail safe
        raise NotImplementedError("Label logs are not available for predictions.")

    @staticmethod
    def update_cache_dir(cache_dir: Path) -> Path:
        # Store prediction specific scores in the predictions subdirectory
        return cache_dir / "predictions"

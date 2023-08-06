# Standard library imports
import os
from pathlib import Path

from ..georeference import georeference
from ..utils import remove_files
from .fix_labels import fix_labels
from .rasterize_labels import rasterize_labels
from .reproject_labels import reproject_labels_to_epsg3857


def preprocess(data_path: str, input_dir: str, image_dir: str, mask_dir: str) -> None:
    """Fully preprocess the input data.

    Args:
        data_path: Path of the directory where all the data are stored.
        input_dir: Name of the directory where the input data are stored.
        image_dir: Name of the directory where the images are stored.
        mask_dir: Name of the directory where the masks are stored.
    """
    data_path, input_dir = Path(data_path), Path(input_dir)
    assert os.path.isdir(data_path / input_dir), "Input data directory wasn't found."
    os.chdir(data_path)

    for sub_dir in os.listdir(input_dir):
        assert os.path.exists(
            input_dir / sub_dir / "labels.geojson"
        ), "Label file wasn't found."

        georeference(str(input_dir), sub_dir, image_dir)
        fix_labels(str(input_dir), sub_dir, image_dir)
        reproject_labels_to_epsg3857(image_dir, sub_dir, image_dir)
        rasterize_labels(image_dir, sub_dir, mask_dir)

        remove_files(f"{mask_dir}/{sub_dir}/*.geojson")
        remove_files(f"{image_dir}/{sub_dir}/*.geojson")

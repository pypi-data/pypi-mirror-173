# Standard library imports
import os
from glob import glob
from pathlib import Path

from .utils import get_bounding_box


def georeference(input_dir: str, sub_dir: str, output_dir: str, is_mask=False) -> None:
    """Perform georeferencing and remove the fourth band from images (if any).

    If the image has only one band, that fourth band removal part
    will be skipped.

    The EPSG:3857 projected coordinate system is used
    ('WGS 84 / Pseudo-Mercator', coordinates in meters).

    Args:
        input_dir: Name of the directory where the input data are stored.
        sub_dir: Name of the subdirectory under the input directory.
        output_dir: Name of the directory where the output data will go.
        is_mask: Whether the image is binary or not.
    """
    input_dir, output_dir = Path(input_dir), Path(output_dir)
    os.makedirs(Path(output_dir) / sub_dir, exist_ok=True)

    for path in glob(f"{input_dir}/{sub_dir}/*.png"):
        filename = Path(path).stem
        x_min, y_min, x_max, y_max = get_bounding_box(filename)

        # Bounding box defined by upper left and lower right corners
        bounding_box = f"{x_min} {y_max} {x_max} {y_min}"
        in_file = input_dir / sub_dir / f"{filename}.png"
        out_file = output_dir / sub_dir / f"{filename}.tif"
        process_image = f"""
            gdal_translate \
                -b 1 {'' if is_mask else '-b 2 -b 3'} \
                -a_ullr {bounding_box} \
                -a_srs EPSG:3857 \
                {in_file} {out_file} 
        """
        os.system(process_image)

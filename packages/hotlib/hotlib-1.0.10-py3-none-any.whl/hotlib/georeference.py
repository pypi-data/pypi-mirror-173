# Standard library imports
import os
from glob import glob

from .utils import get_bounding_box, get_prefix


def georeference(input_dir: str, sub_dir: str, out_dir: str, is_mask=False) -> None:
    """Perform georeferencing and remove the fourth band from images (if any).

    If the image has only one band, that fourth band removal part
    will be skipped.

    The EPSG:3857 projected coordinate system is used
    ('WGS 84 / Pseudo-Mercator', coordinates in meters).

    Args:
        input_dir: Name of the directory where the input data are stored.
        sub_dir: Name of the subdirectory under the input directory.
        out_dir: Name of the directory where the output data will go.
        is_mask: Whether the image is binary or not.
    """
    os.makedirs(f"{out_dir}/{sub_dir}", exist_ok=True)

    for path in glob(f"{input_dir}/{sub_dir}/*.png"):
        filename = get_prefix(path)
        x_min, y_min, x_max, y_max = get_bounding_box(filename)

        # Bounding box defined by upper left and lower right corners
        bounding_box = f"{x_min} {y_max} {x_max} {y_min}"

        process_image = f"""
            gdal_translate \
                -b 1 {'' if is_mask else '-b 2 -b 3'} \
                {input_dir}/{sub_dir}/{filename}.png \
                {out_dir}/{sub_dir}/{filename}.tif \
                -a_ullr {bounding_box} \
                -a_srs EPSG:3857
        """
        os.system(process_image)

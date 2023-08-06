# Standard library imports
import os
from glob import glob
from pathlib import Path

from ..utils import get_bounding_box


def rasterize_labels(input_dir: str, sub_dir: str, output_dir: str) -> None:
    """Rasterize the GeoJSON labels for each of the aerial images.

    For each of the OAM images, the corresponding GeoJSON file is
    clipped first. Then, the clipped GeoJSON files are converted to TIFs.

    The EPSG:3857 projected coordinate system is used
    ('WGS 84 / Pseudo-Mercator', coordinates in meters).

    Args:
        input_dir: Name of the directory where the input data are stored.
        sub_dir: Name of the subdirectory under the input directory.
        output_dir: Name of the directory where the output data will go.
    """
    input_dir, output_dir = Path(input_dir), Path(output_dir)
    os.makedirs(output_dir / sub_dir, exist_ok=True)

    for path in glob(f"{input_dir}/{sub_dir}/*.tif"):
        filename = Path(path).stem
        x_min, y_min, x_max, y_max = get_bounding_box(filename)

        # A string with bounding box "x_min y_min x_max y_max"
        # This format is expected by ogr2ogr and gdal_rasterize commands
        bounding_box = f"{x_min} {y_min} {x_max} {y_max}"
        orig_geojson_file = input_dir / sub_dir / "labels_epsg3857.geojson"
        clipped_geojson_file = output_dir / sub_dir / f"{filename}.geojson"
        raster_file = output_dir / sub_dir / f"{filename}.tif"

        clip_labels = f"""
            ogr2ogr \
                -clipsrc {bounding_box} \
                -f GeoJSON {clipped_geojson_file} {orig_geojson_file}
        """
        os.system(clip_labels)

        rasterize_labels = f"""
            gdal_rasterize \
                -ot Byte \
                -burn 255 \
                -ts 256 256 \
                -te {bounding_box} \
                {clipped_geojson_file} {raster_file}
        """
        os.system(rasterize_labels)

import os
from glob import glob

from ..utils import get_bounding_box, get_prefix


def rasterize_labels(input_dir: str, sub_dir: str, out_dir: str) -> None:
    """Rasterize the GeoJSON labels for each of the aerial images.

    For each of the OAM images, the corresponding GeoJSON files are
    clipped first. Then, the clipped GeoJSON files are converted to TIFs.

    The EPSG:3857 projected coordinate system is used
    ('WGS 84 / Pseudo-Mercator', coordinates in meters).

    Args:
        input_dir: Name of the directory where the input data are stored.
        sub_dir: Name of the subdirectory under the input directory.
        out_dir: Name of the directory where the output data will go.
    """
    os.makedirs(f"{out_dir}/{sub_dir}", exist_ok=True)

    for path in glob(f"{input_dir}/{sub_dir}/*.tif"):
        filename = get_prefix(path)
        x_min, y_min, x_max, y_max = get_bounding_box(filename)

        # A string with bounding box "x_min y_min x_max y_max"
        # This format is expected by ogr2ogr and gdal_rasterize commands
        bounding_box = f"{x_min} {y_min} {x_max} {y_max}"

        clip_labels = f"""
            ogr2ogr \
                -clipsrc {bounding_box} \
                -f GeoJSON \
                {out_dir}/{sub_dir}/{filename}.geojson \
                {input_dir}/{sub_dir}/labels_epsg3857.geojson
        """
        os.system(clip_labels)

        rasterize_labels = f"""
            gdal_rasterize \
                -ot Byte \
                -burn 255 \
                -ts 256 256 \
                -te {bounding_box} \
                {out_dir}/{sub_dir}/{filename}.geojson \
                {out_dir}/{sub_dir}/{filename}.tif
        """
        os.system(rasterize_labels)

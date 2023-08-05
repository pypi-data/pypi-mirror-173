# Standard library imports
import os


def reproject_labels_to_epsg3857(input_dir: str, sub_dir: str, out_dir: str) -> None:
    """Convert a GeoJSON file with labels from EPSG:4326 to EPSG:3857.

    A new GeoJSON file is created, it contains coordinates in meters
    (easting, northing) in the 'WGS 84 / Pseudo-Mercator' projection.

    Args:
        input_dir: Name of the directory where the input data are stored.
        sub_dir: Name of the subdirectory under the input directory.
        out_dir: Name of the directory where the output data will go.
    """
    os.makedirs(f"{out_dir}/{sub_dir}", exist_ok=True)

    reproject_labels = f"""
        ogr2ogr \
            -s_srs EPSG:4326 \
            -t_srs EPSG:3857 \
            -f GeoJSON \
            {out_dir}/{sub_dir}/labels_epsg3857.geojson \
            {input_dir}/{sub_dir}/labels.geojson
    """
    os.system(reproject_labels)

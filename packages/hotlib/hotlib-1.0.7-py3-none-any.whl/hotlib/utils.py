# Standard library imports
import math
import os
import re
from glob import glob
from typing import Tuple

from osgeo import ogr, osr

IMAGE_SIZE = 256


def get_prefix(path: str) -> str:
    """Get filename prefix (without extension) from full path."""
    filename = os.path.basename(path)
    return os.path.splitext(filename)[0]


def get_bounding_box(filename: str) -> Tuple[float, float, float, float]:
    """Get the four corners of the OAM image as EPSG:3857 coordinates.

    This function gives us the limiting values that we will pass to
    the GDAL commands. We need to make sure that the raster image
    that we're generating have the same dimension as the original image.
    Hence, we'll need to fetch these extrema values.

    Returns:
        A tuple, (x_min, y_min, x_max, y_max), with coordinates in meters.
    """
    _, *tile_info = re.split("-", filename)
    x_tile, y_tile, zoom = map(int, tile_info)

    # Lower left and upper right corners in degrees
    lower_left = num2deg(x_tile, y_tile + 1, zoom)
    upper_right = num2deg(x_tile + 1, y_tile, zoom)

    # Convert to meters
    x_min, y_min = reproject_point(lower_left, 4326, 3857)
    x_max, y_max = reproject_point(upper_right, 4326, 3857)

    return x_min, y_min, x_max, y_max


def num2deg(x_tile: int, y_tile: int, zoom: int) -> Tuple[float, float]:
    """Convert tile numbers to EPSG:4326 coordinates.

    Convert tile numbers to the WGS84 latitude/longitude coordinates
    (in degrees) of the upper left corner of the tile.

    Args:
        x_tile: Tile X coordinate
        y_tile: Tile Y coordinate
        zoom: Level of detail

    Returns:
        A tuple (latitude, longitude) in degrees.
    """
    n = 2.0**zoom
    lon_deg = x_tile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * y_tile / n)))
    lat_deg = math.degrees(lat_rad)

    return lat_deg, lon_deg


def reproject_point(
    coord_tuple: Tuple[float, float], source_epsg: int, target_epsg: int
) -> Tuple[float, float]:
    """Reproject a point to a different coordinate reference system.

    For EPSG:4326, the returned tuple would be (latitude, longitude).

    Args:
        coord_tuple: (X, Y) coordinates of the point
        source_epsg: Source EPSG code
        target_epsg: Target EPSG code

    Returns:
        (X, Y) coordinates in the target EPSG projected
            coordinate system.
    """
    source = osr.SpatialReference()
    source.ImportFromEPSG(source_epsg)

    target = osr.SpatialReference()
    target.ImportFromEPSG(target_epsg)

    transform = osr.CoordinateTransformation(source, target)

    point = ogr.CreateGeometryFromWkt(f"POINT ({coord_tuple[0]} {coord_tuple[1]})")
    point.Transform(transform)

    return point.GetX(), point.GetY()


def remove_files(pattern: str) -> None:
    """Remove files matching a wildcard."""
    files = glob(pattern)
    for file in files:
        os.remove(file)

import os
import glob

import geopandas as gpd
import pandas as pd
from shapely.geometry import LineString, Point
from shapely.ops import substring

from CONSTANTS import NYC_CRS
from utils import setup_logging

logger = setup_logging()

SRC_DIR = "processed_activities"
OUT_DIR = "bridges"


def midpoint_along_line(line: LineString) -> Point:
    """Return the point at the halfway cumulative distance along the line.

    This lands exactly on the line of points and follows the bridge's curve,
    rather than the geometric midpoint of the endpoints.
    """
    half = line.length / 2.0
    return substring(line, half, half)


def enclosing_radius_m(line_local: LineString, mid_local: Point) -> float:
    """Largest distance (meters) from the midpoint to any vertex of the line.

    This is the radius that just encloses the whole bridge from its midpoint.
    The frontend pads it a little so the circle sits just outside the bridge.
    """
    return max(mid_local.distance(Point(c)) for c in line_local.coords)


def chart_data(point_frames: list[gpd.GeoDataFrame]) -> pd.DataFrame:
    """Combine all bridges' points into one tabular CSV (no geometry).

    Takes the per-bridge point frames collected in main(), drops the geometry
    column, and concatenates them into a single flat table suitable for
    charting on the frontend.
    """
    combined = pd.concat(point_frames, ignore_index=True)
    df = pd.DataFrame(combined.drop(columns="geometry"))
    df = df[["bridge", "point_id", "track_seg_point_id",
             "distance", "ele", "ele_change"]]
    out_path = os.path.join(OUT_DIR, "chart_data.csv")
    df.to_csv(out_path, index=False)
    logger.info(f"Wrote chart_data.csv with {len(df)} rows")
    return df


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    point_frames = []
    line_records = []
    mid_records = []

    for path in sorted(glob.glob(os.path.join(SRC_DIR, "*.geojson"))):
        bridge = os.path.splitext(os.path.basename(path))[0]
        logger.info(f"Preparing bridge: {bridge}")

        gdf = gpd.read_file(path)
        gdf = gdf.sort_values("point_id").reset_index(drop=True)
        gdf["bridge"] = bridge

        # 1. combined points
        point_frames.append(gdf)

        # 2. line connecting all points (ordered)
        line = LineString(gdf.geometry.tolist())
        line_records.append({"bridge": bridge, "geometry": line})

        # 3. midpoint at halfway cumulative distance, measured in local NYC CRS
        #    so the "halfway" is in true ground distance, then back to lon/lat.
        line_local = (
            gpd.GeoSeries([line], crs=4326).to_crs(epsg=NYC_CRS).iloc[0]
        )
        mid_local = midpoint_along_line(line_local)
        mid = gpd.GeoSeries([mid_local], crs=NYC_CRS).to_crs(epsg=4326).iloc[0]

        # radius (meters) that just encloses the bridge from its midpoint,
        # measured in the local NYC CRS for true ground distance. The frontend
        # converts this to pixels at the current zoom and adds a small margin.
        radius_m = enclosing_radius_m(line_local, mid_local)
        mid_records.append(
            {"bridge": bridge, "radius_m": round(radius_m, 1), "geometry": mid}
        )

    # 1. combined points
    points = gpd.GeoDataFrame(pd.concat(point_frames, ignore_index=True), crs=4326)
    points = points[["bridge", "point_id", "track_seg_point_id",
                     "distance", "ele", "ele_change", "geometry"]]
    points.to_file(os.path.join(OUT_DIR, "bridges_points.geojson"), driver="GeoJSON")
    logger.info(f"Wrote {len(points)} points across {len(point_frames)} bridges")

    # 2. lines
    lines = gpd.GeoDataFrame(line_records, crs=4326)
    lines.to_file(os.path.join(OUT_DIR, "bridges_lines.geojson"), driver="GeoJSON")
    logger.info(f"Wrote {len(lines)} lines")

    # 3. midpoints
    mids = gpd.GeoDataFrame(mid_records, crs=4326)
    mids.to_file(os.path.join(OUT_DIR, "bridges_midpoints.geojson"), driver="GeoJSON")
    logger.info(f"Wrote {len(mids)} midpoints")

    # 4. flat chart data (no geometry)
    chart_data(point_frames)


if __name__ == "__main__":
    main()

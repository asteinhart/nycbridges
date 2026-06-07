import os
import geopandas as gpd
from CONSTANTS import LOOKUP, NYC_CRS
from utils import setup_logging

logger = setup_logging()

os.makedirs("processed_activities", exist_ok=True)

def process_activity(bridge: str, id: str, start_point, end_point) -> gpd.GeoDataFrame:
    """
    Process the activity data for a given ID and return a GeoDataFrame.

    Parameters:
    bridge (str): The name of the bridge.
    id (str): The ID of the activity to process.
    start_point: The starting point of the activity.
    end_point: The ending point of the activity.

    Returns:
    gpd.GeoDataFrame: A GeoDataFrame containing the processed activity data.
    """
    logger.info(f"Processing activity with ID: {id}")

    #load activity
    act = gpd.read_file(f"activities/{id}.gpx", layer="track_points")

    #sort to be safe
    act = act.sort_values("track_seg_point_id")

    filtered = act[(act["track_seg_point_id"] >= start_point) & (act["track_seg_point_id"] <= end_point)]

    #check which direction is larger climb to flip if needed
    if filtered["ele"].iloc[0] > filtered["ele"].iloc[-1]:
        logger.info(f"Flipping activity with ID: {id} for bridge: {bridge}")
        filtered = filtered.iloc[::-1].reset_index(drop=True)

    #reset index to be safe
    filtered = filtered.reset_index(drop=False)
    filtered["point_id"] = filtered.index + 1

    #convert to local NYC CRS to measure
    filtered = filtered.to_crs(epsg=NYC_CRS)

    #change ele to feet from meters
    filtered["ele"] = filtered["ele"] * 3.28084

    #measure distance all from first point
    filtered["distance"] = filtered.geometry.distance(filtered.geometry.shift()).fillna(0).cumsum()

    #ele change
    filtered["ele_change"] = filtered["ele"] - filtered["ele"].iloc[0]

    filtered = filtered.to_crs(epsg=4326)
    filtered = filtered[["point_id","track_seg_point_id","distance", "ele","ele_change","geometry"]]

     # write to file
    filtered.to_file(f"processed_activities/{bridge}.geojson", driver="GeoJSON")
        
    return filtered

def main():
    for bridge, info in LOOKUP.items():
        logger.info(f"Processing bridge: {bridge}")
        gdf = process_activity(bridge, info["activity_id"], info["start_point"], info["end_point"])
        logger.info(f"Finished processing bridge: {bridge}")
       
        # Further processing or saving of gdf can be done here

if __name__ == "__main__":
    main()
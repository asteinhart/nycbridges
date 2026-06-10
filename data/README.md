# Data

This folder contains the scripts and inputs used to collect and process bridge crossing activity data.

## Files

- [getAllActivities.py](getAllActivities.py) downloads Garmin activities as GPX files into `activities/`.
- [processActivities.py](processActivities.py) reads the saved GPX files, extracts the bridge-specific segments, and writes GeoJSON files into `processed_activities/`.
- [CONSTANTS.py](CONSTANTS.py) stores the bridge lookup table, activity IDs, point ranges, and the NYC coordinate reference system.
- [utils.py](utils.py) sets up logging.
- [activities/](activities/) contains raw GPX activity files.
- [processed_activities/](processed_activities/) contains processed bridge GeoJSON files.

## Requirements

- Python dependencies listed in the project environment.
- A Garmin account with `EMAIL` and `PASSWORD` set in your environment or `.env` file.

## Usage

Download GPX activities:

```bash
python getAllActivities.py
```

Process the bridge activities into GeoJSON:

```bash
python processActivities.py
```

## Output

- Raw activity files are saved as `activities/<date>_<activity_id>.gpx`.
- Processed bridge segments are saved as `processed_activities/<bridge>.geojson`.

import os
from garminconnect import Garmin
from dotenv import load_dotenv
from utils import setup_logging 

logger = setup_logging()

load_dotenv()

email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')

def get_all_activities(email, password, start=0, limit=100, verbose=False):
    api = Garmin(
        email,
        password,
        prompt_mfa=lambda: input("MFA code: "),
    )
    api.login("~/.garminconnect")

    # ACTIVITIES
    # Get activities data from start and limit
    activities = api.get_activities(start, limit) # 0=start, 1=limit
 
    # create a file path for the activity
    if not os.path.exists("activities"):
        os.makedirs("activities")

    ## Download an Activity
    for activity in activities:
        activity_id = activity["activityId"]
        # date, no time
        date = activity["startTimeLocal"].split(" ")[0]
        if verbose:
            logger.info("api.download_activities(%s)", activity_id)
        gpx_data = api.download_activity(activity_id, dl_fmt=api.ActivityDownloadFormat.GPX)
        output_file = f"activities/{date}_{str(activity_id)}.gpx"
        with open(output_file, "wb") as fb:
            fb.write(gpx_data)


if __name__ == "__main__":
    get_all_activities(email, password, verbose=True)
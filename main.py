import requests
from datetime import datetime
from secrets import (
    MY_LAT,
    MY_LONG,
    TARGET_EMAIL_ACCOUNT,
)
from email import send_mail

VICINITY_THRESHOLD = 0.05


def are_coordinates_between_threshold(first_coordinate, second_coordinate):
    return first_coordinate - VICINITY_THRESHOLD < second_coordinate < first_coordinate + VICINITY_THRESHOLD


def is_my_position_nearby(iss_latitude, iss_longitude):
    return are_coordinates_between_threshold(iss_latitude, MY_LAT) \
           and are_coordinates_between_threshold(iss_longitude, MY_LONG)


def is_dark():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()
    return time_now.hour < sunrise or time_now.hour > sunset


def fetch_iss_position():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_position = data["iss_position"]
    iss_latitude = float(iss_position["latitude"])
    iss_longitude = float(iss_position["longitude"])
    return iss_latitude, iss_longitude


if __name__ == '__main__':
    iss_latitude, iss_longitude = fetch_iss_position()
    if is_my_position_nearby(iss_latitude, iss_longitude) and is_dark():
        send_mail(
            content="Look up!",
            target_email_address=TARGET_EMAIL_ACCOUNT
        )


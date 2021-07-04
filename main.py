import requests
from datetime import datetime
from secrets import (
    MY_LAT,
    MY_LONG,
)

VICINITY_THRESHOLD = 0.05

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])


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


if is_my_position_nearby(iss_latitude, iss_longitude) and is_dark():



    #If the ISS is close to my current position
    # and it is currently dark
    # Then send me an email to tell me to look up.
    # BONUS: run the code every 60 seconds.




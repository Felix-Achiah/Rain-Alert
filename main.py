import requests
from twilio.rest import Client
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/onecall"
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILO_AUTH_TOKEN")
api_key = os.getenv("API_KEY")
account_sid = TWILIO_ACCOUNT_SID
auth_token = TWILIO_AUTH_TOKEN

weather_params = {
    "lat": 5.564540,
    "lon": -0.225710,
    "appid": api_key,
    "exclude": "current,minutely,daily"
}

response = requests.get(OWM_ENDPOINT, params=weather_params)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["hourly"][:12]

will_rain = False

for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body="It's going to rain today. Remember to bring an ☂️",
        from_='+14302224091',
        to=YOUR_PHONE_NUMBER
    )

    print(message.status)

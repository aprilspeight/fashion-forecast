from dotenv import load_dotenv
import os
from openai import OpenAI
import requests

# Load environment variables from .env file
load_dotenv()

client = OpenAI()

api_url = os.getenv("WEATHER_API_CALL")

# Make a function for the call

def getWeather():
    # put weather call here
    try: 
        response = requests.get(api_url)
        response.raise_for_status()

        data = response.json()

        location = data['location']['name']
        temperature = int(data['current']['temp_f'])
        condition = data['current']['condition']['text']

        completion = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a meteorologist who gives the weather report in the style of Diana Vreeland. You provide outfit suggestions according to the temperature. Your report should not exceed 2 sentences. Mention the weather with the ° symbol."},
            {"role": "user", "content": f"Give me the weather report for a {temperature} degree fahrenheit day in {location}. The condition is {condition}."}
            ]
        )

        print(completion.choices[0].message.content)

    except requests.exceptions.HTTPError as http_err:
        # Handle HTTP errors (4xx and 5xx status codes)
        print(f"HTTP Error: {http_err}")
    except requests.exceptions.RequestException as req_err:
        # Handle other request-related errors
        print(f"Request Error: {req_err}")
    except Exception as err:
        # Handle general exceptions
        print(f"An error occurred: {err}")

getWeather()
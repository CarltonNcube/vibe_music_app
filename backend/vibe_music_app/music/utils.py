import os
from dotenv import load_dotenv
import requests

load_dotenv()


# Deezer API key
API_KEY = os.getenv("API_KEY")

def top_artists():

    url = "https://billboard-api5.p.rapidapi.com/api/charts/artist-100"    

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "billboard-api5.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    response_data = response.json()
    return response_data["chart"]

def top_tracks():
    url = "https://billboard-api5.p.rapidapi.com/api/charts/hot-100"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "billboard-api5.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    return data
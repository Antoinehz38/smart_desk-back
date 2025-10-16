from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import requests
import httpx
import asyncio
from typing import Optional
from datetime import datetime, timedelta


from tools.confort import well_being_score

API_BASE = "https://api.thingspeak.com"


app = FastAPI(title="ThingSpeak proxy API for channel 3120427")

# Autoriser le front local (NiceGUI)
origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/data_all")
def get_data_all():
    url = "https://api.thingspeak.com/channels/3120427/feeds.json"
    params = {"results": 5}
    response = requests.get(url, params)
    Temperature = [response.json()["feeds"][i]["field1"] for i in range(len(response.json()["feeds"]))]
    Pressure= [response.json()["feeds"][i]["field2"] for i in range(len(response.json()["feeds"]))]
    Hum = [response.json()["feeds"][i]["field3"] for i in range(len(response.json()["feeds"]))]
    Time = [response.json()["feeds"][i]["created_at"] for i in range(len(response.json()["feeds"]))]


    return {"ok": True, "Temp":Temperature, "Press": Pressure, "Hum":Hum, "Time":Time}

@app.get("/well-being-score")
def get_well_being_score():
    url = "https://api.thingspeak.com/channels/3120427/feeds.json"
    params = {"results": 1}
    response = requests.get(url, params)

    Temperature = response.json()["feeds"][0]["field1"]
    pressure = response.json()["feeds"][0]["field2"]
    hum = response.json()['feeds'][0]['field3']

    score = well_being_score(temp_c= Temperature,press_hpa=pressure, hum=hum)

    return {"ok": True, "well_being_score": score * 100}








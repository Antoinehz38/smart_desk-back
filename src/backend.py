from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import requests
import httpx
import asyncio
from typing import Optional
from datetime import datetime, timedelta


from tools.confort import well_being_score

API_BASE = "https://api.thingspeak.com"
ID_ROOM = 3120427

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

@app.get("/data/all")
async def get_data_all():
    global ID_ROOM
    url = f"https://api.thingspeak.com/channels/{ID_ROOM}/feeds.json"
    params = {"results": 5}
    response = requests.get(url, params)
    Temperature = [response.json()["feeds"][i]["field1"] for i in range(len(response.json()["feeds"]))]
    Pressure= [response.json()["feeds"][i]["field2"] for i in range(len(response.json()["feeds"]))]
    Hum = [response.json()["feeds"][i]["field3"] for i in range(len(response.json()["feeds"]))]
    Time = [response.json()["feeds"][i]["created_at"] for i in range(len(response.json()["feeds"]))]


    return {"ok": True, "temperature":Temperature, "pressure": Pressure, "humidity":Hum, "time":Time}

@app.get("/data/well-being-score")
async def get_well_being_score():
    url = "https://api.thingspeak.com/channels/3120427/feeds.json"
    params = {"results": 1}
    response = requests.get(url, params)

    Temperature = float(response.json()["feeds"][0]["field1"])
    pressure = float(response.json()["feeds"][0]["field2"])
    hum = float(response.json()['feeds'][0]['field3'])

    score = well_being_score(temp_c= Temperature,press_hpa=pressure, hum=hum)

    return {"ok": True, "well_being_score": score }


@app.put("/room/change")
async def put_new_room_number(data):
    global ID_ROOM
    ID_ROOM = data.get("ID_ROOM", ID_ROOM)
    return {"ok": True}






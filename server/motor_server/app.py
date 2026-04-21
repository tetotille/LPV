from __future__ import annotations
import asyncio
import math
import random
import time
from fastapi import FastAPI
import uvicorn

state = {
    "running": False,
    "speed": 0.0,
    "temp": 25.0,
    "limit": 3200.0,
    "over": False,
}

app = FastAPI(title="Motor Server Local")

async def loop():
    phase = 0.0
    while True:
        await asyncio.sleep(0.3)
        if state["running"]:
            phase += 0.25
            target_speed = 2800 + 450 * math.sin(phase) + random.uniform(-80, 80)
            state["speed"] += 0.20 * (target_speed - state["speed"])
            target_temp = 40 + state["speed"] / 120 + random.uniform(-0.4, 0.4)
            state["temp"] += 0.05 * (target_temp - state["temp"])
        else:
            state["speed"] += 0.18 * (0.0 - state["speed"])
            state["temp"] += 0.05 * (25.0 - state["temp"])

        if abs(state["speed"]) < 0.5:
            state["speed"] = 0.0
        state["over"] = state["speed"] > state["limit"]

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(loop())

@app.get("/status")
def status():
    return {
        "running": state["running"],
        "speed": round(state["speed"], 2),
        "temp": round(state["temp"], 2),
        "limit": round(state["limit"], 2),
        "over": state["over"],
        "timestamp": time.time(),
    }

@app.post("/run")
def run():
    state["running"] = True
    return {"ok": True, "message": "Motor iniciado"}

@app.post("/stop")
def stop():
    state["running"] = False
    return {"ok": True, "message": "Motor detenido"}

def main():
    uvicorn.run("motor_server.app:app", host="127.0.0.1", port=8443, reload=False)

if __name__ == "__main__":
    main()

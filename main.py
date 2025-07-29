from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from datetime import datetime
import os
import logging

# configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#load enviroment variable
load_dotenv()

app = FastAPI()

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Pydantic model for health data
class HealthData(BaseModel):
    uid: str
    heart_rate: int
    temperature: float
    blood_pressure: str
    oxygen_saturation: float

# Record health parameters
@app.post("/health-data")
async def record_health_data(data: HealthData):
    try:
        # Store health data
        health_record = {
            "uid": data.uid,
            "heart_rate": data.heart_rate,
            "temperature": data.temperature,
            "blood_pressure": data.blood_pressure,
            "oxygen_saturation": data.oxygen_saturation,
        }
        
        response = supabase.table("sensor_data").insert(health_record).execute()
        
        return {"message": "Health data recorded successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get health data
@app.get("/health-data/{uid}")
async def get_health_data(uid: str):
    try:
        # Retrieve health data
        data = supabase.table("sensor_data").select("*").eq("uid", uid).order("recorded_at", desc=True).execute()
        
        return {"health_data": data.data}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
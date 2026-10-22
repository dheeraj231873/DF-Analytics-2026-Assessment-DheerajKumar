from pathlib import Path
import sys

import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field
from sklearn.linear_model import LinearRegression
import joblib

PROJECT_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_DIR / "outputs" / "hourly_energy_model.joblib"

app = FastAPI(
    title="Household Energy Forecasting API",
    description="API for predicting hourly household energy consumption.",
    version="1.0.0"
)

class HourlyPredictionInput(BaseModel):
    lag_1: float = Field(ge=0)
    lag_2: float = Field(ge=0)
    lag_3: float = Field(ge=0)
    lag_6: float = Field(ge=0)
    lag_12: float = Field(ge=0)
    lag_24: float = Field(ge=0)
    lag_48: float = Field(ge=0)
    lag_168: float = Field(ge=0)
    hour_of_day: int = Field(ge=0, le=23)
    day_of_week: int = Field(ge=0, le=6)
    month: int = Field(ge=1, le=12)

@app.get("/")
def home():
    return {"message": "Household Energy Forecasting API is running"}

@app.post("/predict/hourly-energy")
def predict_hourly_energy(data: HourlyPredictionInput):
    if not MODEL_PATH.exists():
        return {
            "error": "Model file not found. Export the trained hourly model first."
        }

    model = joblib.load(MODEL_PATH)
    features = pd.DataFrame([data.model_dump()])
    prediction = max(0.0, float(model.predict(features)[0]))

    return {
        "predicted_energy_consumption_kWh": round(prediction, 4)
    }
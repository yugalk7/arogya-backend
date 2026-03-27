from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import joblib
import numpy as np

app = FastAPI()

# 🔥 ADD CORS

app.add_middleware(
CORSMiddleware,
allow_origins=["*"],  # allow all for now
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

model = joblib.load("model/arogya_rf_model.pkl")

class PatientVitals(BaseModel):
    Age: int
    Gender: str
    HeartRate: float
    Temperature: float
    SpO2: float
    Household_ID: str

@app.get("/")
def home():
    return {"message": "Arogya ML backend running"}

def preprocess(vitals: PatientVitals):
    gender = 1 if vitals.Gender.lower() == "female" else 0
    is_febrile = 1 if vitals.Temperature > 38 else 0
    is_hypoxic = 1 if vitals.SpO2 < 94 else 0


    return np.array([[
        vitals.Age,
        gender,
        vitals.HeartRate,
        vitals.Temperature,
        vitals.SpO2,
        is_febrile,
        is_hypoxic
    ]])


def calculate_hcrs(confidence):
    infected = int(confidence // 25)
    hcrs = infected * confidence


    if hcrs < 30:
        status = "Safe"
    elif hcrs < 60:
        status = "Warning"
    else:
        status = "Critical"

    return round(hcrs, 2), status


@app.post("/predict")
def predict(vitals: PatientVitals):
    features = preprocess(vitals)


    prob = model.predict_proba(features)[0][1]
    confidence = round(prob * 100, 2)

    risk_status = "High" if confidence > 60 else "Low"

    hcrs, cluster_status = calculate_hcrs(confidence)

    return {
        "confidence_score": confidence,
        "risk_status": risk_status,
        "hcrs": hcrs,
        "cluster_status": cluster_status
    }


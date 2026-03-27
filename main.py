from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import os

app = FastAPI()

# 🔥 Load model

model = joblib.load("model/arogya_rf_model.pkl")

# 🔹 Input schema

class PatientVitals(BaseModel):
    Age: int
    Gender: str
    HeartRate: float
    Temperature: float
    SpO2: float
    Household_ID: str

# 🔹 Home route (for testing)

@app.get("/")
def home():
 return {"message": "Arogya ML backend running"}

# 🔹 Preprocessing

def preprocess(vitals: PatientVitals):
    gender = 1 if vitals.Gender.lower() == "female" else 0
    is_febrile = 1 if vitals.Temperature > 38 else 0
    is_hypoxic = 1 if vitals.SpO2 < 94 else 0

    features = np.array([[
        vitals.Age,
        gender,
        vitals.HeartRate,
        vitals.Temperature,
        vitals.SpO2,
        is_febrile,
        is_hypoxic
    ]])

    return features


# 🔹 Household risk (simple logic)

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


# 🔹 Prediction route

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


# 🔥 IMPORTANT FOR RENDER

if name == "main":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)

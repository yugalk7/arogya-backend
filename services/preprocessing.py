import numpy as np

def preprocess(vitals):
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


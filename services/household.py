def calculate_hcrs(confidence_score):
# Temporary simulation
    infected_members = int(confidence_score // 25)
    avg_risk = confidence_score

    hcrs = infected_members * avg_risk

    if hcrs < 30:
        status = "Safe"
    elif hcrs < 60:
        status = "Warning"
    else:
        status = "Critical"

    return round(hcrs, 2), status
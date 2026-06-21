"""
Risk calculation engine for Risk Assessment App.

Risk factors are weighted as follows:
- Crime: 35%
- Weather: 30%
- Disaster History: 20%
- Population: 15%

Calculates individual risk factors, total risk score, risk level, and recommendation.
"""

# Risk calculation based on crime count
def calculate_crime_risk(crime_count):
    if crime_count <= 10:
        return 5
    elif crime_count <= 25:
        return 25
    elif crime_count <= 50:
        return 50
    elif crime_count <= 80:
        return 75
    else:
        return 100

# Risk calculation based on storm count
def calculate_weather_risk(storm_count):
    if storm_count <= 5:
        return 5
    elif storm_count <= 15:
        return 15
    elif storm_count <= 30:
        return 35
    elif storm_count <= 50:
        return 60
    else:
        return 100

# Risk calculation based on disaster count
def calculate_disaster_risk(disaster_count):
    if disaster_count == 0:
        return 0
    elif disaster_count <= 3:
        return 10
    elif disaster_count <= 10:
        return 25
    elif disaster_count <= 20:
        return 50
    elif disaster_count <= 30:
        return 75
    else:
        return 100
    
# Risk calculation based on population
def calculate_population_risk(population):
    if population < 5000:
        return 10
    elif population < 20000:
        return 25
    elif population < 50000:
        return 50
    else:
        return 100
    
# Total risk calculation 
def calculate_total_risk(weather, disaster, crime, population):

    total = ( 
        crime * 0.35+ 
        weather * 0.30+ 
        disaster * 0.20+ 
        population * 0.15
        )

    if total <= 30:
        level = "Low Risk"
    elif total <= 40:
        level = "Moderate Risk"
    elif total <= 60:
        level = "Elevated Risk"
    else:
        level = "High Risk"

    return {
        "risk_score": round(total),
        "risk_level": level
    }

# Returns a recommendation based on the calculated risk level
def get_recommendation(level):
    if level == "Low Risk":
        return "No immediate action needed."
    elif level == "Moderate Risk":
        return "Minimal precautions recommended."
    elif level == "Elevated Risk":
        return "Consider taking precautions."
    else:
        return "Take preventive action."
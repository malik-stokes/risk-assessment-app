from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.services.crime_service import get_crime_data
from app.services.weather_service import get_weather_data
from app.services.disaster_service import get_disaster_data
from app.services.census_service import get_population_data

from app.database import engine, SessionLocal
from app.models import Assessment

# Creates database tables if they don't already exist
Assessment.metadata.create_all(bind=engine)

from app.services.risk_engine import (
    calculate_crime_risk,
    calculate_weather_risk,
    calculate_disaster_risk,
    calculate_population_risk,
    calculate_total_risk,
    get_recommendation
)

# Root endpoint (health check)
# Usage: GET http://127.0.0.1:8000/
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Risk Assessment API is running"}

# Main analysis endpoint
# Usage: GET http://127.0.0.1:8000/analyze/{zip_code}
@app.get("/analyze/{zip_code}")
def get_risk_assessment(zip_code: str):

    # Fetch data from APIs
    crime_data = get_crime_data(zip_code)
    weather_data = get_weather_data(zip_code)
    disaster_data = get_disaster_data(zip_code)
    population_data = get_population_data(zip_code)

    # Convert raw data into risk scores
    crime_risk = calculate_crime_risk(crime_data["crime_count"])
    weather_risk = calculate_weather_risk(weather_data["storm_count"])
    disaster_risk = calculate_disaster_risk(disaster_data["disaster_count"])
    population_risk = calculate_population_risk(population_data["population"])

    # Calculate total risk score and risk level
    risk_result = calculate_total_risk(
        weather_risk, 
        disaster_risk, 
        crime_risk, 
        population_risk
    )

    risk_score = risk_result["risk_score"]
    risk_level = risk_result["risk_level"]

    # Get recommendation based on risk level
    recommendation = get_recommendation(risk_level)

    # Open database session
    db = SessionLocal()

    try:
        # Create database record
        assessment = Assessment(
            zip_code=zip_code,

            crime_count=crime_data["crime_count"],
            storm_count=weather_data["storm_count"],
            disaster_count=disaster_data["disaster_count"],
            population=population_data["population"],

            risk_score=risk_score,
            risk_level=risk_level,
            recommendation=recommendation
        )

        db.add(assessment)
        db.commit()

    finally:
        db.close()

    # Return API response
    return {
        "zip_code": zip_code,

        "raw_data": {
            "crime_count": crime_data["crime_count"],
            "storm_count": weather_data["storm_count"],
            "disaster_count": disaster_data["disaster_count"],
            "population": population_data["population"]
        },

        "risk_factors": {
            "crime": {
                "risk": crime_risk,
                "weighted": round(crime_risk * 0.35, 1)
            },
            "weather": {
                "risk": weather_risk,
                "weighted": round(weather_risk * 0.30, 1)
            },
            "disaster": {
                "risk": disaster_risk,
                "weighted": round(disaster_risk * 0.20, 1)
            },
            "population": {
                "risk": population_risk,
                "weighted": round(population_risk * 0.15, 1)
            }
        },

        "overall_risk_assessment": {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "recommendation": recommendation
        }
    }

# ===========================
# History Endpoints (READ)
# ===========================

# Get the most recent 25 assessments
# Usage: GET http://127.0.0.1:8000/history
@app.get("/history")
def get_history():

    db = SessionLocal()

    try:
        # Get latest 25 records (newest first)
        assessments = (
            db.query(Assessment)
            .order_by(Assessment.created_at.desc())
            .limit(25)
            .all()
        )

        results = []

        for assessment in assessments:
            results.append({
                "id": assessment.id,
                "zip_code": assessment.zip_code,
                "crime_count": assessment.crime_count,
                "storm_count": assessment.storm_count,
                "disaster_count": assessment.disaster_count,
                "population": assessment.population,
                "risk_score": assessment.risk_score,
                "risk_level": assessment.risk_level,
                "recommendation": assessment.recommendation,
                "created_at": assessment.created_at
            })

    finally:
        db.close()

    return results

# ===========================
# History Endpoints (DELETE)
# ===========================

# Delete a single assessment by ID
# Usage: DELETE http://127.0.0.1:8000/history/{assessment_id}
@app.delete("/history/{assessment_id}")
def delete_assessment(assessment_id: int):

    db = SessionLocal()

    try:
        # Find record by primary key
        assessment = (
            db.query(Assessment)
            .filter(Assessment.id == assessment_id)
            .first()
        )

        # If not found, return message
        if not assessment:
            db.close()
            return {"message": "Assessment not found"}

        # Delete record from database
        db.delete(assessment)
        db.commit()
    
        return {"message": f"Assessment {assessment_id} deleted"}
    
    finally:
        db.close()

# Delete ALL assessments
# Usage: DELETE http://127.0.0.1:8000/history
@app.delete("/history")
def clear_history():

    db = SessionLocal()

    try:
        # Delete every record in the table
        db.query(Assessment).delete()
        db.commit()

        return {"message": "All assessments deleted"}

    finally:
        db.close()

    
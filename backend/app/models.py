from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.database import Base


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)

    zip_code = Column(String, nullable=False)

    crime_count = Column(Integer)
    storm_count = Column(Integer)
    disaster_count = Column(Integer)
    population = Column(Integer)

    risk_score = Column(Integer)
    risk_level = Column(String)
    recommendation = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)
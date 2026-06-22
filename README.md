# Risk Assessment App

A full-stack risk analysis platform that evaluates environmental and demographic risk for any U.S. ZIP code using multiple external data sources and a custom weighted scoring engine.

The application generates a risk score and recommendation based on crime, weather, disaster history, and population data.

---

## Live Features

- ZIP code-based risk analysis
- Real-time weather + precipitation integration
- Disaster history lookup by state (FEMA API)
- Crime risk simulation layer (extensible placeholder)
- Population data via U.S. Census API
- Weighted risk scoring system
- Categorized risk levels:
  - Low Risk
  - Moderate Risk
  - Elevated Risk
  - High Risk
- Persistent assessment history
- Search + filtering system
- Clean, responsive UI with Tailwind CSS

---

## Tech Stack

### Frontend
- Next.js (React)
- TypeScript
- Tailwind CSS

### Backend
- FastAPI
- Python
- SQLite
- SQLAlchemy 

### External APIs
- Zippopotam.us (ZIP → location lookup)
- Open-Meteo (weather + precipitation data)
- FEMA Disaster Declarations API
- U.S. Census Bureau ACS API

---

## Quick Start

1. Clone the repository
2. Configure the `.env` file
3. Install backend and frontend dependencies
4. Start the FastAPI backend
5. Start the Next.js frontend

## How It Works

### 1. Weather Service
- Converts ZIP code → latitude/longitude via Zippopotam.us
- Fetches weather data from Open-Meteo
- Aggregates precipitation into a storm risk score
- Feeds result into risk engine

---

### 2. Disaster Service
- Converts ZIP → state abbreviation
- Queries FEMA disaster declarations dataset
- Counts historical disaster frequency per state
- Used as a regional risk factor

---

### 3. Crime Service (Placeholder)
- Simulated crime dataset based on ZIP code
- Designed as a replaceable module
- Ensures full system functionality without external dependency

---

### 4. Census Service
- Uses U.S. Census ACS API
- Retrieves population by ZIP (ZCTA)
- Normalized into demographic risk factor

---

### 5. Risk Engine (Core Logic)
The central processing system:

- Normalizes all inputs to a 0–100 scale
- Applies weighted scoring:

  | Factor      | Weight |
  |------------|--------|
  | Crime       | 35%    |
  | Weather     | 30%    |
  | Disaster    | 20%    |
  | Population  | 15%    |

- Produces:
  - Final risk score (0–100)
  - Risk category
  - Human-readable recommendation

---

## API Endpoint

### Analyze Risk
```bash
GET /analyze/{zip_code}
```

Returns:
- Raw data sources
- Normalized risk factors
- Weighted contributions
- Final risk score
- Recommendation

---

## Data Model (Overview)

Stored assessments include:

- ZIP code
- Crime count
- Storm count
- Disaster count
- Population
- Risk score
- Risk level
- Recommendation
- Timestamp

---

## Project Structure
```
risk-assessment-app/
├── backend/
│   ├── app/
│   │   ├── services/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   └── risk_engine.py
│   ├── requirements.txt
│   └── .env.example
│ 
├── frontend/
│   ├── app/
│   │   ├── page.tsx
│   │   ├── history/
│   │   └── layout.tsx
│   ├── public/
│   ├── package.json
│   └── next.config.ts
│ 
└── .gitignore
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/risk-assessment-app.git
cd risk-assessment-app
```

### 2. Configure environment variables

Navigate to the `cd backend` folder.

Copy `.env.example` to a new file named `.env`.

```text
backend/
├── .env.example
└── .env
```

This project uses the U.S. Census Bureau API to retrieve population data. Request a free API key from the U.S. Census Bureau:

https://api.census.gov/data/key_signup.html

Then add your API key to the `.env` file:

```env
CENSUS_API_KEY=your_api_key_here
```

The `.env` file is ignored by Git to prevent sensitive information from being committed.

### 3. Install backend dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 4. Install frontend dependencies

```bash
cd ../frontend
npm install
```

### 5. Run the application

Backend:

```bash
uvicorn app.main:app --reload
```

Frontend:

```bash
npm run dev
```

---

## Current Limitations

- Crime data is simulated (not live)
- Risk model is simplified for demonstration
- Population uses ZCTA-level approximation
- Weights are manually tuned (not actuarial)

---

## Future Improvements

- Integrate live crime data API
- Add population density calculations
- Historical weather trend analysis
- Machine learning-based risk scoring
- Persisted analytics dashboards
- User authentication system
- Data visualization (charts & graphs)
- Improved FastAPI testing suite

---

## Disclaimer

This application is a **proof-of-concept**. Risk scores are not intended for:
- Insurance decisions
- Financial decisions
- Safety or emergency planning

All scoring logic is custom-built for demonstration purposes.

---

## Summary

This project demonstrates:

- Full-stack development (FastAPI + Next.js)
- External API integration
- Data normalization and scoring systems
- Backend architecture design
- Frontend UI development with Tailwind
- Persistent storage and filtering
- Real-world production-style structuring

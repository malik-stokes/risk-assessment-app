# FEMA Disaster API
# Fetches disaster declarations and filters them by ZIP-code related state 

import requests

# Converts ZIP code into a state abbreviation using Zippopotam.us
def get_state_from_zip(zip_code):
    url = f"https://api.zippopotam.us/us/{zip_code}"

    try:
        response = requests.get(url, timeout=10)

        # If ZIP is invalid or API fails, return None
        if response.status_code != 200:
            return None

        data = response.json()

        # Extract state abbreviation (e.g. "GA", "NY", "CA")
        state = data["places"][0]["state abbreviation"]

        return state

    except Exception:
        return None

# Fetches FEMA disaster data and filters it by state
# Applies weighted scoring based on disaster severity
def get_disaster_data(zip_code):

    url = (
        "https://www.fema.gov/api/open/v2/DisasterDeclarationsSummaries"
        "?$top=500&$format=json"
    )

    try:
        response = requests.get(url, timeout=10)

        # Handle potential errors in API response
        if response.status_code != 200:
            return {"disaster_count": 0}

        data = response.json()

        # FEMA returns all disaster records here
        records = data.get("DisasterDeclarationsSummaries", [])

        # Converts ZIP code into state abbreviation (e.g. "GA", "NY", "CA")
        state = get_state_from_zip(zip_code)

        # If state lookup fails, return 0
        if state is None:
            return {"disaster_count": 0}

        # Filters FEMA records to only include disasters in that state
        filtered_records = [
            r for r in records
            if r.get("state") == state
        ]

        # Weighted disaster scoring logic
        disaster_score = 0

        for r in filtered_records:
            incident_type = r.get("incidentType", "")

            # Higher severity disasters
            if incident_type in ["Hurricane", "Tornado", "Fire"]:
                disaster_score += 2

            # Moderate disasters
            elif incident_type in ["Severe Storm", "Flood", "Storm"]:
                disaster_score += 1

            # Default for any other disaster types
            else:
                disaster_score += 1

        return {
            "disaster_count": disaster_score
        }
    except (ValueError, KeyError, IndexError):
        return {"disaster_count": 0}

    except Exception:
        return {"disaster_count": 0}
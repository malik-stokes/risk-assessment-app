# Census Service to fetch population data based on ZIP code

import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("CENSUS_API_KEY")

def get_population_data(zip_code):

    # If API key is missing, return default value
    if not API_KEY:
        return {"population": 0}

    url = (
        "https://api.census.gov/data/2022/acs/acs5"
        f"?get=NAME,B01003_001E"
        f"&for=zip%20code%20tabulation%20area:{zip_code}"
        f"&key={API_KEY}"
    )

    try:
        response = requests.get(url, timeout=10)

        # Handle potential errors in API response
        if response.status_code != 200:
            return {"population": 0}
        
        # Convert API response to JSON
        data = response.json()

        # Ensure API returned valid data and has at least:
        # - row 0: headers
        # - row 1: actual population data
        if not data or len(data) < 2:
            return {"population": 0}

        row = data[1]

        # Population value is stored in the second column
        if len(row) < 2:
            return {"population": 0}

        population = int(row[1])

        return {
            "population": population
        }
        
    except (ValueError, KeyError, IndexError):
        return {"population": 0}

    except Exception:
        return {"population": 0}

# Weather Service
# Uses Zippopotam.us for ZIP-to-coordinate lookup
# Uses Open-Meteo for weather data

import requests

# Converts a ZIP code into latitude and longitude coordinates 
# required for Open-Meteo weather API
def get_coordinates(zip_code):

    url = f"https://api.zippopotam.us/us/{zip_code}"
    
    response = requests.get(url, timeout=10)

    # Handle potential errors in API response
    if response.status_code != 200:
        return None

    data = response.json()

    place = data["places"][0]

    return (
        float(place["latitude"]),
        float(place["longitude"])
    )

# Retrieves weather data for a given ZIP code using Open-Meteo API
# and converts precipitation data into a storm count value
def get_weather_data(zip_code):
    
    coordinates = get_coordinates(zip_code)

    if coordinates is None:
        return {"storm_count": 0}

    lat, lon = coordinates

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&daily=precipitation_sum"
        "&timezone=auto"
    )

    try:
        response = requests.get(url, timeout=10)

        # Handle potential errors in API response
        if response.status_code != 200:
            return {"storm_count": 0}

        data = response.json()

        precipitation_list = data.get("daily", {}).get("precipitation_sum", [])

        # Sum of daily precipitation values returned by Open-Meteo
        precipitation = sum(precipitation_list)

        # Convert total precipitation into an integer value 
        # used by the risk engine
        return {
            "storm_count": round(precipitation)
        }
    
    except (ValueError, KeyError, IndexError):
        return {"storm_count": 0}

    except Exception:
        return {"storm_count": 0}
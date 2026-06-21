"""
Mock Crime Data Service

Uses predefined crime values for selected ZIP codes to demonstrate
how crime data influences the overall risk assessment.

Crime values are intentionally tuned for demonstration and testing
purposes to ensure all risk levels (Low Risk → High Risk) can be
observed during application testing.

This service does not use a live crime API. ZIP codes not listed
below receive a default crime count value.
"""

def get_crime_data(zip_code):

    crime_data = {
        "10001": 5,     # Manhattan
        "30303": 10,    # Atlanta
        "90210": 20,    # Beverly Hills
        "33130": 30,    # Miami
        "60601": 40,    # Chicago
        "90001": 50,    # Los Angeles
        "77084": 75,    # Houston
        "73102": 100,   # Oklahoma City
}

    return {
        "crime_count": crime_data.get(zip_code, 20)
    }
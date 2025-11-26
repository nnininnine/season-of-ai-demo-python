from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import logging
import json

# Initialize FastMCP server
mcp = FastMCP("weather")

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"


async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {"User-Agent": USER_AGENT, "Accept": "application/geo+json"}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None


def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""


@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)


@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # First get the forecast grid endpoint
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch forecast data for this location."

    # Get the forecast URL from the points response
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch detailed forecast."

    # Format the periods into a readable forecast
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # Only show next 5 periods
        forecast = f"""
{period['name']}:
Temperature: {period['temperature']}°{period['temperatureUnit']}
Wind: {period['windSpeed']} {period['windDirection']}
Forecast: {period['detailedForecast']}
"""
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)


@mcp.prompt(title="New York Weather")
def new_york_weather() -> str:
    """
    Get weather forecast and alerts for New York City
    """
    return """
Get the weather forecast for New York City (latitude: 40.7128, longitude: -74.0060) and check for any weather alerts in New York state.
"""


@mcp.prompt(title="Los Angeles Weather")
def los_angeles_weather() -> str:
    """
    Get weather forecast and alerts for Los Angeles
    """
    return """
Get the weather forecast for Los Angeles (latitude: 34.0522, longitude: -118.2437) and check for any weather alerts in California.
"""


@mcp.resource(
    uri="weather://state-codes",
    description="List of US state codes and names for weather alerts",
)
def get_state_codes_resource() -> str:
    """Return JSON describing US state codes usable by the GetAlerts tool."""
    return json.dumps(
        {
            "description": "US State codes for use with GetAlerts tool",
            "states": [
                {"code": "AL", "name": "Alabama"},
                {"code": "AK", "name": "Alaska"},
                {"code": "CA", "name": "California"},
                {"code": "NY", "name": "New York"},
            ],
        }
    )


@mcp.resource(
    uri="weather://majorcities-coords",
    description="Coordinates for major US cities to use with weather forecast",
)
def get_major_cities_resource() -> str:
    """Return JSON with coordinates for a few major US cities."""
    return json.dumps(
        {
            "description": "Pre-defined coordinates for major US cities",
            "cities": [
                {"name": "New York, NY", "latitude": 40.7128, "longitude": -74.0060},
                {
                    "name": "Los Angeles, CA",
                    "latitude": 34.0522,
                    "longitude": -118.2437,
                },
                {"name": "Chicago, IL", "latitude": 41.8781, "longitude": -87.6298},
                {"name": "Houston, TX", "latitude": 29.7604, "longitude": -95.3698},
            ],
        }
    )


def main():
    # Initialize and run the server
    logging.info("Initialize server")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

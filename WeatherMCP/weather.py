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
    # Add tool that return weather alerts for a US state
    return ""


@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    # Add tool that return weather forecast for a location 
    return ""


@mcp.prompt(title="New York Weather")
def new_york_weather() -> str:
    # Add prompt that gets weather forecast and alerts for New York
    return ""


@mcp.prompt(title="Los Angeles Weather")
def los_angeles_weather() -> str:
    # Add prompt that gets weather forecast and alerts for Los Angeles
    return ""


@mcp.resource(
    uri="weather://state-codes",
    description="List of US state codes and names for weather alerts",
)
def get_state_codes_resource() -> str:
    # Add resource that return JSON with US state codes and names
    return ""


@mcp.resource(
    uri="weather://majorcities-coords",
    description="Coordinates for major US cities to use with weather forecast",
)
def get_major_cities_resource() -> str:
    # Add resource that return JSON with major US cities and their coordinates
    return ""


def main():
    # Initialize and run the server
    logging.info("Initialize server")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

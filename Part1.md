# Part 1: Building a Weather MCP Server

In this workshop, you'll build a Model Context Protocol (MCP) server that provides weather information through tools, resources, and prompts.

## Overview

You'll be working with a Python MCP server that integrates with the National Weather Service API to provide weather forecasts and alerts. The implementation uses FastMCP for a streamlined server setup and async HTTP requests.

**Note:** The National Weather Service API only provides data for US locations.

## Step 1: Initialize the FastMCP Server

First, let's set up the MCP server in `WeatherMCP/weather.py`.

**File:** `WeatherMCP/weather.py`

Start by importing the necessary modules and initializing the FastMCP server:

```python
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
```

**What this does:**
- `FastMCP("weather")` - Creates an MCP server instance named "weather"
- Imports `httpx` for async HTTP requests to the National Weather Service API
- Defines constants for API endpoints and headers

## Step 1.1: Add Helper Functions

Add utility functions to handle API requests and format data:

```python
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
```

**What this does:**
- `make_nws_request()` - Handles async HTTP requests with error handling
- `format_alert()` - Formats raw alert data into readable text

## Step 2: Add Weather Tools

Tools are functions that can be called by AI assistants to perform actions.

**File:** `WeatherMCP/weather.py`

1. Add the **get_alerts** tool:

```python
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
```

2. Add the **get_forecast** tool:

```python
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
```

**What this does:**
- `@mcp.tool()` - Decorator marks the function as an MCP tool
- `get_alerts()` - Fetches active weather alerts for a US state
- `get_forecast()` - Fetches a 5-day weather forecast for coordinates
- Async functions enable efficient handling of multiple requests

## Step 2.1: Install Dependencies

Before running the server, install the required dependencies.

### Option 1: Using Virtual Environment (Recommended)

Create and activate a virtual environment:

```bash
# Create virtual environment and activate it
uv venv
source .venv/bin/activate
```

Then install the dependencies:

```bash
uv add "mcp[cli]" httpx
```

### Option 2: Install Dependencies Globally

If you prefer not to use a virtual environment, install directly:

```bash
uv add "mcp[cli]" httpx
```

## Step 2.2: Configure the MCP Server in VS Code

To use your MCP server with GitHub Copilot in VS Code, you need to configure it in the MCP settings file.

1. Create a `.vscode` folder in your project root if it doesn't exist
2. Create a file named `mcp.json` inside the `.vscode` folder
3. Add the following configuration:

```json
{
  "servers": {
    "weather": {
      "command": "${path to your uv}",
      "args": [
        "--directory",
        "./WeatherMCP",
        "run",
        "weather.py"
      ]
    }
  }
}
```

**What this does:**
- Defines an MCP server named "WeatherMCP"
- Configures VS Code to run your server using Python
- Points to your weather.py script

## Step 2.3: Test Your Tools with GitHub Copilot

Now let's test that your tools are working!

1. **Restart the MCP server:**
   - Open `mcp.json` file
   - Click the "Restart" button next to "WeatherMCP"

2. **Open GitHub Copilot Chat** (Ctrl+Shift+I)

3. **Try these test prompts:**
   - "What's the weather forecast for New York City?"
   - "Are there any weather alerts in California?"
   - "Get the weather forecast for Chicago"

4. **Verify the tools are being called:**
   - You should see Copilot using the `get_forecast` and `get_alerts` tools
   - The responses should include actual weather data from the National Weather Service

**Troubleshooting:**
- Check that `.vscode/mcp.json` is properly formatted
- Verify dependencies are installed: `pip list | grep mcp`
- Check the Output panel: View → Output → select "MCP"

### Alternative: Test with MCP Inspector

You can also test your MCP server using the MCP Inspector, which provides a web-based UI to interact with your server.

1. **Run the MCP Inspector:**
   ```bash
   cd WeatherMCP
   uv run mcp dev weather.py
   ```

2. **Open the Inspector:**
   - The command will output a URL (typically `http://localhost:5173`)
   - Open this URL in your browser

3. **Test your tools:**
   - You'll see a visual interface showing your available tools, resources, and prompts
   - Click on the "Tools" tab to see `get_alerts` and `get_forecast`
   - Try calling the tools with different parameters
   - View the JSON responses from the National Weather Service API

**Benefits:**
- Visual debugging interface
- See exact JSON messages
- Test without client configuration

## Step 3: Add Weather Resources

Resources provide static or dynamic data that can be accessed by AI assistants.

**File:** `WeatherMCP/weather.py`

1. Add the **get_state_codes_resource**:

```python
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
```

2. Add the **get_major_cities_resource**:

```python
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
```

**What this does:**
- `@mcp.resource()` - Decorator marks the function as an MCP resource
- `uri` parameter - Defines a unique URI for accessing the resource
- Resources return JSON-serialized data that AI assistants can reference

## Step 3.1: Test Resources in GitHub Copilot

1. **Restart the MCP server:**
   - Open `mcp.json` file
   - Click the "Restart" button next to "WeatherMCP"

2. **Open GitHub Copilot Chat** (Ctrl+Shift+I)

3. **Add resources to your chat context:**
   - Click the **Add Context** icon (paperclip icon) in the chat input
   - Select **MCP Resources**
   - Choose `weather://state-codes` or `weather://majorcities-coords`

4. **Try questions that use the resources:**
   - "What state codes are available for weather alerts?"
   - "Show me the coordinates for major US cities"
   - "What's the weather in one of the major cities you know about?"

5. **Observe:**
   - Copilot can reference the resource data you added
   - It knows the pre-defined state codes and city coordinates

## Step 4: Add Weather Prompts

Prompts are pre-defined templates that help AI assistants perform common tasks.

**File:** `WeatherMCP/weather.py`

1. Add the **new_york_weather** prompt:

```python
@mcp.prompt(title="New York Weather")
def new_york_weather() -> str:
    """
    Get weather forecast and alerts for New York City
    """
    return """
Get the weather forecast for New York City (latitude: 40.7128, longitude: -74.0060) and check for any weather alerts in New York state.
"""
```

2. Add the **los_angeles_weather** prompt:

```python
@mcp.prompt(title="Los Angeles Weather")
def los_angeles_weather() -> str:
    """
    Get weather forecast and alerts for Los Angeles
    """
    return """
Get the weather forecast for Los Angeles (latitude: 34.0522, longitude: -118.2437) and check for any weather alerts in California.
"""
```

**What this does:**
- `@mcp.prompt()` - Decorator marks the function as an MCP prompt
- `title` parameter - Provides a display name for the prompt
- Prompts return strings that provide instructions to AI assistants
- They combine tools and resources to create powerful workflows

## Step 4.1: Run the Server

To run your MCP server, use the following command:

**Command:**

```bash
uv run weather.py
```

The server will start and listen for MCP requests on standard input/output.

## Step 4.2: Test Prompts in GitHub Copilot

1. **Restart the MCP server:**
   - Open `mcp.json` file
   - Click the "Restart" button next to "WeatherMCP"

2. **Open GitHub Copilot Chat** (Ctrl+Shift+I)

3. **Use the prompts:**
   - Type `/` in the chat input to see available prompts
   - Look for:
     - `/New York Weather` - Quick weather check for New York
     - `/Los Angeles Weather` - Quick weather check for Los Angeles

4. **Try the prompts:**
   - Type `/New York Weather` and press Enter
   - Type `/Los Angeles Weather` and press Enter

5. **Verify:**
   - The prompts automatically construct the right queries
   - Copilot uses your tools (`get_forecast` and `get_alerts`) based on the prompt instructions
   - You get comprehensive weather information without typing detailed requests

**What's happening:**
- Prompts provide pre-written instructions that guide Copilot
- They combine with your tools and resources to create powerful, reusable workflows

## Additional Testing Options

Beyond GitHub Copilot, you can test your MCP server in other ways:

1. **MCP Inspector** (covered earlier) - Visual debugging interface
2. **Claude Desktop** - Configure the server in Claude's settings
3. **Other MCP-compatible clients** - Any client that supports the MCP protocol

## Summary

You've successfully created an MCP server with:
- **2 Tools**: `get_alerts` and `get_forecast`
- **2 Resources**: State codes and major cities
- **2 Prompts**: New York weather and Los Angeles weather

These components work together to provide a comprehensive weather information service that AI assistants can use to help users get weather data.

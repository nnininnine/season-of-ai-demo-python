# Part 1: Building a Weather MCP Server

In this workshop, you'll build a Model Context Protocol (MCP) server that provides weather information through tools, resources, and prompts.

## Overview

You'll be working with a .NET MCP server that integrates with the National Weather Service API to provide weather forecasts and alerts. The `WeatherForecastService` class is already implemented and handles the API calls.

**Note:** The National Weather Service API only provides data for US locations.

## Step 1: Register the MCP Server

First, let's register the MCP server in `Program.cs`.

**File:** `WeatherMCP/Program.cs`

Find the comment `// Register MCP server and tools` and add the following code after the `builder.Services.AddSingleton` block:

```csharp
builder.Services.AddMcpServer()
    .WithStdioServerTransport()
    .WithToolsFromAssembly()
    .WithResourcesFromAssembly()
    .WithPromptsFromAssembly();
```

**What this does:**
- `AddMcpServer()` - Registers the MCP server services
- `WithStdioServerTransport()` - Configures the server to communicate via standard input/output
- `WithToolsFromAssembly()` - Auto-discovers and registers tools from the assembly
- `WithResourcesFromAssembly()` - Auto-discovers and registers resources
- `WithPromptsFromAssembly()` - Auto-discovers and registers prompts

## Step 2: Add Weather Tools

Tools are functions that can be called by AI assistants to perform actions.

**File:** `WeatherMCP/WeatherTools.cs`

1. First, add the `[McpServerToolType]` attribute to the `WeatherTools` class:

```csharp
[McpServerToolType]
public static class WeatherTools
{
```

2. Add the **GetAlerts** tool where the first comment indicates:

```csharp
[McpServerTool, Description("Get weather alerts for a US state")]
public static async Task<string> GetAlerts(
    WeatherForecastService service,
    [Description("The US state to get alerts for (e.g., CA, NY, TX).")] string state)
{
    return await service.GetAlerts(state);
}
```

3. Add the **GetForecast** tool where the second comment indicates:

```csharp
[McpServerTool, Description("Get weather forecast for a location.")]
public static async Task<string> GetForecast(
    WeatherForecastService service,
    [Description("Latitude of the location.")] double latitude,
    [Description("Longitude of the location.")] double longitude)
{
    return await service.GetForecast(latitude, longitude);
}
```

**What this does:**
- `[McpServerTool]` - Marks the method as an MCP tool
- `Description` attributes - Provide context to the AI about what the tool does
- The `WeatherForecastService` parameter is automatically injected by dependency injection

## Step 2.1: Build the Project

Build the WeatherMCP project to ensure everything compiles correctly:

```bash
dotnet build WeatherMCP/WeatherMCP.csproj
```

## Step 2.2: Configure the MCP Server in VS Code

To use your MCP server with GitHub Copilot in VS Code, you need to configure it in the MCP settings file.

1. Create a `.vscode` folder in your project root if it doesn't exist
2. Create a file named `mcp.json` inside the `.vscode` folder
3. Add the following configuration:

```json
{
  "servers": {
    "WeatherMCP": {
      "command": "dotnet",
      "args": [
        "run",
        "--project",
        "WeatherMCP/WeatherMCP.csproj",
        "--no-build"
      ]
    }
  }
}
```

**What this does:**
- Defines an MCP server named "WeatherMCP"
- Configures VS Code to run your server using `dotnet run`
- Points to your WeatherMCP project
- Uses `--no-build` to skip rebuilding (since you already built in Step 2.1)

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
   - You should see Copilot using the `GetForecast` and `GetAlerts` tools
   - The responses should include actual weather data from the National Weather Service

**Troubleshooting:**
- Check that `.vscode/mcp.json` is properly formatted
- Verify the project builds: `dotnet build`
- Check the Output panel: View → Output → select "MCP"

### Alternative: Test with MCP Inspector

You can also test your MCP server using the MCP Inspector, which provides a web-based UI to interact with your server.

1. **Run the MCP Inspector:**
   ```powershell
   npx @modelcontextprotocol/inspector dotnet run --project WeatherMCP
   ```

2. **Open the Inspector:**
   - The command will output a URL (typically `http://localhost:5173`)
   - Open this URL in your browser

3. **Test your tools:**
   - You'll see a visual interface showing your available tools, resources, and prompts
   - Click on the "Tools" tab to see `GetAlerts` and `GetForecast`
   - Try calling the tools with different parameters
   - View the JSON responses from the National Weather Service API

**Benefits:**
- Visual debugging interface
- See exact JSON messages
- Test without client configuration

## Step 3: Add Weather Resources

Resources provide static or dynamic data that can be accessed by AI assistants.

**File:** `WeatherMCP/WeatherResources.cs`

1. Add the **GetStateCodesResource** where the first comment indicates:

```csharp
[McpServerResource(UriTemplate = "weather://state-codes")]
[Description("List of US state codes and names for weather alerts")]
public static async Task<string> GetStateCodesResource()
{
    return JsonSerializer.Serialize(new
    {
        description = "US State codes for use with GetAlerts tool",
        states = new[]
        {
            new { code = "AL", name = "Alabama" },
            new { code = "AK", name = "Alaska" },
            new { code = "CA", name = "California" },
            new { code = "NY", name = "New York" },
        }
    });
}
```

2. Add the **GetMajorCitiesResource** where the second comment indicates:

```csharp
[McpServerResource(UriTemplate = "weather://majorcities-coords")]
[Description("Coordinates for major US cities to use with weather forecast")]
public static async Task<string> GetMajorCitiesResource()
{
    return JsonSerializer.Serialize(new
    {
        description = "Pre-defined coordinates for major US cities",
        cities = new[]
        {
            new { name = "New York, NY", latitude = 40.7128, longitude = -74.0060 },
            new { name = "Los Angeles, CA", latitude = 34.0522, longitude = -118.2437 },
            new { name = "Chicago, IL", latitude = 41.8781, longitude = -87.6298 },
            new { name = "Houston, TX", latitude = 29.7604, longitude = -95.3698 }
        }
    });
}
```

**What this does:**
- `[McpServerResource]` - Marks the method as an MCP resource
- `UriTemplate` - Defines a unique URI for accessing the resource
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

**File:** `WeatherMCP/WeatherPrompts.cs`

1. First, add the `[McpServerPromptType]` attribute to the `WeatherPrompts` class:

```csharp
[McpServerPromptType]
public class WeatherPrompts
{
```

2. Add the **NewYorkWeather** prompt:

```csharp
[McpServerPrompt(Name = "NewYorkWeather"), Description("Get weather forecast and alerts for New York City")]
public static string NewYorkWeather()
{
    return "Get the weather forecast for New York City (latitude: 40.7128, longitude: -74.0060) and check for any weather alerts in New York state.";
}
```

3. Add the **LosAngelesWeather** prompt:

```csharp
[McpServerPrompt(Name = "LosAngelesWeather"), Description("Get weather forecast and alerts for Los Angeles")]
public static string LosAngelesWeather()
{
    return "Get the weather forecast for Los Angeles (latitude: 34.0522, longitude: -118.2437) and check for any weather alerts in California.";
}
```

4. Add the **CityWeather** prompt:

```csharp
[McpServerPrompt, Description("Get weather forecast for a given city outside of US, by searching the internet")]
public static string CityWeather(string city)
{
    return $"Get the weather forecast for {city} by searching the internet.";
}
```

**What this does:**
- `[McpServerPrompt]` - Marks the method as an MCP prompt
- Prompts return strings that provide instructions to AI assistants
- Prompts can be parameterized (like `CityWeather`) to make them reusable

## Step 4.1: Test Prompts in GitHub Copilot

1. **Restart the MCP server:**
   - Open `mcp.json` file
   - Click the "Restart" button next to "WeatherMCP"

2. **Open GitHub Copilot Chat** (Ctrl+Shift+I)

3. **Use the prompts:**
   - Type `/` in the chat input to see available prompts
   - Look for:
     - `/NewYorkWeather` - Quick weather check for New York
     - `/LosAngelesWeather` - Quick weather check for Los Angeles
     - `/CityWeather` - Get weather for any city

4. **Try the prompts:**
   - Type `/NewYorkWeather` and press Enter
   - Type `/LosAngelesWeather` and press Enter
   - Type `/CityWeather` followed by a city name (e.g., `/CityWeather Paris`)

5. **Verify:**
   - The prompts automatically construct the right queries
   - Copilot uses your tools (`GetForecast` and `GetAlerts`) based on the prompt instructions
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
- **2 Tools**: `GetAlerts` and `GetForecast`
- **2 Resources**: State codes and major cities
- **3 Prompts**: New York weather, Los Angeles weather, and generic city weather

These components work together to provide a comprehensive weather information service that AI assistants can use to help users get weather data.

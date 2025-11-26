# Part 2: Building a Project Allocation Manager MCP Server

## Introduction

Imagine asking your AI assistant, "Which engineers with frontend skills are available next month?" and getting real-time answers from your actual project management system - not guesses, but live data from your organization's databases.

That's the power of the Model Context Protocol (MCP). MCP servers act as secure bridges, giving AI assistants direct access to your internal systems - databases, APIs, file systems, and more.

In this workshop, you'll build an MCP server for a project allocation system. While we're using JSON files for simplicity, the same patterns apply to any data source: SQL databases, REST APIs etc...

## Demo Video

[Watch this preview to see the Project Allocation Manager MCP in action](allocation-mcp-preview.mp4)

## Overview

**What's already provided:**
- `AllocationService` - Complete service with all business logic, validation and XML documentation
- `Allocation`, `Engineer`, and `Project` models
- Sample data in JSON files
- Basic tool implementations: `ListEngineersTool`, `ListProjectsTool`

**What you'll build:**
- Tools to get individual records by ID
- Tool to allocate and update allocations
- Resources for commonly used data
- Prompts for common allocation tasks

## Getting Started

### Step 1: Understand the Existing Code

1. **Review the models** in `ProjectAllocationManagerMCP/Models/`
2. **Check the sample data** in `ProjectAllocationManagerMCP/data/`
3. **Study the service** in `ProjectAllocationManagerMCP/Services/AllocationService.cs`
   - Read the XML documentation on each method
   - Understand the available methods you can use
4. **Examine existing tools** in `ProjectAllocationManagerMCP/Tools/`

### Step 2: Build the project

Build the ProjectAllocationManagerMCP project to ensure everything compiles correctly:

```bash
dotnet build ProjectAllocationManagerMCP/ProjectAllocationManagerMCP.csproj
```

### Step 3: Configure MCP Server

To use your MCP server with GitHub Copilot in VS Code, configure it in the MCP settings file:

1. Create a `.vscode` folder in your project root if it doesn't exist
2. Create a file named `mcp.json` inside the `.vscode` folder
3. Add the following configuration:

```json
{
  "mcpServers": {
    "ProjectAllocationManagerMCP": {
      "command": "dotnet",
      "args": [
        "run",
        "--project",
        "ProjectAllocationManagerMCP/ProjectAllocationManagerMCP.csproj",
        "--no-build"
      ]
    }
  }
}
```

**What this does:**
- Defines an MCP server named "ProjectAllocationManagerMCP"
- Configures VS Code to run your server using `dotnet run`
- Points to your ProjectAllocationManagerMCP project
- Uses `--no-build` to skip rebuilding (since you already built in Step 2)

### Step 4: Test Existing Tools

Test the provided tools :
- Try listing all engineers
- Try listing all projects

## Exercise Time 🚀

### Task 1: Create tool to retrieve all allocations
**Service method to use:** `GetAllocationsAsync()`

### Task 2: Create tool to retrieve engineers by id
**Service method to use:** `GetEngineerByIdAsync(string id)`

### Task 3: Create tool to retrieve projects by id
**Service method to use:** `GetProjectByIdAsync(string id)`

### Task 4: Create tool to retrieve allocations by id
**Service method to use:** `GetAllocationByIdAsync(string id)`

### Task 5: Create tool to allocate an engineer
**Service method to use:** `AllocateEngineerAsync(string engineerId, string projectId, int allocationPercentage, string? startDate = null, string? endDate = null)`

### Task 6: Create tool to update allocation of an engineer
**Service method to use:** `UpdateAllocationAsync(string allocationId, int? allocationPercentage = null, string? startDate = null, string? endDate = null)`

### Task 7: Add Reference Data Resources

Create resources that provide reference data to AI assistants:

**File to create:**
- `Resources/AllocationResources.cs`

**Resources to implement:**
1. `allocation://engineers` - List all engineers with details
2. `allocation://projects` - List all projects with details

### Task 8: Add Workflow Prompts

Create prompts that guide users through common tasks:

**File to create:**
- `Prompts/AllocationPrompts.cs`

**Prompts to implement:**
1. **AllocateEngineerPrompt** - Guide users to allocate an engineer accepting name, project and start and end date
2. **MoveEngineerToBenchPrompt** - Guide users to move an engineer to the bench (unallocate from current projects)

## Summary

By the end of this workshop, you'll have built:
- **6 Tools** for querying and updating allocations
- **2 Resources** providing reference data
- **2 Prompts** guiding common workflows

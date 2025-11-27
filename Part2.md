# Part 2: Building a Project Allocation Manager MCP Server

## Introduction

Imagine asking your AI assistant, "Which engineers with frontend skills are available next month?" and getting real-time answers from your actual project management system - not guesses, but live data from your organization's databases.

That's the power of the Model Context Protocol (MCP). MCP servers act as secure bridges, giving AI assistants direct access to your internal systems - databases, APIs, file systems, and more.

In this workshop, you'll build a Python MCP server for a project allocation system. While we're using JSON files for simplicity, the same patterns apply to any data source: SQL databases, REST APIs, etc.

## Demo Video

[Watch this preview to see the Project Allocation Manager MCP in action](allocation-mcp-preview.mp4)

## Overview

**What's already provided:**
- `AllocationService` - Complete service with all business logic and validation
- `Allocation`, `Engineer`, and `Project` models
- Sample data in JSON files
- Complete tool implementations: `list_engineers`, `list_projects`

**What you'll build:**
- Tools to get individual records by ID
- Tool to allocate and update allocations
- Resources for commonly used data
- Prompts for common allocation tasks

## Getting Started

### Step 1: Understand the Existing Code

1. **Review the models** in `ProjectAllocationManagerMCP/models/`
2. **Check the sample data** in `ProjectAllocationManagerMCP/data/`
3. **Study the service** in `ProjectAllocationManagerMCP/service/allocation_service.py`
   - Read the docstrings on each method
   - Understand the available methods you can use
4. **Examine existing tools** in `ProjectAllocationManagerMCP/project_mcp/mcp_tools.py`

### Step 2: Install Dependencies

Install the required dependencies:

```bash
cd ProjectAllocationManagerMCP
uv sync
```

Or install manually:

```bash
uv add "mcp[cli]" httpx
```

### Step 3: Configure MCP Server

To use your MCP server with GitHub Copilot in VS Code, configure it in the MCP settings file:

1. Create a `.vscode` folder in your project root if it doesn't exist
2. Create a file named `mcp.json` inside the `.vscode` folder
3. Add the following configuration:

```json
{
  "servers": {
    "ProjectAllocationManagerMCP": {
      "command": "${path to your uv}",
      "args": [
        "--directory",
        "./ProjectAllocationManagerMCP",
        "run",
        "main.py"
      ]
    }
  }
}
```

**What this does:**
- Defines an MCP server named "ProjectAllocationManagerMCP"
- Configures VS Code to run your server using `uv run`
- Points to your ProjectAllocationManagerMCP project
- Runs the `main.py` entry point

### Step 4: Test Existing Tools

Test the provided tools:
- Try listing all engineers: `list_engineers`
- Try listing all projects: `list_projects`

## Exercise Time 🚀

### Task 1: Create tool to retrieve all allocations
**Service method to use:** `get_allocations_async(self)`

### Task 2: Create tool to retrieve engineers by id
**Service method to use:** `get_engineer_by_id_async(self, id: str)`

### Task 3: Create tool to retrieve projects by id
**Service method to use:** `get_project_by_id_async(self, id: str)`

### Task 4: Create tool to retrieve allocations by id
**Service method to use:** `get_allocation_by_id_async(self, id: str)`

### Task 5: Create tool to allocate an engineer
**Service method to use:** `allocate_engineer_async`

### Task 6: Create tool to update allocation of an engineer
**Service method to use:** `update_allocation_async`

### Task 7: Add Reference Data Resources

Create resources that provide reference data to AI assistants:

**File to create:**
- `project_mcp/mcp_resources.py`

**Resources to implement:**
1. `allocation://engineers` - List all engineers with details
2. `allocation://projects` - List all projects with details

### Task 8: Add Workflow Prompts

Create prompts that guide users through common tasks:

**File to create:**
- `project_mcp/mcp_prompts.py`

## Running the Server

To test your MCP server locally:

```bash
cd ProjectAllocationManagerMCP
uv run main.py
```

Or using the MCP Inspector for a web-based UI:

```bash
cd ProjectAllocationManagerMCP
uv run mcp dev main.py
```

## Summary

By the end of this workshop, you'll have built:
- **6 Tools** for querying and updating allocations (pre-built)
- **2 Resources** providing reference data
- **2 Prompts** guiding common workflows

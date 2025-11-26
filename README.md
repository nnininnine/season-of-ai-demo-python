# Season of AI MCP Workshop

Welcome to the Model Context Protocol (MCP) Workshop! This hands-on workshop teaches you how to build MCP servers that connect AI assistants to your internal data and systems.

## Workshop Structure

This workshop consists of two parts, designed to be completed in order:

### Part 1: Weather MCP Server (Follow-Along)

**Type:** Step-by-step guided tutorial

Build a complete MCP server that provides weather information through the National Weather Service API. You'll learn:
- How to create MCP Tools (functions AI assistants can call)
- How to expose Resources (reference data for AI)
- How to define Prompts (workflow templates)
- How to configure and test your MCP server

**[Start Part 1 →](Part1.md)**

### Part 2: Project Allocation Manager (Hands-On Exercise)

**Type:** Self-guided exercises

Apply what you learned by building an MCP server for a project allocation system. You'll implement:
- Tools to query and manage engineer allocations
- Resources for commonly used data
- Prompts for common allocation workflows

The service layer is already built—you'll focus on creating the MCP interface.

**[Start Part 2 →](Part2.md)**

## Prerequisites

- Python 3.10 or later.
- Python MCP SDK 1.2.0 or later.
- Visual Studio Code with GitHub Copilot
- Basic Python knowledge
- Git (for cloning this repository)

## Getting Started

1. **Clone this repository:**
   ```bash
   git clone https://github.com/nnininnine/season-of-ai-demo-python.git
   cd season-of-ai-demo-python
   ```

2. **Complete Part 1 first** - It's essential to understand the fundamentals before moving to Part 2

3. **Then tackle Part 2** - Put your knowledge into practice with hands-on exercises

## What You'll Learn

- **Model Context Protocol (MCP)** - The standard for connecting AI assistants to data sources
- **Tools, Resources, and Prompts** - The three core MCP primitives
- **Real-world patterns** - How to connect AI to databases, APIs, and internal systems
- **Best practices** - Proper tool design, error handling, and testing

## Projects Overview

### WeatherMCP
A complete MCP server demonstrating integration with a public REST API (National Weather Service). Features:
- Weather forecasts by coordinates
- State-level weather alerts
- Pre-configured city data
- Quick-access prompts for major cities

### ProjectAllocationManagerMCP
An MCP server for managing engineer project allocations. Features:
- Complete business logic with validation
- Over-allocation prevention
- Date range handling
- Extensible tool architecture

## Support

If you encounter any issues or have questions during the workshop, please:
- Review the XML documentation in the service classes
- Ask your workshop facilitator

## What's Next?

After completing this workshop, you'll be ready to:
- Build MCP servers for your organization's internal systems
- Connect AI assistants to databases, APIs, and services
- Design effective tools and prompts for common workflows
- Deploy MCP servers in production environments

Happy building! 🚀

from typing import List, Optional
from project_mcp.mcp import mcp
from service.allocation_service import AllocationService
from models.allocation import Allocation
from models.engineer import Engineer
from models.project import Project
from datetime import datetime
import asyncio


# Initialize the allocation service
allocation_service = AllocationService()


# Load data on startup
try:
    asyncio.run(allocation_service.load_data_async())
except RuntimeError:
    # If event loop is already running, create a task instead
    pass


@mcp.tool("list_engineers", description="List all engineers in the system")
async def list_engineers() -> List[dict]:
    """
    List all engineers in the system.

    Returns:
        A list of all engineers.
    """
    engineers = await allocation_service.get_engineers_async()
    return [engineer.to_dict() for engineer in engineers]


@mcp.tool("list_projects", description="List all projects in the system")
async def list_projects() -> List[dict]:
    """
    List all projects in the system.

    Returns:
        A list of all projects.
    """
    projects = await allocation_service.get_projects_async()
    return [project.to_dict() for project in projects]

# Additional tools can be added here following the same pattern.
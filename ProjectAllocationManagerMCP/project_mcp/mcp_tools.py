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


@mcp.tool(
    "allocate_engineer",
    description="Allocate an engineer to a project with a specified percentage and date range",
)
async def allocate_engineer(
    engineer_id: str,
    project_id: str,
    allocation_percentage: int,
    start_date: str | None = None,
    end_date: str | None = None,
) -> dict:
    """
    Allocate an engineer to a project with a specified percentage and date range.

    Args:
        engineer_id: The ID of the engineer to allocate
        project_id: The ID of the project to allocate the engineer to
        allocation_percentage: The allocation percentage (1-100)
        start_date: The start date in YYYY-MM-DD format (optional, defaults to today)
        end_date: The end date in YYYY-MM-DD format (optional, leave empty for indefinite)

    Returns:
        A dictionary with success status, message, and allocation details if successful
    """
    success, message, allocation = await allocation_service.allocate_engineer_async(
        engineer_id, project_id, allocation_percentage, start_date, end_date
    )

    if success:
        return {
            "success": True,
            "message": message,
            "allocation": allocation.to_dict() if allocation else None,
        }
    else:
        return {"success": False, "message": message}


@mcp.tool(
    "get_allocation_by_id", description="Get an allocation by its unique identifier"
)
async def get_allocation_by_id(allocation_id: str) -> Optional[dict]:
    """
    Get an allocation by its unique identifier.

    Args:
        allocation_id: The unique identifier of the allocation.

    Returns:
        An allocation object if found, else None.
    """
    allocation = await allocation_service.get_allocation_by_id_async(allocation_id)
    return allocation.to_dict() if allocation else None


@mcp.tool(
    "get_engineer_by_id", description="Get an engineer by their unique identifier"
)
async def get_engineer_by_id(engineer_id: str) -> Optional[dict]:
    """
    Get an engineer by their unique identifier.

    Args:
        engineer_id: The unique identifier of the engineer.

    Returns:
        An engineer object if found, else None.
    """
    engineer = await allocation_service.get_engineer_by_id_async(engineer_id)
    return engineer.to_dict() if engineer else None


@mcp.tool("get_project_by_id", description="Get a project by its unique identifier")
async def get_project_by_id(project_id: str) -> Optional[dict]:
    """
    Get a project by its unique identifier.

    Args:
        project_id: The unique identifier of the project.

    Returns:
        A project object if found, else None.
    """
    project = await allocation_service.get_project_by_id_async(project_id)
    return project.to_dict() if project else None


@mcp.tool(
    "list_allocations",
    description="List all active allocations in the system (allocations that are currently ongoing)",
)
async def list_allocations() -> List[dict]:
    """
    List all active allocations in the system (allocations that are currently ongoing).

    Returns:
        A dictionary with success status, message, and a list of active allocations.
    """
    all_allocations = await allocation_service.get_allocations_async()
    today = datetime.now()
    active_allocations = [
        alloc for alloc in all_allocations if alloc.is_active(on_date=today)
    ]
    return [alloc.to_dict() for alloc in active_allocations]


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


@mcp.tool(
    "update_allocation",
    description="Update an existing allocation with new percentage and/or date range. All parameters except allocationId are optional.",
)
async def update_allocation(
    allocation_id: str,
    allocation_percentage: int | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
) -> dict:
    """
    Update an existing allocation with new percentage and/or date range.

    Args:
        allocation_id: The ID of the allocation to update
        allocation_percentage: The new allocation percentage (1-100) (optional)
        start_date: The new start date in YYYY-MM-DD format (optional)
        end_date: The new end date in YYYY-MM-DD format (optional)

    Returns:
        A dictionary with success status, message, and updated allocation details if successful
    """
    success, message, allocation = await allocation_service.update_allocation_async(
        allocation_id, allocation_percentage, start_date, end_date
    )

    if success:
        return {
            "success": True,
            "message": message,
            "allocation": allocation.to_dict() if allocation else None,
        }
    else:
        return {"success": False, "message": message}

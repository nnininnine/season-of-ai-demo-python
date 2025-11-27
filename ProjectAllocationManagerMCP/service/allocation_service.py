import json
import os
import uuid
from datetime import datetime
from typing import List, Optional, Tuple
from models.allocation import Allocation
from models.engineer import Engineer
from models.project import Project


class AllocationService:
    """
    Service for managing engineer allocations to projects.

    Handles allocation logic including validation, conflict detection,
    and data persistence.
    """

    def __init__(self, data_folder: Optional[str] = None):
        """
        Initialize the AllocationService with an optional custom data folder path.

        Args:
            data_folder: Optional path to the data folder. If not provided,
                        defaults to 'data' folder in the current directory.
        """
        if data_folder is None:
            self.data_folder = os.path.join(os.getcwd(), "data")
        else:
            self.data_folder = data_folder

        self._engineers: List[Engineer] = []
        self._projects: List[Project] = []
        self._allocations: List[Allocation] = []

    async def get_engineers_async(self) -> List[Engineer]:
        """
        Retrieve all engineers in the system.

        Returns:
            A list of all engineers.
        """
        return self._engineers

    async def get_projects_async(self) -> List[Project]:
        """
        Retrieve all projects in the system.

        Returns:
            A list of all projects.
        """
        return self._projects

    async def get_allocations_async(self) -> List[Allocation]:
        """
        Retrieve all allocations in the system.

        Returns:
            A list of all allocations.
        """
        return self._allocations

    async def get_engineer_by_id_async(self, id: str) -> Optional[Engineer]:
        """
        Retrieve an engineer by their unique identifier.

        Args:
            id: The unique identifier of the engineer.

        Returns:
            The engineer if found, otherwise None.
        """
        for engineer in self._engineers:
            if engineer.id == id:
                return engineer
        return None

    async def get_project_by_id_async(self, id: str) -> Optional[Project]:
        """
        Retrieve a project by its unique identifier.

        Args:
            id: The unique identifier of the project.

        Returns:
            The project if found, otherwise None.
        """
        for project in self._projects:
            if project.id == id:
                return project
        return None

    async def get_allocation_by_id_async(self, id: str) -> Optional[Allocation]:
        """
        Retrieve an allocation by its unique identifier.

        Args:
            id: The unique identifier of the allocation.

        Returns:
            The allocation if found, otherwise None.
        """
        for allocation in self._allocations:
            if allocation.id == id:
                return allocation
        return None

    async def get_allocations_by_engineer_id_async(
        self, engineer_id: str
    ) -> List[Allocation]:
        """
        Retrieve all allocations for a specific engineer.

        Args:
            engineer_id: The unique identifier of the engineer.

        Returns:
            A list of allocations for the specified engineer.
        """
        return [a for a in self._allocations if a.engineer_id == engineer_id]

    async def get_allocations_by_project_id_async(
        self, project_id: str
    ) -> List[Allocation]:
        """
        Retrieve all allocations for a specific project.

        Args:
            project_id: The unique identifier of the project.

        Returns:
            A list of allocations for the specified project.
        """
        return [a for a in self._allocations if a.project_id == project_id]

    async def allocate_engineer_async(
        self,
        engineer_id: str,
        project_id: str,
        allocation_percentage: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Tuple[bool, str, Optional[Allocation]]:
        """
        Allocate an engineer to a project with specified percentage and date range.

        Validates that the engineer and project exist, the allocation percentage is valid (1-100),
        and the engineer won't be over-allocated (total allocations don't exceed 100%).

        Args:
            engineer_id: The unique identifier of the engineer to allocate.
            project_id: The unique identifier of the project.
            allocation_percentage: The percentage of time allocated (1-100).
            start_date: Optional start date in YYYY-MM-DD format. Defaults to today if not provided.
            end_date: Optional end date in YYYY-MM-DD format. Leave empty for indefinite allocation.

        Returns:
            A tuple containing (success, message, allocation).
        """
        # Validation 1: Check if engineer exists
        engineer = await self.get_engineer_by_id_async(engineer_id)
        if engineer is None:
            return (False, f"Engineer with ID '{engineer_id}' not found.", None)

        # Validation 2: Check if project exists
        project = await self.get_project_by_id_async(project_id)
        if project is None:
            return (False, f"Project with ID '{project_id}' not found.", None)

        # Validation 3: Validate allocation percentage (must be between 1 and 100)
        if allocation_percentage < 1 or allocation_percentage > 100:
            return (False, "Allocation percentage must be between 1 and 100.", None)

        # Validation 4: Validate and set dates
        if not start_date or start_date.strip() == "":
            parsed_start_date = datetime.today()
        else:
            try:
                parsed_start_date = datetime.strptime(start_date, "%Y-%m-%d")
            except ValueError:
                return (False, f"Invalid start date format: '{start_date}'.", None)

        # End date is optional for indefinite assignments
        parsed_end_date: Optional[datetime] = None
        if end_date and end_date.strip() != "":
            try:
                parsed_end_date = datetime.strptime(end_date, "%Y-%m-%d")
            except ValueError:
                return (False, f"Invalid end date format: '{end_date}'.", None)

            if parsed_end_date <= parsed_start_date:
                return (False, "End date must be after start date.", None)

        # Validation 5: Check for overlapping allocations and total percentage
        existing_allocations = await self.get_allocations_by_engineer_id_async(
            engineer_id
        )
        overlapping_allocations = self._get_overlapping_allocations(
            existing_allocations, parsed_start_date, parsed_end_date
        )

        if overlapping_allocations:
            total_allocation = (
                sum(a.allocation_percentage for a in overlapping_allocations)
                + allocation_percentage
            )
            if total_allocation > 100:
                current_total = sum(
                    a.allocation_percentage for a in overlapping_allocations
                )
                return (
                    False,
                    f"Engineer '{engineer.name}' is over-allocated. "
                    f"Current allocation during this period: {current_total}%. "
                    f"Adding {allocation_percentage}% would result in {total_allocation}% total allocation.",
                    None,
                )

        # Validation 6: Check if engineer is already allocated to the same project with overlapping dates
        duplicate_allocation = next(
            (a for a in overlapping_allocations if a.project_id == project_id), None
        )
        if duplicate_allocation is not None:
            end_date_str = (
                duplicate_allocation.end_date.strftime("%Y-%m-%d")
                if duplicate_allocation.end_date
                else "indefinite"
            )
            return (
                False,
                f"Engineer '{engineer.name}' is already allocated to project '{project.name}' "
                f"from {duplicate_allocation.start_date.strftime('%Y-%m-%d')} to {end_date_str}.",
                None,
            )

        # Create new allocation
        new_allocation = Allocation(
            id=f"alloc-{str(uuid.uuid4())[:8]}",
            engineer_id=engineer_id,
            project_id=project_id,
            allocation_percentage=allocation_percentage,
            start_date=parsed_start_date,
            end_date=parsed_end_date,
        )

        self._allocations.append(new_allocation)

        if parsed_end_date is None:
            message = (
                f"Successfully allocated {allocation_percentage}% of {engineer.name} to {project.name} "
                f"starting from {parsed_start_date.strftime('%Y-%m-%d')} (indefinite)."
            )
        else:
            message = (
                f"Successfully allocated {allocation_percentage}% of {engineer.name} to {project.name} "
                f"from {parsed_start_date.strftime('%Y-%m-%d')} to {parsed_end_date.strftime('%Y-%m-%d')}."
            )

        return (True, message, new_allocation)

    async def update_allocation_async(
        self,
        allocation_id: str,
        allocation_percentage: Optional[int] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Tuple[bool, str, Optional[Allocation]]:
        """
        Update an existing allocation with new percentage and/or date range.

        All update parameters are optional - only provided values will be updated.
        Validates that the allocation exists, dates are valid, and the engineer won't be over-allocated.

        Args:
            allocation_id: The unique identifier of the allocation to update.
            allocation_percentage: Optional new allocation percentage (1-100).
            start_date: Optional new start date in YYYY-MM-DD format.
            end_date: Optional new end date in YYYY-MM-DD format.

        Returns:
            A tuple containing (success, message, allocation).
        """
        # Validation 1: Find the allocation
        allocation = await self.get_allocation_by_id_async(allocation_id)
        if allocation is None:
            return (False, f"Allocation with ID '{allocation_id}' not found.", None)

        # Get engineer and project details for validation and messaging
        engineer = await self.get_engineer_by_id_async(allocation.engineer_id)
        project = await self.get_project_by_id_async(allocation.project_id)

        if engineer is None or project is None:
            return (False, "Associated engineer or project not found.", None)

        # Parse and validate new dates
        parsed_start_date = allocation.start_date
        parsed_end_date = allocation.end_date

        if start_date and start_date.strip() != "":
            try:
                parsed_start_date = datetime.strptime(start_date, "%Y-%m-%d")
            except ValueError:
                return (False, f"Invalid start date format: '{start_date}'.", None)

        if end_date and end_date.strip() != "":
            try:
                parsed_end_date = datetime.strptime(end_date, "%Y-%m-%d")
            except ValueError:
                return (False, f"Invalid end date format: '{end_date}'.", None)

        # Validate end date is after start date
        if parsed_end_date is not None and parsed_end_date <= parsed_start_date:
            return (False, "End date must be after start date.", None)

        # Validate allocation percentage if provided
        new_allocation_percentage = allocation.allocation_percentage
        if allocation_percentage is not None:
            if allocation_percentage < 1 or allocation_percentage > 100:
                return (False, "Allocation percentage must be between 1 and 100.", None)
            new_allocation_percentage = allocation_percentage

        # Check for overlapping allocations (excluding the current allocation being updated)
        existing_allocations = await self.get_allocations_by_engineer_id_async(
            allocation.engineer_id
        )
        existing_allocations = [
            a for a in existing_allocations if a.id != allocation_id
        ]

        overlapping_allocations = self._get_overlapping_allocations(
            existing_allocations, parsed_start_date, parsed_end_date
        )

        if overlapping_allocations:
            total_allocation = (
                sum(a.allocation_percentage for a in overlapping_allocations)
                + new_allocation_percentage
            )
            if total_allocation > 100:
                current_total = sum(
                    a.allocation_percentage for a in overlapping_allocations
                )
                return (
                    False,
                    f"Engineer '{engineer.name}' would be over-allocated. "
                    f"Current allocation during this period: {current_total}%. "
                    f"Adding {new_allocation_percentage}% would result in {total_allocation}% total allocation.",
                    None,
                )

        # Check for duplicate allocation to the same project (excluding current allocation)
        duplicate_allocation = next(
            (
                a
                for a in overlapping_allocations
                if a.project_id == allocation.project_id
            ),
            None,
        )
        if duplicate_allocation is not None:
            end_date_str = (
                duplicate_allocation.end_date.strftime("%Y-%m-%d")
                if duplicate_allocation.end_date
                else "indefinite"
            )
            return (
                False,
                f"Engineer '{engineer.name}' is already allocated to project '{project.name}' "
                f"from {duplicate_allocation.start_date.strftime('%Y-%m-%d')} to {end_date_str} in allocation '{duplicate_allocation.id}'.",
                None,
            )

        # Update the allocation
        allocation.allocation_percentage = new_allocation_percentage
        allocation.start_date = parsed_start_date
        allocation.end_date = parsed_end_date

        if parsed_end_date is None:
            message = (
                f"Successfully updated allocation. {engineer.name} is now {new_allocation_percentage}% allocated to {project.name} "
                f"starting from {parsed_start_date.strftime('%Y-%m-%d')} (indefinite)."
            )
        else:
            message = (
                f"Successfully updated allocation. {engineer.name} is now {new_allocation_percentage}% allocated to {project.name} "
                f"from {parsed_start_date.strftime('%Y-%m-%d')} to {parsed_end_date.strftime('%Y-%m-%d')}."
            )

        return (True, message, allocation)

    async def load_data_async(self) -> None:
        """
        Load engineers, projects, and allocations data from JSON files in the data folder.

        If the data folder doesn't exist, it will be created.
        Uses case-insensitive property matching for deserialization.
        """
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)
            return

        # Load Engineers
        engineers_path = os.path.join(self.data_folder, "engineers.json")
        if os.path.exists(engineers_path):
            try:
                with open(engineers_path, "r") as f:
                    engineers_data = json.load(f)
                    for eng_dict in engineers_data:
                        engineer = Engineer(**eng_dict)
                        self._engineers.append(engineer)
            except Exception as e:
                print(f"Error loading engineers: {e}")

        # Load Projects
        projects_path = os.path.join(self.data_folder, "projects.json")
        if os.path.exists(projects_path):
            try:
                with open(projects_path, "r") as f:
                    projects_data = json.load(f)
                    for proj_dict in projects_data:
                        project = Project(**proj_dict)
                        self._projects.append(project)
            except Exception as e:
                print(f"Error loading projects: {e}")

        # Load Allocations
        allocations_path = os.path.join(self.data_folder, "allocations.json")
        if os.path.exists(allocations_path):
            try:
                with open(allocations_path, "r") as f:
                    allocations_data = json.load(f)
                    for alloc_dict in allocations_data:
                        # Convert date strings to datetime objects
                        start_date = datetime.strptime(
                            alloc_dict.get("startDate"), "%Y-%m-%dT%H:%M:%S"
                        )
                        end_date_str = alloc_dict.get("endDate")
                        end_date = (
                            datetime.strptime(end_date_str, "%Y-%m-%dT%H:%M:%S")
                            if end_date_str
                            else None
                        )

                        allocation = Allocation(
                            id=alloc_dict.get("id"),
                            engineer_id=alloc_dict.get("engineerId"),
                            project_id=alloc_dict.get("projectId"),
                            allocation_percentage=alloc_dict.get(
                                "allocationPercentage"
                            ),
                            start_date=start_date,
                            end_date=end_date,
                        )
                        self._allocations.append(allocation)
            except Exception as e:
                print(f"Error loading allocations: {e}")

    def _get_overlapping_allocations(
        self,
        allocations: List[Allocation],
        new_start: datetime,
        new_end: Optional[datetime],
    ) -> List[Allocation]:
        """
        Helper method to find allocations that overlap with the given date range.

        Args:
            allocations: List of allocations to check.
            new_start: Start date of the new allocation.
            new_end: End date of the new allocation (None for indefinite).

        Returns:
            List of overlapping allocations.
        """
        overlapping = []

        for alloc in allocations:
            existing_start = alloc.start_date
            existing_end = alloc.end_date

            # Check if date ranges overlap
            # Case 1: Both have end dates
            if new_end is not None and existing_end is not None:
                if new_start < existing_end and new_end > existing_start:
                    overlapping.append(alloc)
            # Case 2: New allocation is indefinite
            elif new_end is None and existing_end is not None:
                if new_start < existing_end:
                    overlapping.append(alloc)
            # Case 3: Existing allocation is indefinite
            elif new_end is not None and existing_end is None:
                if new_end > existing_start:
                    overlapping.append(alloc)
            # Case 4: Both are indefinite
            else:
                overlapping.append(alloc)

        return overlapping

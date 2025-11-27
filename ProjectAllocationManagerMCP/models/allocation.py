from datetime import datetime
from typing import Optional


class Allocation:
    """Represents an allocation of an engineer to a project."""

    def __init__(
        self,
        id: str,
        engineer_id: str,
        project_id: str,
        allocation_percentage: int,
        start_date: datetime,
        end_date: Optional[datetime] = None,
    ):
        self.id = id
        self.engineer_id = engineer_id
        self.project_id = project_id
        self.allocation_percentage = allocation_percentage
        self.start_date = start_date
        self.end_date = end_date
        
    def is_active(self, on_date: datetime) -> bool:
        """Check if the allocation is active on the given date."""
        if self.end_date:
            return self.start_date <= on_date <= self.end_date
        return self.start_date <= on_date

    def to_dict(self) -> dict:
        """Convert allocation to dictionary."""
        return {
            "id": self.id,
            "engineerId": self.engineer_id,
            "projectId": self.project_id,
            "allocationPercentage": self.allocation_percentage,
            "startDate": self.start_date.strftime("%Y-%m-%d"),
            "endDate": self.end_date.strftime("%Y-%m-%d") if self.end_date else None,
        }

class Project:
    """Represents a project in the system."""

    def __init__(self, id: str, name: str, **kwargs):
        self.id = id
        self.name = name
        # Store any additional attributes
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_dict(self) -> dict:
        """Convert project to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            **{k: v for k, v in self.__dict__.items() if k not in ['id', 'name']}
        }
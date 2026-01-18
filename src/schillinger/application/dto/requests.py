"""
Application Layer - DTOs (Data Transfer Objects)
Request and response objects for use cases.
"""

from dataclasses import dataclass
from typing import Optional
from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ...domain.rhythm.entities import RhythmPattern

@dataclass
class GenerateRhythmRequest:
    """Request DTO for rhythm generation."""
    major_generator: int
    minor_generator: int
    rhythm_type: str = "binary_sync"  # "binary_sync" or "fractioning"
    time_signature: str = "4/4"  # String format like "4/4"

    def __post_init__(self):
        if self.rhythm_type not in ["binary_sync", "fractioning"]:
            raise ValueError(f"Invalid rhythm type: {self.rhythm_type}")


@dataclass
class RhythmResponse:
    """Response DTO for rhythm generation."""
    rhythm_pattern: Optional['RhythmPattern'] = None  # Forward reference to avoid circular import
    notation_path: Optional[str] = None
    error_message: Optional[str] = None

    @property
    def success(self) -> bool:
        return self.error_message is None
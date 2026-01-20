"""
Domain Layer - Rhythm Subdomain
Core business logic for rhythm generation using Schillinger theory.
"""

from dataclasses import dataclass, field
from typing import List, Optional
class DomainError(Exception):
    """Base class for all domain-related errors."""
    pass


@dataclass(frozen=True)
class Generator:
    """Value Object: Represents a rhythm generator in Schillinger theory."""
    value: int

    def __post_init__(self):
        if not isinstance(self.value, int) or self.value < 1:
            raise DomainError(f"Generator must be a positive integer, got {self.value}")


@dataclass(frozen=True)
class TimeSignature:
    """Value Object: Represents a musical time signature."""
    numerator: int
    denominator: int

    def __post_init__(self):
        if not isinstance(self.numerator, int) or self.numerator < 1:
            raise DomainError(f"Time signature numerator must be positive integer, got {self.numerator}")
        if not isinstance(self.denominator, int) or self.denominator < 1:
            raise DomainError(f"Time signature denominator must be positive integer, got {self.denominator}")
        # Common denominators: 2, 4, 8, 16, 32
        valid_denominators = [2, 4, 8, 16, 32]
        if self.denominator not in valid_denominators:
            raise DomainError(f"Time signature denominator must be one of {valid_denominators}, got {self.denominator}")

    def to_string(self) -> str:
        return f"{self.numerator}/{self.denominator}"

    @classmethod
    def from_string(cls, time_sig_str: str) -> 'TimeSignature':
        """Create TimeSignature from string like '4/4' or '3/4'."""
        try:
            num, den = map(int, time_sig_str.split('/'))
            return cls(numerator=num, denominator=den)
        except (ValueError, TypeError):
            raise DomainError(f"Invalid time signature format: {time_sig_str}. Expected format: '4/4'")


@dataclass(frozen=True)
class RhythmSequence:
    """Value Object: Represents a sequence of beats and rests."""
    beats: List[int]  # 1 for beat, 0 for rest

    def __post_init__(self):
        if not self.beats:
            raise DomainError("Rhythm sequence cannot be empty")
        if not all(isinstance(beat, int) and beat in (0, 1) for beat in self.beats):
            raise DomainError("Rhythm sequence must contain only 0s and 1s")

    def to_durations(self) -> List[int]:
        """
        Convert binary rhythm to note durations.
        Example: [1, 0, 1, 1, 1, 0] -> [2, 1, 1, 2]
        """
        if not self.beats:
            return []

        result = []
        i = 0
        while i < len(self.beats):
            if self.beats[i] == 1:
                count = 1
                # Count consecutive zeros after this beat
                while i + count < len(self.beats) and self.beats[i + count] == 0:
                    count += 1
                result.append(count)
                i += count
            else:
                i += 1  # Skip initial rests

        return result


@dataclass(frozen=True)
class RhythmPattern:
    """Value Object: A complete rhythm pattern with metadata."""
    sequence: RhythmSequence
    time_signature: TimeSignature
    generator_a: Optional[Generator] = None
    generator_b: Optional[Generator] = None
    rhythm_type: str = "binary_sync"  # "binary_sync" or "fractioning"

    def __post_init__(self):
        valid_types = ["binary_sync", "fractioning"]
        if self.rhythm_type not in valid_types:
            raise DomainError(f"Rhythm type must be one of {valid_types}, got {self.rhythm_type}")

    @property
    def durations(self) -> List[int]:
        """Get the note durations for this rhythm."""
        return self.sequence.to_durations()

    def get_total_beats(self) -> int:
        """Get the total number of beats in this rhythm."""
        return len(self.sequence.beats)

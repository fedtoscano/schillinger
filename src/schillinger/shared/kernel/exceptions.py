"""
Shared Kernel - Domain Exceptions
Cross-cutting concerns and shared domain concepts.
"""

from typing import Any


class InvalidGeneratorError(Exception):
    """Raised when a generator value is invalid."""
    pass


class InvalidRhythmError(Exception):
    """Raised when a rhythm pattern is invalid."""
    pass


class CompositionError(Exception):
    """Raised when a composition operation fails."""
    pass


class RhythmGenerationError(Exception):
    """Raised when rhythm generation fails."""
    pass
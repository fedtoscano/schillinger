"""
Application Layer - Use Cases
Business logic orchestration using domain services and infrastructure.
"""

from typing import Protocol, TYPE_CHECKING
from ..dto.requests import GenerateRhythmRequest, RhythmResponse
from ...domain.rhythm.entities import Generator, TimeSignature
from ...domain.rhythm.services import RhythmGenerator

if TYPE_CHECKING:
    from ...domain.rhythm.entities import RhythmPattern


class RhythmRenderer(Protocol):
    """Interface for rhythm rendering (infrastructure concern)."""
    def render_to_png(self, rhythm: 'RhythmPattern') -> str:
        """Render rhythm to PNG file and return path."""
        ...


class GenerateRhythmUseCase:
    """
    Use Case: Generate a rhythm and prepare it for display.

    This orchestrates the domain logic and coordinates with infrastructure
    services to provide a complete rhythm generation workflow.
    """

    def __init__(self, rhythm_generator: RhythmGenerator, renderer: RhythmRenderer):
        self.rhythm_generator = rhythm_generator
        self.renderer = renderer

    def execute(self, request: GenerateRhythmRequest) -> RhythmResponse:
        """
        Execute the rhythm generation use case.

        Args:
            request: The generation request with parameters

        Returns:
            RhythmResponse: The result of the generation
        """
        try:
            # Convert request data to domain objects
            major_gen = Generator(request.major_generator)
            minor_gen = Generator(request.minor_generator)
            time_sig = TimeSignature.from_string(request.time_signature)

            # Generate rhythm using domain service
            if request.rhythm_type == "binary_sync":
                rhythm_pattern = self.rhythm_generator.generate_binary_sync(
                    major_gen, minor_gen, time_sig
                )
            elif request.rhythm_type == "fractioning":
                rhythm_pattern = self.rhythm_generator.generate_fractioning(
                    major_gen, minor_gen, time_sig
                )
            else:
                raise ValueError(f"Unknown rhythm type: {request.rhythm_type}")

            # Render to notation (infrastructure concern)
            notation_path = self.renderer.render_to_png(rhythm_pattern)

            return RhythmResponse(
                rhythm_pattern=rhythm_pattern,
                notation_path=notation_path
            )

        except Exception as e:
            # Return error response
            return RhythmResponse(
                error_message=str(e)
            )
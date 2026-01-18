"""
Infrastructure Layer - Dependency Injection Container
Centralized dependency management for the application.
"""

from dependency_injector import containers, providers

from ...domain.rhythm.services import RhythmGenerator
from ...application.use_cases.generate_rhythm import GenerateRhythmUseCase
from ...infrastructure.config.settings import Settings
from ...infrastructure.external.music21.renderer import Music21RhythmRenderer


class Container(containers.DeclarativeContainer):
    """Dependency injection container for the Schillinger application."""

    # Configuration
    config = providers.Singleton(Settings)

    # Domain Services
    rhythm_generator = providers.Singleton(RhythmGenerator)

    # Infrastructure Services
    rhythm_renderer = providers.Singleton(
        Music21RhythmRenderer,
        output_dir=config.provided.storage.output,
        lilypond_path=config.provided.lilypond.path
    )

    # Application Services (Use Cases)
    generate_rhythm_use_case = providers.Singleton(
        GenerateRhythmUseCase,
        rhythm_generator=rhythm_generator,
        renderer=rhythm_renderer
    )
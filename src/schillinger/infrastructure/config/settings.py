"""
Infrastructure Layer - Configuration
Application settings and environment management.
"""

import os
from pathlib import Path
from typing import Optional


class Settings:
    """Application settings with environment-specific values."""

    def __init__(self):
        # Core settings
        self.app_name = "Schillinger System"
        self.version = "0.1.0"

        # Paths
        self.project_root = Path(__file__).parent.parent.parent.parent
        self.output_dir = self.project_root / "output"
        self.compositions_dir = self.project_root / "compositions"

        # External tools
        self.lilypond_path = os.getenv('LILYPOND_PATH')

        # UI settings
        self.default_window_size = (800, 600)
        self.default_time_signature = "4/4"

        # Ensure directories exist
        self.output_dir.mkdir(exist_ok=True)
        self.compositions_dir.mkdir(exist_ok=True)

    @property
    def storage(self):
        """Storage-related settings."""
        class Storage:
            compositions = str(self.compositions_dir)
            output = str(self.output_dir)
        return Storage()

    @property
    def lilypond(self):
        """LilyPond-related settings."""
        class LilyPond:
            path = self.lilypond_path
        return LilyPond()
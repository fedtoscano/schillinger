"""
Infrastructure Layer - Music21 Adapters
Adapters for the music21 external library.
"""

import os
import subprocess
from pathlib import Path
from typing import Optional
import lilypond
import cairosvg
from music21.stream import Stream
from music21.note import Note
from music21.meter.base import TimeSignature as Music21TimeSignature
from music21 import environment

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ....domain.rhythm.entities import RhythmPattern


class Music21RhythmRenderer:
    """
    Infrastructure Adapter: Converts domain RhythmPattern to PNG using music21/LilyPond.

    This handles all external dependencies for rhythm rendering.
    """

    def __init__(self, output_dir: str = "output", lilypond_path: Optional[str] = None):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Configure music21
        env = environment.Environment()
        if lilypond_path:
            env['lilypondPath'] = lilypond_path
        else:
            # Use the bundled lilypond
            env['lilypondPath'] = str(lilypond.executable())

    def render_to_png(self, rhythm) -> str:
        """
        Render a RhythmPattern to PNG using music21 and LilyPond.

        Args:
            rhythm: Domain rhythm pattern to render

        Returns:
            str: Path to the generated PNG file

        Raises:
            RenderingError: If rendering fails
        """
        try:
            # Convert domain objects to music21 objects
            stream = self._create_music21_stream(rhythm)

            # Generate output paths
            base_name = f"rhythm_{id(rhythm)}"  # Use object id for uniqueness
            ly_path = self.output_dir / f"{base_name}.ly"
            svg_path = self.output_dir / f"{base_name}.svg"
            png_path = self.output_dir / f"{base_name}.png"

            # Generate LilyPond file
            stream.write('lilypond', fp=str(ly_path))

            # Fix version in generated .ly file
            self._fix_lilypond_version(ly_path)

            # Convert .ly to .svg
            self._convert_ly_to_svg(ly_path, svg_path)

            # Convert .svg to .png
            self._convert_svg_to_png(svg_path, png_path)

            return str(png_path)

        except Exception as e:
            raise RenderingError(f"Failed to render rhythm: {e}") from e

    def _create_music21_stream(self, rhythm: 'RhythmPattern') -> Stream:
        """Convert RhythmPattern to music21 Stream."""
        stream = Stream()

        # Add time signature
        ts = Music21TimeSignature(f"{rhythm.time_signature.numerator}/{rhythm.time_signature.denominator}")
        stream.append(ts)

        # Add notes based on durations
        for duration in rhythm.durations:
            note = Note()
            note.duration.quarterLength = duration
            stream.append(note)

        return stream

    def _fix_lilypond_version(self, ly_path: Path) -> None:
        """Fix the LilyPond version in the generated .ly file."""
        content = ly_path.read_text()
        content = content.replace('\\version "2.25"', '\\version "2.25.12"')
        ly_path.write_text(content)

    def _convert_ly_to_svg(self, ly_path: Path, svg_path: Path) -> None:
        """Convert LilyPond file to SVG."""
        result = subprocess.run([
            str(lilypond.executable()),
            '-dbackend=svg',
            '-o', str(svg_path.with_suffix('')),  # Remove .svg extension for lilypond
            str(ly_path)
        ], check=True, capture_output=True, text=True)

        if result.returncode != 0:
            raise RenderingError(f"LilyPond conversion failed: {result.stderr}")

    def _convert_svg_to_png(self, svg_path: Path, png_path: Path) -> None:
        """Convert SVG to PNG."""
        cairosvg.svg2png(
            url=str(svg_path),
            write_to=str(png_path)
        )


class RenderingError(Exception):
    """Raised when rhythm rendering fails."""
    pass
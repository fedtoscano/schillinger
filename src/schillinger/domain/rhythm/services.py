"""
Domain Layer - Rhythm Services
Domain services for rhythm generation using Schillinger theory.
"""

from typing import List, Optional
from .entities import Generator, RhythmPattern, RhythmSequence, TimeSignature
from ...shared.kernel.exceptions import RhythmGenerationError


class RhythmGenerator:
    """
    Domain Service: Core rhythm generation logic using Schillinger theory.

    This service contains the pure business logic for generating rhythms,
    without any external dependencies.
    """

    def generate_binary_sync(self, major: Generator, minor: Generator,
                           time_signature: Optional[TimeSignature] = None) -> RhythmPattern:
        """
        Generate a binary synchronization rhythm pattern.

        Args:
            major: Major generator (a)
            minor: Minor generator (b)
            time_signature: Time signature for the rhythm

        Returns:
            RhythmPattern: Generated rhythm pattern

        Raises:
            RhythmGenerationError: If generation fails
        """
        if time_signature is None:
            time_signature = TimeSignature(4, 4)  # Default 4/4

        try:
            # Generate the common period (least common multiple)
            common_period = major.value * minor.value

            # Generate individual rhythm strings
            major_rhythm = self._generate_rhythm_string(major.value, common_period)
            minor_rhythm = self._generate_rhythm_string(minor.value, common_period)

            # Merge rhythms (OR operation)
            merged_rhythm = self._merge_rhythms([major_rhythm, minor_rhythm])

            # Create domain objects
            sequence = RhythmSequence(beats=merged_rhythm)

            return RhythmPattern(
                sequence=sequence,
                time_signature=time_signature,
                generator_a=major,
                generator_b=minor,
                rhythm_type="binary_sync"
            )

        except Exception as e:
            raise RhythmGenerationError(f"Failed to generate binary sync rhythm: {e}") from e

    def generate_fractioning(self, major: Generator, minor: Generator,
                           time_signature: Optional[TimeSignature] = None) -> RhythmPattern:
        """
        Generate a double fractioning rhythm pattern.

        Args:
            major: Major generator (a)
            minor: Minor generator (b)
            time_signature: Time signature for the rhythm

        Returns:
            RhythmPattern: Generated rhythm pattern

        Raises:
            RhythmGenerationError: If generation fails
        """
        if time_signature is None:
            time_signature = TimeSignature(4, 4)  # Default 4/4

        try:
            # Generate major generator rhythm for full period
            major_period = major.value * major.value
            major_rhythm = self._generate_rhythm_string(major.value, major_period)

            # Find beat positions in major rhythm
            beat_indexes = [i for i, beat in enumerate(major_rhythm) if beat == 1]

            # Generate fractioning groups
            fractioning_groups = self._generate_fractioning_groups(
                major.value, minor.value, beat_indexes, major_period
            )

            # Merge all rhythms
            all_rhythms = [major_rhythm] + fractioning_groups
            merged_rhythm = self._merge_rhythms(all_rhythms)

            # Create domain objects
            sequence = RhythmSequence(beats=merged_rhythm)

            return RhythmPattern(
                sequence=sequence,
                time_signature=time_signature,
                generator_a=major,
                generator_b=minor,
                rhythm_type="fractioning"
            )

        except Exception as e:
            raise RhythmGenerationError(f"Failed to generate fractioning rhythm: {e}") from e

    def _generate_rhythm_string(self, generator: int, period: int) -> List[int]:
        """Generate a basic rhythm string for a single generator."""
        return [int(i % generator == 0) for i in range(period)]

    def _merge_rhythms(self, rhythms: List[List[int]]) -> List[int]:
        """Merge multiple rhythms using OR operation."""
        if not rhythms:
            return []

        # Ensure all rhythms have the same length
        max_length = max(len(r) for r in rhythms)
        padded_rhythms = []
        for rhythm in rhythms:
            if len(rhythm) < max_length:
                # Pad with zeros
                padded = rhythm + [0] * (max_length - len(rhythm))
            else:
                padded = rhythm
            padded_rhythms.append(padded)

        # Merge using OR operation
        return [1 if any(values) else 0 for values in zip(*padded_rhythms)]

    def _generate_fractioning_groups(self, major: int, minor: int,
                                   beat_indexes: List[int], max_length: int) -> List[List[int]]:
        """Generate fractioning rhythm groups for double fractioning."""
        groups = []
        rhythm_length = major * minor

        for index in beat_indexes:
            # Create group starting with padding
            group = [0] * index if index != 0 else []

            # Insert the fractioning rhythm
            fractioning_rhythm = self._generate_rhythm_string(minor, rhythm_length)
            group[index:index] = fractioning_rhythm

            # Truncate if too long
            if len(group) > max_length:
                group = group[:max_length]
                break

            # Pad to max length
            group += [0] * (max_length - len(group))
            groups.append(group)

        return groups
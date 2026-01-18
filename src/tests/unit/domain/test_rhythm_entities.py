"""
Unit Tests - Domain Layer - Rhythm Entities
Tests for domain entities and value objects.
"""

import pytest
from schillinger.domain.rhythm.entities import Generator, TimeSignature, RhythmSequence, RhythmPattern, DomainError


class TestGenerator:
    """Test cases for Generator value object."""

    def test_valid_generator(self):
        """Test creating a valid generator."""
        gen = Generator(3)
        assert gen.value == 3

    def test_invalid_generator_zero(self):
        """Test that zero is rejected."""
        with pytest.raises(DomainError, match="positive integer"):
            Generator(0)

    def test_invalid_generator_negative(self):
        """Test that negative values are rejected."""
        with pytest.raises(DomainError, match="positive integer"):
            Generator(-1)


class TestTimeSignature:
    """Test cases for TimeSignature value object."""

    def test_valid_time_signature(self):
        """Test creating a valid time signature."""
        ts = TimeSignature(4, 4)
        assert ts.numerator == 4
        assert ts.denominator == 4
        assert ts.to_string() == "4/4"

    def test_time_signature_from_string(self):
        """Test creating time signature from string."""
        ts = TimeSignature.from_string("3/4")
        assert ts.numerator == 3
        assert ts.denominator == 4

    def test_invalid_denominator(self):
        """Test that invalid denominators are rejected."""
        with pytest.raises(DomainError, match="denominator must be one of"):
            TimeSignature(4, 3)  # 3 is not a valid denominator

    def test_zero_numerator(self):
        """Test that zero numerator is rejected."""
        with pytest.raises(DomainError, match="numerator must be positive"):
            TimeSignature(0, 4)


class TestRhythmSequence:
    """Test cases for RhythmSequence value object."""

    def test_valid_sequence(self):
        """Test creating a valid rhythm sequence."""
        seq = RhythmSequence([1, 0, 1, 1, 1, 0])
        assert seq.beats == [1, 0, 1, 1, 1, 0]

    def test_to_durations(self):
        """Test converting sequence to note durations."""
        seq = RhythmSequence([1, 0, 1, 1, 1, 0])
        durations = seq.to_durations()
        assert durations == [2, 1, 1, 2]  # [1+1, 1, 1, 1+1]

    def test_empty_sequence(self):
        """Test that empty sequence is rejected."""
        with pytest.raises(DomainError, match="cannot be empty"):
            RhythmSequence([])

    def test_invalid_values(self):
        """Test that invalid values are rejected."""
        with pytest.raises(DomainError, match="must contain only 0s and 1s"):
            RhythmSequence([1, 0, 2])  # 2 is invalid


class TestRhythmPattern:
    """Test cases for RhythmPattern value object."""

    def test_valid_pattern(self):
        """Test creating a valid rhythm pattern."""
        sequence = RhythmSequence([1, 0, 1])
        time_sig = TimeSignature(4, 4)
        gen_a = Generator(3)
        gen_b = Generator(2)

        pattern = RhythmPattern(
            sequence=sequence,
            time_signature=time_sig,
            generator_a=gen_a,
            generator_b=gen_b,
            rhythm_type="binary_sync"
        )

        assert pattern.sequence == sequence
        assert pattern.time_signature == time_sig
        assert pattern.generator_a == gen_a
        assert pattern.generator_b == gen_b
        assert pattern.rhythm_type == "binary_sync"
        assert pattern.durations == [2, 1]  # [1+1, 1]

    def test_invalid_rhythm_type(self):
        """Test that invalid rhythm types are rejected."""
        sequence = RhythmSequence([1, 0])
        time_sig = TimeSignature(4, 4)

        with pytest.raises(DomainError, match="Rhythm type must be one of"):
            RhythmPattern(sequence, time_sig, rhythm_type="invalid")
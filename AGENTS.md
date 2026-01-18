# AGENTS.md - Guidelines for Agentic Coding Assistants

This document provides guidelines for agentic coding assistants working on the Schillinger Rhythm Generator project. It includes build/lint/test commands and code style guidelines to ensure consistency across the codebase.

## Project Overview

The Schillinger Rhythm Generator is a Python GUI application that implements Joseph Schillinger's theory of music composition, focusing on binary synchronization and double fractioning techniques for generating complex rhythmic patterns.

## Build/Lint/Test Commands

### Running the Application
```bash
# Run the main GUI application
python main.py

# Run with virtual environment (recommended)
source .venv/bin/activate && python main.py
```

### Testing Commands

```bash
# Run all tests using unittest
python -m unittest discover tests/

# Run specific test file
python -m unittest tests.test_music_processor

# Run specific test method
python -m unittest tests.test_music_processor.TestMusicProcessor.test_binary_sync

# Run tests with verbose output
python -m unittest discover tests/ -v

# Run tests in quiet mode (only show failures)
python -m unittest discover tests/ -q
```

### Linting and Code Quality

```bash
# Run flake8 linting on all Python files
python -m flake8 schillinger/ tests/ main.py

# Run flake8 on specific file
python -m flake8 schillinger/music_processor.py

# Check code complexity with mccabe
python -m flake8 --select=C schillinger/

# Run flake8 with custom max line length
python -m flake8 --max-line-length=100 schillinger/
```

### Code Formatting

```bash
# Format code with black (if installed)
black schillinger/ tests/ main.py

# Check formatting without changes
black --check schillinger/ tests/ main.py

# Format specific file
black schillinger/music_processor.py
```

### Dependency Management

```bash
# Install dependencies
pip install -r requirements.txt

# Update requirements.txt after installing new packages
pip freeze > requirements.txt

# Install in development mode (if setup.py exists)
pip install -e .
```

### Environment Setup

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment (Linux/Mac)
source .venv/bin/activate

# Activate virtual environment (Windows)
.venv\Scripts\activate

# Deactivate virtual environment
deactivate
```

## Code Style Guidelines

### Python Version and Imports

- **Python Version**: Target Python 3.8+ (currently using 3.12.12)
- **Import Style**: Use absolute imports within the schillinger package
- **Import Organization**:
  - Standard library imports first
  - Third-party imports second
  - Local imports last
  - One import per line
  - Alphabetize imports within each group

```python
# Good
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

from schillinger.music_processor import dbl_bynary_sync, dbl_fractioning

# Avoid
from schillinger.music_processor import *
import os, sys
```

### Naming Conventions

- **Variables**: `snake_case` (e.g., `rhythmic_resultant`, `time_signature`)
- **Functions**: `snake_case` (e.g., `generate_png`, `dbl_bynary_sync`)
- **Classes**: `PascalCase` (e.g., `RhythmicContinuity`, `MusicProcessor`)
- **Constants**: `UPPER_CASE` (e.g., `DEFAULT_TIME_SIG = "4/4"`)
- **Modules**: `snake_case` (e.g., `music_processor.py`, `u_rhythm.py`)
- **Packages**: `snake_case` (e.g., `schillinger`, `utils`)

### Function and Method Signatures

- Use type hints for function parameters and return values
- Provide descriptive parameter names
- Include default values where appropriate

```python
def dbl_bynary_sync(a: int, b: int, time_sig: str = '4/4') -> str:
    """Generate binary synchronization rhythm."""

def process_rhythm_data(data: List[int], time_signature: str) -> Optional[Stream]:
    """Process rhythm data into music21 stream."""
```

### Documentation

- Use docstrings for all public functions, classes, and modules
- Follow Google-style docstrings
- Include parameter descriptions and return value information
- Document exceptions that may be raised

```python
def generate_rhythm_str(generator: int, length: int) -> str:
    """Generate a rhythm string from a generator.

    Args:
        generator: The generator number for rhythm creation
        length: The desired length of the rhythm string

    Returns:
        A string representation of the rhythm pattern

    Raises:
        ValueError: If generator is not a positive integer
    """
```

### Error Handling

- Use specific exception types rather than generic `Exception`
- Provide meaningful error messages
- Handle edge cases gracefully
- Log errors appropriately for debugging

```python
# Good
if b > a:
    raise ValueError("Minor generator (b) must be <= major generator (a)")

try:
    img = Image.open(png_path)
    img = img.resize((600, 200), Image.LANCZOS)
except FileNotFoundError:
    messagebox.showerror("Error", "Image file not found")
except Exception as e:
    messagebox.showerror("Error", f"Unexpected error: {e}")

# Avoid
except:
    pass
```

### Code Structure and Organization

- **Package Structure**: Follow the existing schillinger package layout
- **File Organization**: Group related functionality together
- **Class Design**: Use classes for complex data structures and state management
- **Function Length**: Keep functions focused and under 50 lines when possible
- **Module Imports**: Use relative imports within packages

```python
# schillinger/music_processor.py
from .utils.rhythm.u_rhythm import get_rhythmic_resultant_from_generators
from .render.render_rhythm import generate_png
```

### GUI Development Guidelines

- **Tkinter Best Practices**: Use ttk widgets for modern appearance
- **Layout Management**: Use grid() for complex layouts, pack() for simple ones
- **Event Handling**: Separate UI logic from business logic
- **Resource Management**: Properly manage image references to prevent garbage collection
- **Error Messages**: Use messagebox for user notifications

```python
# Good
def update_image(self, png_path: str) -> None:
    """Update the displayed image with proper resource management."""
    try:
        img = Image.open(png_path)
        img = img.resize((600, 200), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)

        self.label_img.configure(image=photo)
        self.label_img.image = photo  # Prevent garbage collection
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load image: {e}")
```

### Testing Guidelines

- **Test Organization**: Place tests in `tests/` directory mirroring package structure
- **Test Naming**: Use `test_` prefix for test functions and methods
- **Test Coverage**: Test both success and failure cases
- **Mocking**: Use unittest.mock for external dependencies
- **Assertions**: Use descriptive assertion messages

```python
# tests/test_music_processor.py
import unittest
from unittest.mock import patch
from schillinger.music_processor import dbl_bynary_sync

class TestMusicProcessor(unittest.TestCase):
    def test_binary_sync_valid_input(self):
        """Test binary sync with valid generators."""
        result = dbl_bynary_sync(3, 2, "4/4")
        self.assertIsInstance(result, str)
        self.assertTrue(result.endswith('.png'))

    def test_binary_sync_invalid_input(self):
        """Test binary sync with invalid generators."""
        with self.assertRaises(ValueError):
            dbl_bynary_sync(2, 3)  # b > a should raise error
```

### Performance Considerations

- **Memory Management**: Be mindful of image loading and GUI resource usage
- **Algorithm Efficiency**: Optimize rhythm generation algorithms for larger inputs
- **File I/O**: Use context managers for file operations
- **Caching**: Consider caching for expensive computations

### Security Best Practices

- **Input Validation**: Validate all user inputs before processing
- **File Paths**: Sanitize file paths to prevent directory traversal
- **External Commands**: Avoid shell injection in system calls
- **Dependencies**: Keep dependencies updated and review for vulnerabilities

### Git and Version Control

- **Commit Messages**: Use descriptive commit messages following conventional format
- **Branching**: Use feature branches for new functionality
- **Code Reviews**: Ensure all changes are reviewed before merging

```bash
# Good commit messages
git commit -m "feat: add double fractioning rhythm generation"
git commit -m "fix: handle edge case when b > a in binary sync"
git commit -m "refactor: extract rhythm rendering logic to separate module"
```

### Development Workflow

1. **Setup**: Create virtual environment and install dependencies
2. **Development**: Write code following style guidelines
3. **Testing**: Run tests and linting before committing
4. **Documentation**: Update docstrings and comments as needed
5. **Review**: Ensure code follows all guidelines before submitting

This document should be updated as the project evolves and new conventions are established.</content>
<parameter name="filePath">/home/federicotoscano/projects/schillinger/AGENTS.md
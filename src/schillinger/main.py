"""
Main Application Entry Point
Wires together all layers using dependency injection.
"""

import tkinter as tk
from schillinger.infrastructure.config.container import Container
from schillinger.presentation.views.rhythm_generator_view import RhythmGeneratorView


def main():
    """Application entry point."""
    # Initialize dependency injection container
    container = Container()

    # Create root window
    root = tk.Tk()

    # Create and configure the main view
    view = RhythmGeneratorView(root, container.generate_rhythm_use_case())

    # Start the application
    view.run()


if __name__ == "__main__":
    main()
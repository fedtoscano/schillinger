"""
Presentation Layer - Rhythm Generator View
Clean UI component that orchestrates use cases for rhythm generation.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
from PIL import Image, ImageTk

from ...application.use_cases.generate_rhythm import GenerateRhythmUseCase
from ...application.dto.requests import GenerateRhythmRequest


class RhythmGeneratorView:
    """
    Presentation Layer: Clean UI for rhythm generation.

    This view handles all UI concerns and delegates business logic
    to the application layer (use cases).
    """

    def __init__(self, root: tk.Tk, generate_use_case: GenerateRhythmUseCase):
        self.root = root
        self.generate_use_case = generate_use_case

        # UI state
        self.current_image: Optional[ImageTk.PhotoImage] = None

        self.setup_ui()
        self.setup_bindings()

    def setup_ui(self):
        """Initialize the user interface."""
        self.root.title("Schillinger Rhythm Generator")
        self.root.geometry("800x600")

        # Variables
        self.major_gen_var = tk.IntVar(value=3)
        self.minor_gen_var = tk.IntVar(value=2)
        self.rhythm_type_var = tk.StringVar(value="binary_sync")
        self.time_sig_var = tk.StringVar(value="4/4")

        # Header
        header = tk.Label(self.root, text="Schillinger Rhythm Generator",
                         font=("Arial", 16, "bold"))
        header.pack(pady=10)

        # Control panel
        self.create_control_panel()

        # Result display
        self.create_result_display()

        # Footer
        footer = tk.Button(self.root, text="Exit", command=self.root.quit)
        footer.pack(pady=10)

    def create_control_panel(self):
        """Create the control panel with input fields."""
        panel = tk.Frame(self.root, relief="raised", borderwidth=2)
        panel.pack(pady=10, padx=20, fill="x")

        # Title
        title = tk.Label(panel, text="Rhythm Parameters", font=("Arial", 12, "bold"))
        title.pack(pady=5)

        # Input fields
        input_frame = tk.Frame(panel)
        input_frame.pack(pady=5)

        # Major generator
        tk.Label(input_frame, text="Major Generator (A):").grid(row=0, column=0, padx=5, pady=2, sticky="e")
        major_combo = ttk.Combobox(input_frame, textvariable=self.major_gen_var,
                                  values=list(range(1, 10)), state="readonly", width=5)
        major_combo.grid(row=0, column=1, padx=5, pady=2)

        # Minor generator
        tk.Label(input_frame, text="Minor Generator (B):").grid(row=0, column=2, padx=5, pady=2, sticky="e")
        minor_combo = ttk.Combobox(input_frame, textvariable=self.minor_gen_var,
                                  values=list(range(1, 10)), state="readonly", width=5)
        minor_combo.grid(row=0, column=3, padx=5, pady=2)

        # Rhythm type
        tk.Label(input_frame, text="Rhythm Type:").grid(row=1, column=0, padx=5, pady=2, sticky="e")
        type_combo = ttk.Combobox(input_frame, textvariable=self.rhythm_type_var,
                                 values=["binary_sync", "fractioning"], state="readonly", width=12)
        type_combo.grid(row=1, column=1, padx=5, pady=2)

        # Time signature
        tk.Label(input_frame, text="Time Signature:").grid(row=1, column=2, padx=5, pady=2, sticky="e")
        time_combo = ttk.Combobox(input_frame, textvariable=self.time_sig_var,
                                 values=["4/4", "3/4", "2/4", "6/8"], state="readonly", width=5)
        time_combo.grid(row=1, column=3, padx=5, pady=2)

        # Generate button
        generate_btn = tk.Button(panel, text="Generate Rhythm",
                                command=self.on_generate_clicked,
                                bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        generate_btn.pack(pady=10)

    def create_result_display(self):
        """Create the result display area."""
        result_frame = tk.Frame(self.root)
        result_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Title
        title = tk.Label(result_frame, text="Generated Rhythm", font=("Arial", 12, "bold"))
        title.pack(pady=5)

        # Image display
        self.image_label = tk.Label(result_frame, text="Click 'Generate Rhythm' to create a rhythm",
                                   bg="lightgray", relief="sunken", width=60, height=20)
        self.image_label.pack(pady=10, fill="both", expand=True)

    def setup_bindings(self):
        """Set up event bindings."""
        # Could add keyboard shortcuts here
        pass

    def on_generate_clicked(self):
        """Handle generate button click - delegate to use case."""
        try:
            # Create request
            request = GenerateRhythmRequest(
                major_generator=self.major_gen_var.get(),
                minor_generator=self.minor_gen_var.get(),
                rhythm_type=self.rhythm_type_var.get(),
                time_signature=self.time_sig_var.get()
            )

            # Execute use case
            response = self.generate_use_case.execute(request)

            if response.success:
                self.display_rhythm(response.notation_path)
                self.show_success_message()
            else:
                messagebox.showerror("Generation Failed", response.error_message)

        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
        except Exception as e:
            messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {e}")

    def display_rhythm(self, png_path: str):
        """Display the generated rhythm PNG."""
        try:
            # Load and resize image
            img = Image.open(png_path)
            img = img.resize((600, 200), Image.Resampling.LANCZOS)

            # Convert for tkinter
            self.current_image = ImageTk.PhotoImage(img)
            self.image_label.configure(image=self.current_image, text="")
            self.image_label.image = self.current_image  # Keep reference

        except Exception as e:
            messagebox.showerror("Display Error", f"Failed to display rhythm: {e}")

    def show_success_message(self):
        """Show success message to user."""
        # Could be enhanced with rhythm statistics
        messagebox.showinfo("Success", "Rhythm generated successfully!")

    def run(self):
        """Start the UI event loop."""
        self.root.mainloop()
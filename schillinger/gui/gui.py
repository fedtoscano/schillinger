import tkinter as tk
from tkinter import ttk
from .view.components.RhythmicGenerators import RhythmicGenerators

def run_gui():
    root = tk.Tk()
    root.geometry("1200x800")
    root.title("Schillinger System Pattern Generator")
    
    # Add RhythmicGenerators component
    generators = RhythmicGenerators(root)
    generators.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
    
    root.mainloop()
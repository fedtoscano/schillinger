import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from music_processor import *

class RhythmsGenerator(ttk.Frame):
    def __init__ (self, parent):
        super().__init__(parent)
        self.maj_gen = 1
        self.min_gen = 1
        self.extra_gen = []

    def initialize_generators(self):
        return [self.maj_gen, self.min_gen, *self.extra_gen]
    
    

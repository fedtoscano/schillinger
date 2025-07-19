from music21.stream import Stream, Measure
from music21.note import Note
from music21 import environment
from music21.meter import TimeSignature

us = environment.UserSettings()
us['musescoreDirectPNGPath'] = r"C:\Program Files\MuseScore 4\bin\MuseScore4.exe"

def generate_png(continuity: list, time_sig: str):
    stream = Stream()
    stream.append(TimeSignature(time_sig));
    for beat in continuity:
        n = Note()
        n.duration.quarterLength = beat
        stream.append(n)
        
    stream.show('musicxml.png')

    pass
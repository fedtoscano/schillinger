from music21.stream import Stream, Measure
from music21.note import Note
from music21 import environment
from music21.meter import TimeSignature
from utils.rhythm import u_rhythm

us = environment.UserSettings()
us['musescoreDirectPNGPath'] = r"C:\Program Files\MuseScore 4\bin\MuseScore4.exe"

def dbl_bynary_sync(a: int, b: int, time_sig: str):
    """
    This method takes two generators (a, b) and opens a .pgn file that contains the
    rhythmical interference of the two
    Args:
        a (int): major generator
        b (int): minor generator
    Returns:
        void
    """
    if b > a: return #todo handle the exception
    resultant = u_rhythm.get_rhythmic_resultant(a, b)
    bars = u_rhythm.replace_rests(resultant)

    stream = Stream()
    stream.append(TimeSignature(time_sig));
    for beat in bars:
        n = Note()
        n.duration.quarterLength = beat
        stream.append(n)

    stream.show('musicxml.png')

def dlb_fractioning(a: int, b: int):
    
    return 


dbl_bynary_sync(9, 2, '9/8')


from music21.stream import Stream, Measure
from music21.note import Note
from music21 import environment
from music21.meter import TimeSignature
from utils.rhythm.u_rhythm import * 
from render.render_rhythm import *

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
    resultant = get_rhythmic_resultant_from_generators(a, b, cp = a * b)
    bars = replace_rests(resultant)
    generate_png(bars, time_sig)

def dbl_fractioning(a: int, b: int, time_sig: str):
    maj_gen_str = generate_rhythm_str(a, a * a)
    b_indexes = [i for i, beat in enumerate(maj_gen_str) if beat == 1];
    b_groups = generate_fractioning_from_min_gen(a, b, b_indexes);
    continuity = merge_rhythmical_strings(maj_gen_str, *b_groups);
    no_rests = replace_rests(continuity)
    generate_png(no_rests, time_sig)


# dbl_bynary_sync(7, 3, '2/2')
dbl_fractioning(4, 3, '4/4')


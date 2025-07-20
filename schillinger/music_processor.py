from music21.stream import Stream, Measure
from music21.note import Note
from music21 import environment
from music21.meter import TimeSignature
from utils.rhythm.u_rhythm import * 
from render.render_rhythm import *

us = environment.UserSettings()
us['musescoreDirectPNGPath'] = r"C:\Program Files\MuseScore 4\bin\MuseScore4.exe"

def bynary_sync(a: int, b: int, time_sig: str):
    """
    This method takes two generators (a, b) and opens a .pgn file that contains the
    rhythmical interference of the two
    Args:
        a (int): major generator
        b (int): minor generator
    """
    if b > a: return #todo handle the exception
    resultant = get_rhythmic_resultant_from_generators(a, b, cp = a * b)
    bars = replace_rests(resultant)
    generate_png(bars, time_sig)
    return bars

def fractioning(a: int, b: int, time_sig: str):
    maj_gen_str = generate_rhythm_str(a, a * a)
    b_indexes = [i for i, beat in enumerate(maj_gen_str) if beat == 1]
    b_groups = generate_fractioning_from_min_gen(a, b, b_indexes)

    continuity = merge_rhythmical_continuities(maj_gen_str, *b_groups)
    no_rests = replace_rests(continuity)
    generate_png(no_rests, time_sig)
    return no_rests

def balancing(a: int, b: int, time_sig: str):
    #fractioning + bynary_sync + a(a - b)
    continuity = fractioning(a, b, time_sig)
    continuity.extend(bynary_sync(a, b, time_sig=time_sig))
    continuity.extend([a] * (a - b))
    
    print(continuity)
    return continuity
    pass

def expanding(a: int, b: int, time_sig: str):
    #bynary_sync + fractioning
    continuity = bynary_sync(a, b, time_sig=time_sig)
    continuity.extend(fractioning(a, b, time_sig=time_sig))
    # return bynary_sync(a, b, time_sig=time_sig).extend(fractioning(a, b, time_sig=time_sig))
    print(continuity)

    pass

def contracting(a: int, b: int, time_sig: str):
    #fractioning + bynary_sinc
    continuity = fractioning(a, b, time_sig=time_sig)
    continuity.extend(bynary_sync(a, b, time_sig=time_sig))
    # return fractioning(a, b, time_sig).extend(bynary_sync(a, b, time_sig=time_sig))
    print(continuity)
    pass

# bynary_sync(8, 5, '8/4')
# fractioning(8, 5, '8/4')
balancing(3, 2, '4/4')
expanding(3, 2, '4/4')
contracting(3, 2, '4/4')

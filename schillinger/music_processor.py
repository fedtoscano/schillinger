from music21.stream import Stream, Measure
from music21.note import Note
from music21 import environment
from music21.meter import TimeSignature
from .utils.rhythm.u_rhythm import * 
from .render.render_rhythm import *
from functools import reduce
from operator import mul

us = environment.UserSettings()
us['musescoreDirectPNGPath'] = r"C:\Program Files\MuseScore 4\bin\MuseScore4.exe"

def bynary_sync(a: int, b: int, time_sig: str):
    """
    This method takes two generators (a, b) and opens a .png file that contains the
    rhythmical interference of the two
    Args:
        a (int): major generator
        b (int): minor generator
    """
    if b > a: return #todo handle the exception
    resultant = get_rhythmic_resultant_from_generators(a, b, cp = a * b)
    bars = replace_rests(resultant)
    # generate_png(bars, time_sig)
    return bars

def multiple_sync(generators: list, time_sig: str): 
    """
    This method takes three or more generators to generate rhythmic interference
    From three generators, two resultants are produced, and they well complement each other:
        1. the first resultant is produced from the generators (ex. 2, 3, 5)
        2. the second resultant is produced from the complementary factors (ex. 6, 10, 15)
    """
    cp = reduce(mul, generators, 1)
    complementary_factors = [cp // gen for gen in generators]
    
    gen_resultant = get_rhythmic_resultant_from_generators(*generators, cp = cp)
    cfactors_resultant = get_rhythmic_resultant_from_generators(*complementary_factors, cp = cp)

    gen_bars = replace_rests(gen_resultant)
    cfactors_bars = replace_rests(cfactors_resultant)

    generate_png(gen_bars, time_sig)
    generate_png(cfactors_bars, time_sig)

    print(gen_resultant)
    print(cfactors_resultant)

def fractioning(a: int, b: int, time_sig: str):
    """
    Fractioning is the techique by which a becomes is own complementary factor, and b appears 'a' times
    """
    maj_gen_str = generate_rhythm_str(a, a * a)
    b_indexes = [i for i, beat in enumerate(maj_gen_str) if beat == 1]
    b_groups = generate_fractioning_from_min_gen(a, b, b_indexes)

    continuity = merge_rhythmical_continuities(maj_gen_str, *b_groups)
    no_rests = replace_rests(continuity)
    
    # generate_png(no_rests, time_sig)
    return no_rests


"""
The three methods shown below (balancing, expanding and contracting) represents three mathematical
ways to extend a rhythmic continuity from given generators, creating two rhythmical phrases that complement
each other in different ways:
    1. balancing: the two phrases are equal in length
    2. expanding: the second phrase is longer than the first
    3. contracting: the second phrase is shorter than the first
"""
def balancing(a: int, b: int, time_sig: str):
    #fractioning + bynary_sync + a(a - b)
    continuity = fractioning(a, b, time_sig)
    continuity.extend(bynary_sync(a, b, time_sig=time_sig))
    continuity.extend([a] * (a - b))    
    return continuity

def expanding(a: int, b: int, time_sig: str):
    #bynary_sync + fractioning
    continuity = bynary_sync(a, b, time_sig=time_sig)
    continuity.extend(fractioning(a, b, time_sig=time_sig))
    return continuity

def contracting(a: int, b: int, time_sig: str):
    #fractioning + bynary_sinc
    continuity = fractioning(a, b, time_sig=time_sig)
    continuity.extend(bynary_sync(a, b, time_sig=time_sig))
    print(continuity)
    return continuity;


multiple_sync([2, 3, 5], '4/4');
from dataclasses import dataclass
from typing import List

@dataclass
class RhythmicContinuity:
    major_gen: int
    minor_gen: List[int] 
    time_sig = str
    continuity = List[int] = None

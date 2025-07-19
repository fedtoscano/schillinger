from dataclasses import dataclass
from typing import List
from music_processor import *

@dataclass
class RhythmicContinuity:
    def bynary_sync(self, note):
        return dbl_bynary_sync()
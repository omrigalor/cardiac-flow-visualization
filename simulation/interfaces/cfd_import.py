"""Future adapter contract only. No sample/synthetic computational fields."""
from dataclasses import dataclass
from typing import Sequence
@dataclass
class CFDInput:
    source_file: str
    coordinate_units: str
    velocity_units: str
    pressure_units: str
    source_to_scene: Sequence[Sequence[float]]
    provenance: str
    # Source payload must provide points_xyz[N,3], velocity[T,N,3],
    # pressure[T,N], times_seconds[T], and optional streamlines[list[M,3]].
def import_cfd(data: CFDInput):
    raise NotImplementedError('Supply and review real CFD data, topology, units and registration before implementing visualization.')

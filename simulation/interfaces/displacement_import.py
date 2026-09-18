"""Future frame-by-frame mesh displacement contract; no invented dataset."""
from dataclasses import dataclass
@dataclass
class DisplacementInput:
    mesh_object: str
    source_file: str
    topology_hash: str
    units: str
    provenance: str
    # Required data: times_seconds[T], vertex_ids[N], displacement[T,N,3].
    # Must retain baseline coordinates; offsets never accumulate in-place.
def import_displacement(data: DisplacementInput):
    raise NotImplementedError('Verify topology, absolute/relative convention, timing and units against real results first.')

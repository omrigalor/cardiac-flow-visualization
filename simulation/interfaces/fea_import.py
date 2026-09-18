"""Future adapter contract only. Does not generate structural results."""
from dataclasses import dataclass
@dataclass
class FEAInput:
    source_file: str
    displacement_units: str
    stress_units: str
    strain_convention: str
    provenance: str
    # Payload must include persistent node IDs, element connectivity,
    # times_seconds[T], frame/leaflet displacement[T,N,3], stress and strain.
def import_fea(data: FEAInput):
    raise NotImplementedError('Real solver output and reviewed node correspondence are required.')

"""Finalize delivery PNGs and copy the two primary deliverables directly to Desktop."""
from pathlib import Path
import shutil,json,hashlib
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
import sys;sys.path.insert(0,str(ROOT));import config as C

def cards():
    end=C.ANIMATION_FPS*C.DURATION_SECONDS
    size=Image.open(ROOT/'renders/frames/0001.png').size
    card=Image.open(ROOT/'assets/branding/endcard_clean.png').resize(size)
    for f in range(end+1,end+3*C.ANIMATION_FPS+1):card.save(ROOT/'renders/frames'/('%04d.png'%f))

def copy_deliverables():
    desktop=ROOT.parent
    pairs=[(ROOT/'renders/final/concept_presentation.mp4',ROOT/'WATCH_VIDEO.mp4'),(ROOT/'renders/final/concept_presentation.mp4',desktop/'the device_Medical_Animation.mp4'),(ROOT/'valve_concept.blend',desktop/'the device_Medical_Animation.blend')]
    report=[]
    for source,dest in pairs:
        if not source.exists():raise FileNotFoundError(source)
        shutil.copy2(source,dest)
        digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
        assert digest(source)==digest(dest)
        report.append({'source':str(source),'desktop_copy':str(dest),'bytes':dest.stat().st_size,'sha256':digest(dest)})
    (ROOT/'renders/final/delivery_manifest.json').write_text(json.dumps(report,indent=2))
if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--cards',action='store_true');p.add_argument('--copy',action='store_true');a=p.parse_args()
    if a.cards:cards()
    if a.copy:copy_deliverables()

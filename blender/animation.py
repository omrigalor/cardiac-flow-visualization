import bpy
import config as C
from utils import visible_between

def create(root):
    # A conceptual crossfade at the annulus, never a claimed delivery procedure.
    for o in root.children:visible_between(o,C.REVEAL_START+21,C.ANIMATION_FPS*C.DURATION_SECONDS)
    mats=set(m for o in root.children if hasattr(o.data,'materials') for m in o.data.materials)
    for m in mats:
        p=m.node_tree.nodes.get('Principled BSDF')
        if not p:continue
        for f,v in [(1,0),(C.REVEAL_START+20,0),(C.REVEAL_END,1)]:
            p.inputs['Alpha'].default_value=v;p.inputs['Alpha'].keyframe_insert('default_value',frame=f)
        m.surface_render_method='DITHERED'
    scene=bpy.context.scene
    scene['Physiology']='RA (+Z) -> RV (-Z) in ventricular diastole; native RV -> RA jet in systole only.'
    scene['Concept_notice']='Not validated CFD, FEA, structural, fatigue, hemodynamic or clinical simulation. Generic device; not proprietary the device CAD.'
    scene['Timeline']='0–3 right heart; 3–8.5 native TR; 8.5–11 reveal; 11–20 function; 20–24 hero and text end card.'

def endcard(mat,camera):
    # Branding is composited onto a separate end card by encode.py; never over the anatomy.
    pass

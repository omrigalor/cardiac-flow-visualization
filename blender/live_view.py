"""GUI-only progress viewer. Polls the saved project, preserves playback on reload."""
import bpy,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
state={'mtime':0,'play':False}
def tick():
    p=ROOT/'valve_concept.blend'
    if p.exists() and p.stat().st_mtime>state['mtime']:
        state['mtime']=p.stat().st_mtime
        try:
            bpy.ops.wm.open_mainfile(filepath=str(p))
            for screen in bpy.data.screens:
                for area in screen.areas:
                    if area.type=='VIEW_3D':
                        area.spaces.active.region_3d.view_perspective='CAMERA'
                        area.spaces.active.shading.type='MATERIAL'
            state['play']=True
        except Exception as e:print('Live reload:',e)
    if state['play']:
        try:
            if not bpy.context.screen.is_animation_playing:bpy.ops.screen.animation_play()
            state['play']=False
        except Exception:pass
    return 4.0
bpy.app.timers.register(tick,first_interval=2,persistent=True)

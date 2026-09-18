import bpy,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'blender')]
import config as C
import materials,anatomy,anatomy_reference,import_device,valve,leaflets,blood_flow,lighting,cameras,animation,render,validation
bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene;s.frame_start=1;s.frame_end=C.ANIMATION_FPS*C.DURATION_SECONDS;s.render.fps=C.ANIMATION_FPS
for p in ['assets/reference','assets/branding','assets/textures','geometry/generated','geometry/imported','renders/diagnostics','renders/stills','renders/previews','renders/frames','renders/final']:(ROOT/p).mkdir(parents=True,exist_ok=True)
mat=materials.create();anatomy_reference.create(mat);anatomy_reference.great_vessels(mat);lighting.create(mat);cams=cameras.create();render.settings()
def save(label):
    s['Build milestone']=label
    bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'valve_concept.blend'))
    print('MILESTONE:',label,flush=True)
save('Right-heart anatomy MVP')
root,frame=valve.create(mat)
if C.IMPORTED_DEVICE:
    imported=import_device.import_device(root)
    for o in frame:o.hide_render=True;o.hide_viewport=True;o.parent=None
save('Concept frame and skirt MVP')
leaflets.create(mat,root);save('Three deforming leaflets animated')
blood_flow.create(mat);animation.create(root);animation.endcard(mat,cams['Hero_Camera'])
s.frame_set(1)
# Pack reproducibility scripts and attribution into the blend for the Desktop handoff.
for path in [ROOT/'config.py',ROOT/'README.md',ROOT/'docs/ATTRIBUTION.md',*sorted((ROOT/'blender').glob('*.py'))]:
    if path.exists():
        text=bpy.data.texts.new(path.name);text.write(path.read_text())
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=='VIEW_3D':
            area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.shading.color_type='MATERIAL';area.spaces.active.overlay.show_overlays=False;area.spaces.active.shading.use_scene_world=True;area.spaces.active.shading.use_scene_lights=True;area.spaces.active.region_3d.view_camera_zoom=0
save('Complete animated scene with flow and story')
validation.validate()

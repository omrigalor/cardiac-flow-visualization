"""Pack and save a navigable delivery scene; no geometry or timing changes."""
import bpy,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'blender')]
import config as C
from validation import validate
s=bpy.context.scene;s.frame_set(1);s.render.resolution_x=C.RENDER_WIDTH;s.render.resolution_y=C.RENDER_HEIGHT;s.render.resolution_percentage=100;s.render.fps=C.ANIMATION_FPS;s.render.filepath=str(ROOT/'renders/frames/')
# Keep orbit navigation available and avoid locking viewport motion to the render camera.
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='VIEW_3D':
   space=area.spaces.active;space.lock_camera=False;space.overlay.show_overlays=False;space.region_3d.view_perspective='CAMERA';space.shading.type='MATERIAL'
for path in [ROOT/'config.py',ROOT/'README.md',ROOT/'RUNBOOK.md',ROOT/'docs/ATTRIBUTION.md',ROOT/'docs/REVIEW.md',*sorted((ROOT/'blender').glob('*.py'))]:
 if path.exists():
  text=bpy.data.texts.get(path.name) or bpy.data.texts.new(path.name);text.clear();text.write(path.read_text())
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'valve_concept.blend'));validate()

import bpy,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path[:0]=[str(R),str(R/'blender')]
from render import settings
settings(True);s=bpy.context.scene;s.render.resolution_percentage=60
for f in [380,585,640,698,754,810]:
 s.frame_set(f);s.render.filepath=str(R/'renders/diagnostics'/('orbit_%04d.png'%f));bpy.ops.render.render(write_still=True)

import bpy,sys,time
from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=bpy.context.scene
s.render.engine='BLENDER_WORKBENCH';s.render.resolution_x=800;s.render.resolution_y=600;s.render.resolution_percentage=100
s.display.shading.light='STUDIO';s.display.shading.color_type='MATERIAL';s.display.shading.show_shadows=True;s.display.shading.show_cavity=True
s.render.image_settings.file_format='PNG'
for f in [35,196,380,415,630]:
 s.frame_set(f);s.render.filepath=str(R/'renders/diagnostics'/('shape_%d.png'%f));print('START',f,flush=True);bpy.ops.render.render(write_still=True)

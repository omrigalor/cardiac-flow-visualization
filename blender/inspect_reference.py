import bpy,sys,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(R/'assets/reference/hra_heart_male.glb'))
for o in bpy.context.scene.objects:
 if o.type=='MESH':
  vs=[o.matrix_world@v.co for v in o.data.vertices];cen=sum(vs,Vector())/len(vs)
  print(o.name,'CENTER',tuple(round(x,4) for x in cen),'RANGE',[(round(min(v[i] for v in vs),4),round(max(v[i] for v in vs),4)) for i in range(3)],'verts',len(vs))

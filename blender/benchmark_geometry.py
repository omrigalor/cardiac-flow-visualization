import bpy,time
s=bpy.context.scene;s.frame_set(35)
for o in list(s.objects):
 if o.type=='MESH':
  print(o.name,'v',len(o.data.vertices),'p',len(o.data.polygons),'max_ngon',max((len(p.vertices) for p in o.data.polygons),default=0),flush=True)
  for m in list(o.modifiers):o.modifiers.remove(m)
s.render.engine='BLENDER_WORKBENCH';s.render.resolution_x=640;s.render.resolution_y=360;s.render.resolution_percentage=100;s.render.filepath=bpy.path.abspath('//renders/diagnostics/no_subdivision.png')
print('RENDER NO MODIFIERS',flush=True);bpy.ops.render.render(write_still=True)

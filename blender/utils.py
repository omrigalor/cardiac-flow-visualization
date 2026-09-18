import bpy, math
from mathutils import Vector

def mesh(name,verts,faces,mat):
    d=bpy.data.meshes.new(name); d.from_pydata(verts,[],faces); d.update()
    o=bpy.data.objects.new(name,d); bpy.context.collection.objects.link(o)
    o.data.materials.append(mat)
    for p in d.polygons:p.use_smooth=True
    return o

def curve(name,points,radius,mat,cyclic=False):
    d=bpy.data.curves.new(name,'CURVE');d.dimensions='3D';d.resolution_u=12;d.bevel_depth=radius;d.bevel_resolution=3
    s=d.splines.new('POLY');s.points.add(len(points)-1)
    for p,co in zip(s.points,points):p.co=(*co,1)
    s.use_cyclic_u=cyclic
    o=bpy.data.objects.new(name,d);bpy.context.collection.objects.link(o);d.materials.append(mat);return o

def ring(name,r,z,tube,mat,yscale=1):
    return curve(name,[(r*math.cos(i*math.tau/160),r*yscale*math.sin(i*math.tau/160),z) for i in range(160)],tube,mat,True)

def aim(o,target):o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()

def smooth_keys(idblock):
    if not idblock.animation_data or not idblock.animation_data.action:return
    # Blender 5 layered actions.
    a=idblock.animation_data.action
    for layer in a.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                for fc in bag.fcurves:
                    for k in fc.keyframe_points:k.interpolation='LINEAR'

def visible_between(o,start,end,total=720):
    for f,hidden in [(1,start>1),(max(1,start-1),True),(start,False),(end,False),(end+1,True)]:
        if f==1 and start==1:hidden=False
        o.hide_render=hidden;o.keyframe_insert('hide_render',frame=f)
        o.hide_viewport=hidden;o.keyframe_insert('hide_viewport',frame=f)
    o.hide_render=False

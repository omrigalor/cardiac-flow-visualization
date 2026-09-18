"""One continuous anterior camera path; named inspection cameras remain available."""
import bpy,json,math
from mathutils import Vector,Matrix,Quaternion
import config as C

def orient(o,target,up):
    forward=(Vector(target)-o.location).normalized();right=forward.cross(up).normalized();newup=right.cross(forward)
    o.rotation_euler=Matrix((right,newup,-forward)).transposed().to_quaternion().to_euler()

def create():
    d=json.loads((C.ROOT/'geometry/generated/anatomy_registration.json').read_text());basis=Matrix(d['basis']);up=basis@Vector((0,0,1));direction=(basis@Vector((-.10,-1,.24))).normalized()
    cams={}
    for name,(loc,target,lens) in C.CAMERAS.items():
        data=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,data);bpy.context.collection.objects.link(o);o.location=loc;data.lens=lens;data.clip_start=C.CAMERA_CLIP_START;data.clip_end=C.CAMERA_CLIP_END;orient(o,target,up);cams[name]=o
    master=cams['Hero_Camera'];master.data.lens=52
    # Medical explanation stays on the same anterior axis.
    for f,dist,target in [(1,25,(.9,-.5,-.2)),(75,24,(.9,-.5,-.2)),(160,17,(.4,-.2,-.1)),(255,16,(.3,-.1,-.1)),(331,15,(.2,0,-.1)),(540,15,(.2,0,-.1))]:
        master.location=Vector(target)+direction*dist;orient(master,target,up);master.keyframe_insert('location',frame=f);master.keyframe_insert('rotation_euler',frame=f)
    # One dedicated, continuous 360-degree anatomical-X orbit, with a restrained Y excursion.
    # Rotate the up-vector with the camera to avoid pole singularities / sudden roll flips.
    xaxis=basis@Vector((1,0,0));yaxis=basis@Vector((0,1,0));last_euler=master.rotation_euler.copy()
    for f in range(541,C.ANIMATION_FPS*C.DURATION_SECONDS+1):
        pull=min(1,(f-540)/45);pull=pull*pull*(3-2*pull)
        target=Vector((.2,0,-.1)).lerp(Vector((.8,-.4,-.2)),pull);dist=15+13*pull
        t=max(0,(f-585)/(C.ANIMATION_FPS*C.DURATION_SECONDS-585));e=t*t*(3-2*t)
        q=Quaternion(yaxis,.10*math.sin(math.tau*e))@Quaternion(xaxis,math.tau*e)
        master.location=target+(q@direction)*dist;orient(master,target,q@up)
        master.rotation_euler=master.rotation_euler.to_quaternion().to_euler('XYZ',last_euler);last_euler=master.rotation_euler.copy()
        master.keyframe_insert('location',frame=f);master.keyframe_insert('rotation_euler',frame=f)
    for f,title in [(1,'01 | Whole heart'),(90,'02 | Anterior cutaway'),(160,'03 | Native regurgitation'),(255,'04 | Concept reveal'),(331,'05 | Valve function'),(541,'06 | Pull back'),(585,'07 | Single 360-degree hero orbit')]:
        marker=bpy.context.scene.timeline_markers.new(title,frame=f);marker.camera=master
    bpy.context.scene.camera=master;return cams

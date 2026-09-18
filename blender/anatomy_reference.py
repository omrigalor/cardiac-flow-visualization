"""Adapted HRA Visible Human anatomy, CC BY 4.0. See docs/ATTRIBUTION.md.
Rigid reorientation and art scale only; procedural annular interface remains conceptual.
"""
import bpy,bmesh,math
import numpy as np
from mathutils import Vector,Matrix
import config as C
from utils import smooth_keys

def create(mat):
    before=set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=str(C.ROOT/'assets/reference/hra_heart_male.glb'))
    imported=[o for o in bpy.data.objects if o not in before]
    empties=[o for o in imported if o.type=='EMPTY']
    native=next(o for o in imported if o.name=='VH_M_tricuspid_valve')
    atrium=next(o for o in imported if 'right_cardiac_atrium' in o.name)
    def arr(o):return np.array([tuple(o.matrix_world@v.co) for v in o.data.vertices])
    points=arr(native);center=points.mean(axis=0)
    w,e=np.linalg.eigh(np.cov((points-center).T));z=e[:,0]
    if np.dot(z,arr(atrium).mean(axis=0)-center)<0:z=-z
    # Anatomy axis: RV->RA is +Z. Positive X keeps adjacent LV on viewer's right.
    x=np.array([1.,0,0]);x-=z*np.dot(x,z);x/=np.linalg.norm(x);y=np.cross(z,x)
    rotation=np.array([x,y,z]);projected=(points-center)@rotation.T
    radii=np.sqrt(projected[:,0]**2+projected[:,1]**2)
    scale=(C.TRICUSPID_ANNULUS_DIAMETER/2)/np.quantile(radii,.92)
    # Orient around the geometric center of the published native annular region.
    transform=Matrix(((scale*x[0],scale*x[1],scale*x[2],-scale*np.dot(x,center)),(scale*y[0],scale*y[1],scale*y[2],-scale*np.dot(y,center)),(scale*z[0],scale*z[1],scale*z[2],-scale*np.dot(z,center)),(0,0,0,1)))
    rename={'VH_M_right_cardiac_atrium':'Right_Atrium','VH_M_heart_right_ventricle':'Right_Ventricle','VH_M_left_cardiac_atrium':'Surrounding_Left_Atrial_Myocardium','VH_M_heart_left_ventricle':'Surrounding_Left_Ventricular_Myocardium','VH_M_interventricular_septum':'Interventricular_Septum'}
    retained=[]
    for o in imported:
        if o.type!='MESH':continue
        old=o.name
        if 'valve' in old or 'papillary' in old:
            # No imported aortic/mitral apparatus is included in this scene.
            bpy.data.objects.remove(o,do_unlink=True);continue
        world=o.matrix_world.copy();o.parent=None;o.matrix_world=Matrix.Identity(4);o.data.transform(transform@world);o.name=rename.get(old,old)
        o.data.materials.clear();o.data.materials.append(mat['tissue']);o.data.materials.append(mat['edge'])
        for p in o.data.polygons:p.use_smooth=True
        # Gentle smoothing retains atlas contour and anatomical asymmetry.
        sm=o.modifiers.new('Reference surface smoothing','SMOOTH');sm.factor=.7;sm.iterations=3
        # Atlas is already dense; subdivision of clipped high-valence caps stalls evaluation.
        # Preserve the published tessellation and smooth normals instead.
        o['source']='HRA / Visible Human Male, adapted: rigid registration, visual scale, cutaway, shader.'
        retained.append(o)
        if o.name in ['Right_Atrium','Right_Ventricle']:
            center_local=sum((v.co for v in o.data.vertices),Vector())/len(o.data.vertices)
            bpy.context.scene[o.name+'_center']=list(center_local)
    for o in empties:bpy.data.objects.remove(o,do_unlink=True)
    # Continuous exterior for the opening: union source myocardium before cutting.
    exterior_data=bpy.data.meshes.new('Whole exterior source union');bm=bmesh.new()
    for source in retained:
        # External-only closed chamber envelopes prevent thin-wall remesh perforations.
        # The internal cutaway still uses unmodified atlas contours.
        hull=bmesh.new()
        for vertex in source.data.vertices:hull.verts.new(vertex.co)
        bmesh.ops.convex_hull(hull,input=list(hull.verts),use_existing_faces=False)
        unused=[v for v in hull.verts if not v.link_faces]
        if unused:bmesh.ops.delete(hull,geom=unused,context='VERTS')
        temp=bpy.data.meshes.new('Exterior closure temporary');hull.to_mesh(temp);hull.free();bm.from_mesh(temp);bpy.data.meshes.remove(temp)
    bm.to_mesh(exterior_data);bm.free()
    exterior=bpy.data.objects.new('Whole_Heart_Exterior',exterior_data);bpy.context.collection.objects.link(exterior);exterior_data.materials.append(mat['tissue'])
    bpy.context.view_layer.objects.active=exterior;exterior.select_set(True)
    rem=exterior.modifiers.new('Continuous epicardial envelope','REMESH');rem.mode='VOXEL';rem.voxel_size=.065;rem.use_smooth_shade=True
    bpy.ops.object.modifier_apply(modifier=rem.name)
    sm=exterior.modifiers.new('Soft anatomical envelope','SMOOTH');sm.factor=.8;sm.iterations=4
    exterior['source']='Union of adapted HRA myocardial surfaces, for exterior context only.'
    for f,hidden in [(1,False),(89,False),(90,True),(720,True)]:
        exterior.hide_render=hidden;exterior.keyframe_insert('hide_render',frame=f);exterior.hide_viewport=hidden;exterior.keyframe_insert('hide_viewport',frame=f)
    for body in retained:
        for f,hidden in [(1,True),(89,True),(90,False),(720,False)]:
            body.hide_render=hidden;body.keyframe_insert('hide_render',frame=f);body.hide_viewport=hidden;body.keyframe_insert('hide_viewport',frame=f)
    # Front right-heart walls are a separate matching segment, fading to an actual cut plane.
    for o in list(retained):
        if o.name not in ['Right_Atrium','Right_Ventricle']:continue
        front=o.copy();front.data=o.data.copy();bpy.context.collection.objects.link(front);front.name=o.name+'_Anterior_Reveal'
        cut_offset=0.02 if o.name=='Right_Atrium' else -.42
        for target,clear_inner,clear_outer in [(o,True,False),(front,False,True)]:
            bm=bmesh.new();bm.from_mesh(target.data)
            result=bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=.0001,plane_co=tuple(Vector(rotation[:,1])*cut_offset),plane_no=tuple(rotation[:,1]),clear_inner=clear_inner,clear_outer=clear_outer)
            boundary=[e for e in bm.edges if e.is_boundary and all(abs(v.co.dot(Vector(rotation[:,1]))-cut_offset)<.002 for v in e.verts)]
            if boundary:
                fill=bmesh.ops.holes_fill(bm,edges=boundary,sides=0)
                for f in fill.get('faces',[]):f.material_index=1
            bm.to_mesh(target.data);bm.free()
        for i,base in enumerate(list(front.data.materials)):
            fade=base.copy();fade.name=base.name+' | anterior reveal';front.data.materials[i]=fade
            p=fade.node_tree.nodes.get('Principled BSDF')
            for f,a in [(1,1),(90,1),(150,.10),(720,.10)]:p.inputs['Alpha'].default_value=a;p.inputs['Alpha'].keyframe_insert('default_value',frame=f)
            fade.surface_render_method='DITHERED'
        for f,v in [(1,True),(89,True),(90,False),(150,False),(151,False),(720,False)]:
            front.hide_render=v;front.keyframe_insert('hide_render',frame=f);front.hide_viewport=v;front.keyframe_insert('hide_viewport',frame=f)
        retained.append(front)
    # Save registration evidence; coordinate basis never presented as clinical dimensions.
    import json
    (C.ROOT/'geometry/generated/anatomy_registration.json').write_text(json.dumps({'source':'HRA VH_M_Heart.glb','scale_art_units':float(scale),'origin_source':center.tolist(),'basis':rotation.tolist(),'cut_plane_normal':rotation[:,1].tolist(),'cut_plane_RA_offset':.02,'cut_plane_RV_offset':-.42,'notice':'Concept art registration, not patient-specific planning.'},indent=2))
    from utils import ring
    ring('Tricuspid_Annulus',C.TRICUSPID_ANNULUS_DIAMETER/2,0,.065,mat['edge'])
    return retained

def great_vessels(mat):
    """Context-only great vessel continuations, not delivery access or aortic-valve geometry."""
    import json
    from utils import mesh,curve
    d=json.loads((C.ROOT/'geometry/generated/anatomy_registration.json').read_text());rot=Matrix(d['basis']);origin=Vector(d['origin_source']);sc=d['scale_art_units']
    def tr(p):return rot@((Vector(p)-origin)*sc)
    # Source-coordinate paths continue visible superior vessel openings.
    paths=[('Superior_Vena_Cava',[(-.025,-.028,.519),(-.027,-.027,.538),(-.027,-.026,.560)],.0065),
           ('Pulmonary_Trunk',[(.0179,-.0432,.5086),(.014,-.046,.532),(.004,-.042,.548),(-.020,-.032,.552)],.009),
           ('Great_Arterial_Arch',[(.0089,-.0279,.4971),(.010,-.025,.530),(.006,-.016,.553),(-.012,-.004,.553),(-.023,.006,.537)],.0095)]
    for name,points,radius in paths:
        # Catmull-Rom interpolation with open tubular walls and visible lumens.
        src=[Vector(points[0])]+[Vector(p) for p in points]+[Vector(points[-1])];samples=[]
        for i in range(1,len(src)-2):
            for j in range(18):
                t=j/18;p0,p1,p2,p3=src[i-1:i+3]
                p=.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t*t*t)
                samples.append(tr(p))
        samples.append(tr(points[-1]));v=[];f=[];N=32
        for j,p in enumerate(samples):
            tangent=(samples[min(j+1,len(samples)-1)]-samples[max(0,j-1)]).normalized();a=tangent.cross(Vector((0,0,1)))
            if a.length<.01:a=tangent.cross(Vector((0,1,0)))
            a.normalize();b=tangent.cross(a)
            for k in range(N):
                theta=k*math.tau/N;v.append(tuple(p+radius*sc*(math.cos(theta)*a+math.sin(theta)*b)))
        for j in range(len(samples)-1):
            for k in range(N):q=j*N+k;qn=j*N+(k+1)%N;f.append((q,qn,qn+N,q+N))
        ob=mesh(name,v,f,mat['tissue']);ob.data.materials.append(mat['edge']);sol=ob.modifiers.new('Vessel wall','SOLIDIFY');sol.thickness=.06;sol.material_offset_rim=1
        # Move out of the closeup after establishing; retain full exterior for opening.
        from utils import visible_between
        visible_between(ob,1,120)
        for frame,hidden in [(121,True),(540,True),(541,False),(C.ANIMATION_FPS*C.DURATION_SECONDS,False)]:
            ob.hide_render=hidden;ob.keyframe_insert('hide_render',frame=frame);ob.hide_viewport=hidden;ob.keyframe_insert('hide_viewport',frame=frame)

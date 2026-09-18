import bpy,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
import config as C

def validate(require_saved=True):
    names=bpy.data.objects
    checks={}
    for name in ['Right_Atrium','Right_Ventricle','Tricuspid_Annulus','Prosthetic_Frame',*C.CAMERAS]:checks[name]=name in names
    leaf=[o for o in names if o.name.startswith('Prosthetic_Leaflet_')]
    checks['exactly_three_prosthetic_leaflets']=len(leaf)==3
    checks['animated_leaflets']=len(leaf)==3 and all(o.data.shape_keys and o.data.shape_keys.animation_data for o in leaf)
    checks['forward_flow']=any(o.name.startswith('Forward_RA_to_RV_') for o in names)
    checks['regurgitant_flow']=any(o.name.startswith('Regurgitant_RV_to_RA_') for o in names)
    checks['no_aortic_primary_geometry']=not any(any(x in o.name.lower() for x in ['aortic','tavi']) for o in names)
    checks['frame_range']=bpy.context.scene.frame_start==1 and bpy.context.scene.frame_end==C.ANIMATION_FPS*C.DURATION_SECONDS
    checks['saved_blend']=not require_saved or (bool(bpy.data.filepath) and Path(bpy.data.filepath).exists())
    for path in ['renders/previews','renders/diagnostics','renders/stills','renders/frames','renders/final']:checks[path]=(ROOT/path).is_dir()
    from leaflets import opening
    checks['diastolic_open']=opening(20)>.99
    checks['systolic_closed']=opening(52)==0
    checks['seamless_cycle']=opening(1)==opening(C.CARDIAC_CYCLE_FRAMES+1)
    # Verify saved animation samples and phase-gating, beyond object presence.
    s=bpy.context.scene;old=s.frame_current
    for f,expected in [(380,1),(415,0)]:
        s.frame_set(f);checks['leaflet_phase_'+str(f)]=all(abs(o.data.shape_keys.key_blocks['Diastolic_Opening'].value-expected)<.01 for o in leaf)
    s.frame_set(415)
    checks['no_flow_through_closed_prosthesis']=all(o.scale.length<1e-6 for o in names if o.name.startswith(('Forward_RA_to_RV_','Regurgitant_RV_to_RA_')))
    # Verify actual advected cell positions, excluding periodic path wrap-around.
    import statistics
    for prefix,first,sign in [('Forward_RA_to_RV_',380,-1),('Regurgitant_RV_to_RA_',196,1)]:
        cells=[o for o in names if o.name.startswith(prefix)]
        s.frame_set(first);pos={o.name:o.location.z for o in cells if o.scale.length>.001}
        s.frame_set(first+1);deltas=[o.location.z-pos[o.name] for o in cells if o.name in pos and o.scale.length>.001 and abs(o.location.z-pos[o.name])<.5]
        checks[prefix+'direction']=len(deltas)>10 and statistics.median(deltas)*sign>0
    from bpy_extras.object_utils import world_to_camera_view
    from mathutils import Vector
    camera=names['Hero_Camera'];quaternions=[];framed=[]
    for frame in [1,75,160,255,331,540]:
        s.frame_set(frame);quaternions.append(camera.rotation_euler.to_quaternion())
        point=world_to_camera_view(s,camera,Vector((0,0,0)))
        framed.append(.05<point.x<.95 and .05<point.y<.95 and point.z>0)
    checks['stable_medical_sequence_camera_axis']=max(quaternions[0].rotation_difference(q).angle for q in quaternions)<.01
    checks['annulus_remains_in_frame']=all(framed)
    orbit=[]
    for frame in range(585,C.ANIMATION_FPS*C.DURATION_SECONDS+1,3):
        s.frame_set(frame);orbit.append(camera.rotation_euler.to_quaternion())
    checks['smooth_hero_orbit']=max(a.rotation_difference(b).angle for a,b in zip(orbit,orbit[1:]))<.15
    checks['whole_heart_exterior']='Whole_Heart_Exterior' in names
    checks['no_overlay_titles']=not any(o.type=='FONT' for o in names)
    s.frame_set(old)
    report={'passed':all(checks.values()),'checks':checks,'notice':'Sanity checks, not clinical validation.'}
    (ROOT/'renders/diagnostics/validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
    if not report['passed']:raise RuntimeError('Scene sanity checks failed')
    return report
if __name__=='__main__':
    sys.path.insert(0,str(ROOT/'blender'));validate()

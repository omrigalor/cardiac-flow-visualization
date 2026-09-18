"""Dense cellular flow illustration with phase-synchronized advection. NOT CFD.
Individual visible cells are exaggerated in size and spacing for readability.
"""
import bpy,math,random
from mathutils import Vector
import config as C
from utils import mesh,smooth_keys

def create(mat):
    rng=random.Random(904);end=C.ANIMATION_FPS*C.DURATION_SECONDS;result=[]
    ra=Vector(bpy.context.scene.get('Right_Atrium_center',(-.3,0,1.5)));rv=Vector(bpy.context.scene.get('Right_Ventricle_center',(.3,0,-1.8)))
    ra.z=max(.9,ra.z);rv.z=min(-1.1,rv.z)
    # Shared biconcave erythrocyte mesh; these are cells suspended in blood, not droplets.
    v=[];f=[];rings=8;sides=12
    for j in range(rings+1):
        phi=math.pi*j/rings;r=math.sin(phi);z=.23*math.cos(phi)*(.38+.62*r*r)
        for k in range(sides):a=k*math.tau/sides;v.append((r*math.cos(a),r*math.sin(a),z))
    for j in range(rings):
        for k in range(sides):q=j*sides+k;qn=j*sides+(k+1)%sides;f.append((q,qn,qn+sides,q+sides))
    template=mesh('Blood_Cell_Template',v,f,mat['flow']);data=template.data;bpy.data.objects.remove(template,do_unlink=True)
    for backward,count in [(False,C.BLOOD_PARTICLE_COUNT),(True,C.REGURGITATION_PARTICLE_COUNT)]:
        for i in range(count):
            name=('Regurgitant_RV_to_RA_' if backward else 'Forward_RA_to_RV_')+'Cell_%03d'%i
            o=bpy.data.objects.new(name,data);bpy.context.collection.objects.link(o)
            a=rng.random()*math.tau;rad=math.sqrt(rng.random())*(.22 if backward else .54);offset=rng.random();size=rng.uniform(.022,.040)
            o['illustrative_only']=True;o['direction']='RV -> RA in ventricular systole' if backward else 'RA -> RV in ventricular diastole'
            for frame in range(1,end+2):
                p=((frame-1)%C.CARDIAC_CYCLE_FRAMES)/C.CARDIAC_CYCLE_FRAMES
                lo,hi=(.63,.90) if backward else (.11,.49)
                active=lo<p<hi and (not backward or frame<C.REVEAL_START+20)
                phase=(p-lo)/(hi-lo);t=(phase*1.45*C.FLOW_SPEED+offset)%1
                # Smooth through-plane acceleration; cells follow a connected chamber-to-chamber route.
                travel=t-.08*math.sin(math.tau*t)
                if backward:
                    center=rv*.75*(1-travel/.40) if travel<.40 else ra*1.05*((travel-.40)/.60)
                    spread=.55+travel*.85
                else:
                    center=ra*1.10*(1-travel/.45) if travel<.45 else rv*1.2*((travel-.45)/.55)
                    spread=.75+.35*abs(travel-.45)
                o.location=center+Vector((rad*math.cos(a)*spread,rad*math.sin(a)*spread,0))
                fade=max(0,min(1,t*12,(1-t)*12,(p-lo)*40,(hi-p)*40)) if active else 0
                o.scale=(size*fade,)*3;o.rotation_euler=(a+.7*math.sin(t*6),t*3+i,frame*.018+i)
                o.keyframe_insert('location',frame=frame);o.keyframe_insert('scale',frame=frame);o.keyframe_insert('rotation_euler',frame=frame)
            smooth_keys(o);result.append(o)
    return result

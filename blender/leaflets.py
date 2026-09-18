import bpy,math
import config as C
from utils import mesh,smooth_keys,visible_between

def opening(frame):
    p=((frame-1)%C.CARDIAC_CYCLE_FRAMES)/C.CARDIAC_CYCLE_FRAMES
    # Predominantly diastolic filling, closure 0.48–0.62, systole to .90.
    def ease(t):return t*t*(3-2*t)
    if p<.10:return ease(p/.10)
    if p<.48:return 1.
    if p<.62:return 1-ease((p-.48)/.14)
    if p<.90:return 0.
    return 0. # Reopening begins at next cycle; loop joins continuously.

def coords(u,v,angle,opened,native=False):
    r=C.FRAME_DIAMETER/2-.055
    if native:r=C.TRICUSPID_ANNULUS_DIAMETER/2-.02
    a=angle+u*math.pi/3;co=math.cos(u*math.pi/2)
    outer=(r*math.cos(a),r*math.sin(a),.42-C.LEAFLET_HEIGHT*.87*co)
    # Closed free margin forms a Y with neighboring cusps. Native keeps central gap.
    gap=.24 if native else .0015
    rc=gap+(1-gap)*abs(u)
    ac=angle+(1 if u>=0 else -1)*math.pi/3
    closed=(r*rc*math.cos(ac),r*rc*math.sin(ac),.42*abs(u)**2-.025*co)
    ro=r*(C.OPENING_FRACTION+(1-C.OPENING_FRACTION)*abs(u)**4)
    openedco=(ro*math.cos(a),ro*math.sin(a),.42-C.LEAFLET_HEIGHT*co)
    free=tuple(closed[i]*(1-opened)+openedco[i]*opened for i in range(3))
    x=outer[0]*(1-v)+free[0]*v;y=outer[1]*(1-v)+free[1]*v
    z=outer[2]*(1-v)+free[2]*v-.16*math.sin(math.pi*v)*co
    if native:z-=.12
    return x,y,z

def create(mat,root):
    result=[]
    for native in [False,True]:
        for k in range(3):
            nu=40;nv=18;angle=math.pi/2+k*math.tau/3
            verts=[coords(-1+2*i/nu,j/nv,angle,0,native) for j in range(nv+1) for i in range(nu+1)]
            faces=[]
            for j in range(nv):
                for i in range(nu):
                    q=j*(nu+1)+i;faces.append((q,q+1,q+nu+2,q+nu+1))
            name=('Native_Leaflet_' if native else 'Prosthetic_Leaflet_')+str(k+1)
            o=mesh(name,verts,faces,mat['native' if native else 'leaflet'])
            o.shape_key_add(name='Coapted' if not native else 'Incomplete_Coaptation')
            op=o.shape_key_add(name='Diastolic_Opening')
            for j in range(nv+1):
                for i in range(nu+1):op.data[j*(nu+1)+i].co=coords(-1+2*i/nu,j/nv,angle,1,native)
            for f in range(1,C.ANIMATION_FPS*C.DURATION_SECONDS+2):
                op.value=opening(f);op.keyframe_insert('value',frame=f)
            smooth_keys(o.data.shape_keys)
            sub=o.modifiers.new('Supple curved tissue','SUBSURF');sub.levels=1
            sol=o.modifiers.new('Thin tissue','SOLIDIFY');sol.thickness=C.LEAFLET_THICKNESS
            o['motion']='Illustrative deformation; opens toward RV (-Z) in ventricular diastole.'
            if native:visible_between(o,1,C.REVEAL_START+20)
            else:o.parent=root;result.append(o)
    return result

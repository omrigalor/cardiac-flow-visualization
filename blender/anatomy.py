"""Stylized isolated right-heart cutaway. z+ atrial; z- ventricular."""
import bpy, math
import config as C
from utils import mesh,curve,ring

def shell(name,profiles,mat):
    verts=[];faces=[];N=72
    # Anterior wall deliberately removed to expose intracardiac structures.
    for z,rx,ry,cx,cy in profiles:
        for j in range(N+1):
            a=-.15+(math.pi+.30)*j/N
            ripple=1+.018*math.sin(5*a+z*2)+.012*math.sin(9*a-z)
            verts.append((cx+rx*math.cos(a)*ripple,cy+ry*math.sin(a)*ripple,z))
    for i in range(len(profiles)-1):
        for j in range(N):
            k=i*(N+1)+j;faces.append((k,k+1,k+N+2,k+N+1))
    o=mesh(name,verts,faces,mat['inner']);o.data.materials.append(mat['edge'])
    sub=o.modifiers.new('Organic continuity','SUBSURF');sub.levels=2
    sol=o.modifiers.new('Visible myocardial cut wall','SOLIDIFY');sol.thickness=.105 if 'Atrium' in name else .15;sol.material_offset_rim=1
    bevel=o.modifiers.new('Soft cut edge','BEVEL');bevel.width=.035;bevel.segments=3
    o['anatomy']='Right heart; anterior cutaway; schematic non-patient-specific'
    return o

def create(mat):
    ar=C.RIGHT_ATRIUM_SCALE;vr=C.RIGHT_VENTRICLE_SCALE;r=C.TRICUSPID_ANNULUS_DIAMETER/2
    ra=shell('Right_Atrium',[(.04,r,r*.93,0,0),(.35,1.37,1.16,-.08,0),(.75,ar[0]*.88,ar[1]*.86,-.20,.03),(1.30,ar[0]*.93,ar[1]*.91,-.32,.08),(1.82,1.22,1.02,-.38,.16),(2.20,.78,.68,-.4,.24),(2.41,.46,.44,-.40,.28)],mat)
    rv=shell('Right_Ventricle',[(-.05,r,r*.93,0,0),(-.45,1.50,1.13,.16,0),(-1.10,vr[0],vr[1],.32,.03),(-1.88,vr[0]*.91,vr[1]*.94,.52,.08),(-2.66,1.24,.87,.79,.12),(-3.23,.64,.45,1.02,.12),(-vr[2],.05,.045,1.18,.14)],mat)
    ring('Tricuspid_Annulus',r,0,.092,mat['edge'],.97)
    # Open caval continuation, positioned superiorly, and inferior caval hint.
    for name,pts,rad in [('Superior_Vena_Cava',[(-.4,.28,2.24),(-.43,.31,2.63),(-.46,.35,3.05)],.46),('Inferior_Vena_Cava',[(-1.24,.56,.6),(-1.65,.68,.16),(-1.91,.77,-.34)],.30)]:
        curve(name,pts,rad,mat['tissue'])
    # Fine ventricular trabeculae follow posterior endocardial wall, clear of valve.
    for k in range(10):
        a=.15+(math.pi-.3)*k/9
        pts=[]
        for j in range(28):
            t=j/27;z=-.62-2.48*t;r0=1.60*(1-.68*t)
            pts.append((.22+.76*t+r0*math.cos(a+.10*math.sin(t*5)),.04+1.12*(1-.63*t)*math.sin(a)-.035,z))
        curve('RV_Trabecula_%02d'%k,pts,.034+.011*(k%3),mat['tissue'])
    return ra,rv

def surrounding_tissue(mat):
    """Epicardial surrounding myocardium, no left-heart valve or access model."""
    import random
    from mathutils import Vector
    random.seed(7)
    # Surrounding ventricular myocardial silhouette, exposed outside the cutaway.
    # Asymmetric lateral mass links the right ventricular chamber to an overall heart silhouette.
    verts=[];faces=[];rows=55;cols=88
    for j in range(rows+1):
        t=j/rows;z=.67-4.45*t
        width=1.76*math.sin(math.pi*t)**.68
        cx=.85+.55*t
        for k in range(cols):
            a=k*math.tau/cols
            x=cx+width*math.cos(a);y=.95+width*.70*math.sin(a)
            # Keep the anterior-lateral open RV cavity visible; only surrounding tissue here.
            verts.append((x,y,z))
    for j in range(rows):
        for k in range(cols):
            a=k*math.tau/cols
            if math.cos(a)<-.25 and math.sin(a)<.35:continue
            q=j*cols+k;qn=j*cols+(k+1)%cols;faces.append((q,qn,qn+cols,q+cols))
    o=mesh('Surrounding_Ventricular_Myocardium',verts,faces,mat['tissue'])
    sub=o.modifiers.new('Epicardial continuity','SUBSURF');sub.levels=1
    # Epicardial vessels sweep along the visible lateral heart surface.
    for index in range(5):
        pts=[]
        for j in range(70):
            t=.12+.69*j/69;z=.67-4.45*t;width=1.76*math.sin(math.pi*t)**.68
            a=-.58+index*.30+.10*math.sin(t*8+index)
            pts.append((.85+.55*t+(width+.018)*math.cos(a),.95+(width*.70+.018)*math.sin(a),z))
        curve('Epicardial_Vessel_%02d'%index,pts,.018+.007*(index%2),mat['tissue'])
    # Papillary structures and branching chordae in RV, inset below annulus.
    for k,(x,y,z) in enumerate([(-.67,.46,-1.55),(.88,.50,-1.85),(.12,1.02,-1.43)]):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=16,location=(x,y,z))
        ob=bpy.context.object;ob.name='RV_Papillary_Muscle_'+str(k);ob.scale=(.15,.13,.43);ob.data.materials.append(mat['inner'])
        for p in ob.data.polygons:p.use_smooth=True
        for branch in range(4):
            a=math.pi/2+k*math.tau/3+(branch-1.5)*.13
            curve('Native_Chordae_%d_%d'%(k,branch),[(x,y,z+.32),(x*.75+.10*math.cos(a),y*.7+.13*math.sin(a),-1.0),(.86*math.cos(a),.86*math.sin(a),-.53)],.008,mat['native'])

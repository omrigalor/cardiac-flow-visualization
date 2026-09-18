import bpy
from utils import aim

def create(mat):
    world=bpy.data.worlds.new('Midnight clinical studio');bpy.context.scene.world=world;world.use_nodes=True
    world.node_tree.nodes.get('Background').inputs[0].default_value=(.018,.031,.055,1)
    world.node_tree.nodes.get('Background').inputs[1].default_value=.40
    for name,loc,power,color,size in [
        ('Key_Softbox',(-3.8,-6,7.8),1150,(1,.88,.77),5),
        ('Fill_Softbox',(5,-4,3),850,(.66,.83,1),4),
        ('Rim_Cyan',(2.5,4,5.5),1450,(.38,.77,.89),3),
        ('Tissue_Fill',(-4,1,-1),520,(1,.42,.35),3),
        ('Leaflet_Softbox',(-.5,-1,7),600,(1,.98,.89),3)]:
        d=bpy.data.lights.new(name,'AREA');d.energy=power;d.color=color;d.shape='DISK';d.size=size
        o=bpy.data.objects.new(name,d);bpy.context.collection.objects.link(o);o.location=loc;aim(o,(0,0,0))

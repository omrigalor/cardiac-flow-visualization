import bpy

def material(name,color,metal=0,rough=.4,subsurface=0,noise=False):
    m=bpy.data.materials.new(name); m.diffuse_color=(*color,1); m.use_nodes=True
    n=m.node_tree.nodes; l=m.node_tree.links; p=n.get('Principled BSDF')
    p.inputs['Base Color'].default_value=(*color,1)
    p.inputs['Metallic'].default_value=metal; p.inputs['Roughness'].default_value=rough
    p.inputs['Subsurface Weight'].default_value=subsurface
    p.inputs['Subsurface Radius'].default_value=(1,.28,.16)
    if noise:
        t=n.new('ShaderNodeTexNoise'); t.inputs['Scale'].default_value=38; t.inputs['Detail'].default_value=3
        b=n.new('ShaderNodeBump'); b.inputs['Strength'].default_value=.10; b.inputs['Distance'].default_value=.035
        l.new(t.outputs['Fac'],b.inputs['Height']); l.new(b.outputs['Normal'],p.inputs['Normal'])
        ramp=n.new('ShaderNodeValToRGB'); ramp.color_ramp.elements[0].position=.2; ramp.color_ramp.elements[1].position=.8
        ramp.color_ramp.elements[0].color=(*[x*.62 for x in color],1)
        ramp.color_ramp.elements[1].color=(*[min(1,x*1.22) for x in color],1)
        l.new(t.outputs['Fac'],ramp.inputs[0]); l.new(ramp.outputs[0],p.inputs['Base Color'])
    return m

def create():
    m={}
    m['tissue']=material('Myocardium | burgundy microtexture',(.31,.069,.078),rough=.37,subsurface=.09,noise=True)
    m['inner']=material('Endocardium | warm wet tissue',(.23,.047,.061),rough=.36,subsurface=.10,noise=True)
    m['edge']=material('Cut surface | myocardial wall',(.34,.075,.089),rough=.48,subsurface=.08,noise=True)
    m['metal']=material('Frame | satin neutral alloy',(.58,.65,.72),metal=.92,rough=.23)
    m['leaflet']=material('Leaflets | ivory tissue',(.77,.67,.52),rough=.39,subsurface=.075,noise=True)
    m['native']=material('Native leaflets | collagen',(.53,.30,.25),rough=.42,subsurface=.10,noise=True)
    m['skirt']=material('Skirt | fine woven neutral textile',(.62,.64,.58),rough=.72)
    n=m['skirt'].node_tree.nodes; l=m['skirt'].node_tree.links; p=n.get('Principled BSDF')
    tex=n.new('ShaderNodeTexNoise'); tex.inputs['Scale'].default_value=240
    bump=n.new('ShaderNodeBump'); bump.inputs['Strength'].default_value=.25; bump.inputs['Distance'].default_value=.016
    l.new(tex.outputs['Fac'],bump.inputs['Height']); l.new(bump.outputs[0],p.inputs['Normal'])
    m['flow']=material('Blood | crimson highlights',(.48,.014,.030),metal=.15,rough=.25)
    p=m['flow'].node_tree.nodes.get('Principled BSDF'); p.inputs['Emission Color'].default_value=(.30,.006,.011,1); p.inputs['Emission Strength'].default_value=.3
    m['jet']=material('Regurgitation | warm crimson',(.70,.035,.045),metal=.1,rough=.23)
    m['cyan']=material('Accent | clinical cyan',(.04,.45,.52),metal=.4,rough=.3)
    m['white']=material('Typography | porcelain',(.83,.92,1),rough=.8)
    for key in ['white','cyan']:
        p=m[key].node_tree.nodes.get('Principled BSDF'); p.inputs['Emission Color'].default_value=(*m[key].diffuse_color[:3],1); p.inputs['Emission Strength'].default_value=.7
    m['back']=material('Backdrop | midnight blue',(.007,.015,.029),rough=.95)
    for key in ['tissue','inner','edge','leaflet']:
        n=m[key].node_tree.nodes;l=m[key].node_tree.links;p=n.get('Principled BSDF')
        p.inputs['Coat Weight'].default_value=.13;p.inputs['Coat Roughness'].default_value=.28
        texcoord=n.new('ShaderNodeTexCoord');mapping=n.new('ShaderNodeVectorMath');mapping.operation='MULTIPLY';mapping.inputs[1].default_value=(5,5,110) if key!='leaflet' else (35,4,85)
        fiber=n.new('ShaderNodeTexNoise');fiber.inputs['Scale'].default_value=1.5;fiber.inputs['Detail'].default_value=2
        l.new(texcoord.outputs['Object'],mapping.inputs[0]);l.new(mapping.outputs[0],fiber.inputs['Vector'])
        bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.17 if key!='leaflet' else .08;bump.inputs['Distance'].default_value=.014
        l.new(fiber.outputs['Fac'],bump.inputs['Height'])
        old=p.inputs['Normal'].links[0].from_socket if p.inputs['Normal'].links else None
        if old:l.new(old,bump.inputs['Normal'])
        l.new(bump.outputs[0],p.inputs['Normal'])
    return m

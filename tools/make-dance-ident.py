import bpy,math,os
from pathlib import Path
FRAME_DIR=Path(os.environ.get("DANCE_FRAME_DIR", str(Path(__file__).resolve().parents[1]/"dance-frames")))
FRAME_DIR.mkdir(parents=True,exist_ok=True)
from mathutils import Vector
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=4;s.cycles.use_denoising=False;s.render.resolution_x=512;s.render.resolution_y=512;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.fps=12
s.world.color=(.07,.07,.07)
def mat(name,color,metal=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=.55;p.inputs['Metallic'].default_value=metal;return m
red=mat('Shuttlebug red',(.65,.009,.025));skin=mat('warm skin',(.32,.13,.065));black=mat('charcoal',(.018,.022,.03));white=mat('cream',(.9,.91,.88));floor=mat('stage',(.018,.02,.025))
def sphere(name,loc,scale,material):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=12,location=loc);o=bpy.context.object;o.name=name;o.scale=scale;o.data.materials.append(material)
 for p in o.data.polygons:p.use_smooth=True
 return o
parts={}
parts['body']=sphere('red jacket',(0,0,1.35),(.33,.2,.46),red)
parts['head']=sphere('head',(0,0,2.05),(.24,.21,.28),skin)
parts['hat']=sphere('red cap',(0,0,2.28),(.25,.22,.09),red)
parts['brim']=sphere('cap brim',(0,-.19,2.25),(.27,.19,.025),red)
for side in [-1,1]:
 parts[f'eye{side}']=sphere('eye',(side*.085,-.196,2.09),(.026,.016,.035),black)
 parts[f'shoe{side}']=sphere('white sneaker',(side*.18,-.05,.12),(.13,.23,.1),white)
 parts[f'hand{side}']=sphere('hand',(side*.5,0,1.1),(.1,.085,.12),skin)
for key in ['la','lb','ra','rb','ll','lm','rl','rm']:
 bpy.ops.mesh.primitive_cylinder_add(vertices=16,radius=.09,depth=1);o=bpy.context.object;o.data.materials.append(red if key in ['la','lb','ra','rb'] else black);parts[key]=o
 for p in o.data.polygons:p.use_smooth=True
# Small smile, raised cheeks and ears retain a friendly human cartoon style.
for side in [-1,1]:parts[f'ear{side}']=sphere('ear',(side*.23,0,2.05),(.045,.055,.075),skin)
parts['smile']=sphere('smile',(0,-.205,1.965),(.069,.012,.015),black)
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,0));bpy.context.object.data.materials.append(floor)
for loc,power,size,col in [((3,-4,6),650,5,(1,.88,.8)),((-3,1,4),850,4,(1,.12,.18)),((0,3,5),500,3,(.6,.7,1))]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.data.color=col;o.rotation_euler=(Vector((0,0,1.2))-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(3,-8,3.1));cam=bpy.context.object;cam.rotation_euler=(Vector((0,0,1.25))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=3.35;s.camera=cam
s.view_settings.view_transform='AgX'
def seg(name,a,b,r):
 o=parts[name];a,b=Vector(a),Vector(b);o.location=(a+b)/2;o.scale=(r/.09,r/.09,(b-a).length);o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler()
for frame in range(48):
 t=frame/12;beat=t*math.pi*2*1.5;bob=.055*(1-math.cos(beat*2));sway=.11*math.sin(beat);turn=.07*math.sin(beat)
 for k in ['body','head','hat','brim','eye-1','eye1','ear-1','ear1','smile']:
  o=parts[k];base=o.get('base')
  if base is None:o['base']=list(o.location);base=o['base']
  o.location=(base[0]+sway,base[1],base[2]+bob)
 parts['body'].rotation_euler.y=.12*math.sin(beat)
 for side in [-1,1]:
  phase=beat+(math.pi if side<0 else 0);lift=.14*max(0,math.sin(phase));foot=(side*.2+.07*math.sin(beat),-.08+.12*math.cos(phase),.12+lift);knee=(side*.22+sway*.6,-.07-.12*math.cos(phase),.63+lift*.5);hip=(side*.15+sway,0,1.11+bob)
  parts[f'shoe{side}'].location=foot;seg('ll' if side<0 else 'rl',hip,knee,.12);seg('lm' if side<0 else 'rm',knee,foot,.095)
  shoulder=(side*.29+sway,0,1.65+bob);elbow=(side*.5+sway,-.12+.14*math.cos(phase),1.35+bob+.16*math.sin(phase));hand=(side*.49+sway,-.37,1.62+bob+.24*math.sin(phase));parts[f'hand{side}'].location=hand;seg('la' if side<0 else 'ra',shoulder,elbow,.095);seg('lb' if side<0 else 'rb',elbow,hand,.08)
 s.render.filepath=str(FRAME_DIR/f'{frame:04}.png');bpy.ops.render.render(write_still=True)
 print('DANCE FRAME',frame,flush=True)
 if os.environ.get('TEST_FRAME'):break

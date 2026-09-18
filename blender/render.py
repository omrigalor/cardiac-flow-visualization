import bpy,sys,argparse,struct
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT));import config as C

def settings(preview=True):
    s=bpy.context.scene;s.render.engine='CYCLES' if not preview else 'BLENDER_EEVEE'
    # Metal-enabled Cycles with denoising: robust translucent tissue and metal shading.
    s.cycles.samples=C.PREVIEW_SAMPLES if preview else C.RENDER_SAMPLES;s.cycles.use_denoising=True
    s.cycles.max_bounces=5;s.cycles.diffuse_bounces=2;s.cycles.glossy_bounces=3;s.cycles.transmission_bounces=3
    try:
        prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='METAL';prefs.get_devices()
        for dev in prefs.devices:dev.use=dev.type=='METAL'
        if any(dev.type=='METAL' for dev in prefs.devices):s.cycles.device='GPU'
    except Exception as e:print('CPU fallback:',e)
    s.render.resolution_x=C.PREVIEW_WIDTH if preview else C.RENDER_WIDTH;s.render.resolution_y=C.PREVIEW_HEIGHT if preview else C.RENDER_HEIGHT;s.render.resolution_percentage=100
    s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.image_settings.color_depth='8'
    s.render.fps=C.ANIMATION_FPS;s.render.film_transparent=False
    if hasattr(s,'eevee'):
        if hasattr(s.eevee,'taa_render_samples'):s.eevee.taa_render_samples=16 if preview else 32
    s.render.use_persistent_data=True
    s.view_settings.view_transform='AgX'
    s.render.use_file_extension=True
    s.render.filepath=str(ROOT/'renders/frames/')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--mode',choices=['first','diagnostics','segment','preview','final','stills'],default='first');ap.add_argument('--start',type=int);ap.add_argument('--end',type=int);ap.add_argument('--engine',choices=['CYCLES','BLENDER_EEVEE']);args=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    settings(args.mode not in ['final','stills']);s=bpy.context.scene
    if args.engine:s.render.engine=args.engine
    frames={'whole_heart':35,'native_TR':196,'prosthesis_open':380,'prosthesis_closing':400,'prosthesis_closed':415,'hero':630}
    if args.mode=='first':
        s.render.resolution_percentage=50;s.cycles.samples=8;s.frame_set(380);s.render.filepath=str(ROOT/'renders/diagnostics/first.png');bpy.ops.render.render(write_still=True)
    elif args.mode in ['diagnostics','stills']:
        folder='stills' if args.mode=='stills' else 'diagnostics'
        for name,f in frames.items():
            s.frame_set(f)
            if args.mode=='stills' and name.startswith('prosthesis_'):
                s.camera=bpy.data.objects['Valve_Atrial_View']
            s.render.filepath=str(ROOT/'renders'/folder/(name+'.png'));bpy.ops.render.render(write_still=True)
    else:
        folder='frames' if args.mode=='final' else 'previews/'+args.mode
        out=ROOT/'renders'/folder;out.mkdir(parents=True,exist_ok=True)
        start=args.start or (361 if args.mode=='segment' else 1);end=args.end or (432 if args.mode=='segment' else s.frame_end)
        for f in range(start,end+1):
            path=out/('%04d.png'%f)
            if (ROOT/'renders/STOP_RENDER').exists():
                print('Graceful render stop requested; completed PNGs preserved.',flush=True);break
            if path.exists():
                dimensions=struct.unpack('>II',path.read_bytes()[16:24])
                if dimensions!=(s.render.resolution_x,s.render.resolution_y):raise RuntimeError('Existing frame resolution differs; archive that sequence before rerendering.')
                continue
            s.frame_set(f);s.render.filepath=str(path);bpy.ops.render.render(write_still=True)
if __name__=='__main__':main()

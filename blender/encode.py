"""Encode PNGs to H.264 and append a separate branded end card (Pillow generated)."""
import argparse,subprocess,sys,struct
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT));import config as C

def main():
    import imageio_ffmpeg
    p=argparse.ArgumentParser();p.add_argument('--source',default='renders/previews/preview');p.add_argument('--output',default='renders/previews/concept_preview.mp4');p.add_argument('--start',type=int,default=1);p.add_argument('--internal',action='store_true');p.add_argument('--no-endcard',action='store_true');a=p.parse_args()
    ff=imageio_ffmpeg.get_ffmpeg_exe();out=ROOT/a.output;out.parent.mkdir(parents=True,exist_ok=True)
    first=ROOT/a.source/('%04d.png'%a.start)
    with first.open('rb') as f:
        header=f.read(24);width,height=struct.unpack('>II',header[16:24])
    args=[ff,'-y','-framerate',str(C.ANIMATION_FPS),'-start_number',str(a.start),'-i',str(ROOT/a.source/'%04d.png')]
    if not a.no_endcard:
        card=ROOT/'assets/branding'/('endcard_internal.png' if a.internal else 'endcard_clean.png')
        args+=['-loop','1','-framerate',str(C.ANIMATION_FPS),'-i',str(card),'-filter_complex',f'[0:v]trim=end_frame={C.ANIMATION_FPS*C.DURATION_SECONDS},setpts=PTS-STARTPTS,setsar=1,format=yuv420p[v0];[1:v]scale={width}:{height},setsar=1,format=yuv420p,trim=duration=3,setpts=PTS-STARTPTS[v1];[v0][v1]concat=n=2:v=1:a=0[v]','-map','[v]']
    args+=['-r',str(C.ANIMATION_FPS),'-fps_mode','cfr','-c:v','libx264','-crf','17','-preset','medium','-pix_fmt','yuv420p','-movflags','+faststart',str(out)]
    subprocess.run(args,check=True)
if __name__=='__main__':main()

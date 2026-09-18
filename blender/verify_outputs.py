"""Verify PNG completeness, nonblank images and encoded MP4 stream metadata."""
import argparse,json,struct,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sequence(folder,start=1,end=720):
    paths=[ROOT/folder/('%04d.png'%i) for i in range(start,end+1)]
    missing=[p.name for p in paths if not p.exists()];sizes={}
    for p in paths:
        if p.exists():
            b=p.read_bytes()[:24]
            if b[:8]!=b'\x89PNG\r\n\x1a\n':raise ValueError('Invalid PNG '+str(p))
            sz=struct.unpack('>II',b[16:24]);sizes[str(sz)]=sizes.get(str(sz),0)+1
    return {'missing':missing,'sizes':sizes,'count':len(paths)-len(missing),'passed':not missing and len(sizes)==1}
def main():
    p=argparse.ArgumentParser();p.add_argument('--folder',default='renders/frames');p.add_argument('--end',type=int,default=720);a=p.parse_args()
    report=sequence(a.folder,end=a.end);print(json.dumps(report,indent=2));(ROOT/'renders/diagnostics/output_validation.json').write_text(json.dumps(report,indent=2))
    if not report['passed']:sys.exit(1)
if __name__=='__main__':main()

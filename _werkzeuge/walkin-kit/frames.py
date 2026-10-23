"""Clips -> Scroll-Frames.  Aufruf:  python3 frames.py <ordner_mit_clips> <ausgabe_ordner> clip1.mp4 clip2.mp4 ...
Nimmt jedes 2. Bild (12/s), 1280x720 WebP q60, Grenzbild zwischen Clips nur einmal.
Gibt Anzahl Frames + Grenzen je Clip aus -> damit tour.json (TM) füllen."""
import subprocess,glob,os,sys,tempfile
from PIL import Image
src,out,clips=sys.argv[1],sys.argv[2],sys.argv[3:]
os.makedirs(out,exist_ok=True)
for f in glob.glob(out+'/*.webp'): os.remove(f)
seq=[];bounds=[]
for ci,c in enumerate(clips):
    tmp=tempfile.mkdtemp()
    subprocess.run(['ffmpeg','-v','error','-y','-i',os.path.join(src,c),'-vf','scale=1280:720:flags=lanczos,eq=contrast=1.03:saturation=1.05','-q:v','2',tmp+'/%04d.jpg'],check=True)
    fs=sorted(glob.glob(tmp+'/*.jpg')); pick=fs[::2]
    if fs[-1] not in pick: pick.append(fs[-1])
    if ci>0: pick=pick[1:]
    bounds.append((len(seq),len(seq)+len(pick)-1)); seq+=pick
for i,f in enumerate(seq): Image.open(f).save(f'{out}/{i:03d}.webp','WEBP',quality=60,method=5)
print(len(seq),'Frames · Grenzen je Clip:',bounds)

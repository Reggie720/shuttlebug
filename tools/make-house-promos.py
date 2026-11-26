"""Build original text/shape house promos; no third-party film, music or voices."""
from pathlib import Path
import subprocess
root=Path(__file__).resolve().parents[1]
out=root/'originals';out.mkdir(exist_ok=True)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
regular='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def text(s,size,y,start,end,color='white',bold=True):
    # Fixed production strings only; no untrusted inputs.
    return f"drawtext=fontfile='{font if bold else regular}':text='{s}':fontsize={size}:fontcolor={color}:x=(w-tw)/2:y={y}:enable='between(t,{start},{end})'"
def render(name,duration,lines):
    filters=['drawbox=x=0:y=0:w=iw:h=18:color=0xd81928:t=fill','drawbox=x=140:y=910:w=1640:h=2:color=0x393941:t=fill',text('A HOG ENTERTAINMENT',25,965,0,duration,'0xbdbdc9',False)]
    for args in lines:filters.append(text(*args))
    filters+=['fade=t=in:st=0:d=0.4',f'fade=t=out:st={duration-.45}:d=0.45','format=yuv420p']
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','lavfi','-i',f'color=c=0x101115:s=1920x1080:r=30:d={duration}','-f','lavfi','-i',f'anullsrc=r=48000:cl=stereo','-vf',','.join(filters),'-c:v','libx264','-preset','fast','-crf','19','-c:a','aac','-b:a','96k','-t',str(duration),'-movflags','+faststart',str(out/name)],check=True)
render('Shuttlebug_Promo_20s_1080p.mp4',20,[
 ('SHUTTLEBUG',115,325,0,4.99),('Find your next independent story.',46,515,0,4.99,'0xff7781',False),
 ('FREE TO WATCH',100,325,5,9.99),('Independent films. Documentary series.',47,505,5,9.99,'white',False),('No subscription. No account required.',37,610,5,9.99,'0xbdbdc9',False),
 ('MAKE IT MOVIE TIME',94,325,10,14.99),('Browse. Save favorites. Keep watching.',46,515,10,14.99,'white',False),
 ('WATCH SHUTTLEBUG',94,300,15,20),('shuttlebug.onrender.com',63,490,15,20,'0xff7781'),('Internet required. Titles and availability may change.',29,640,15,20,'0xbdbdc9',False)])
render('Shuttlebug_Ident_6s_1080p.mp4',6,[('SHUTTLEBUG',125,345,0,6),('Independent stories. Your screen.',47,535,0,6,'0xff7781',False)])
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss','1','-i',str(out/'Shuttlebug_Promo_20s_1080p.mp4'),'-frames:v','1',str(out/'promo-poster.jpg')],check=True)
print('Built 20-second promo and 6-second ident in 1080p; silent by design.')

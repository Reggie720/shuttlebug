"""Render a new, provisional opening-scene animation. No old screenplay is overwritten.
Requires Python/Pillow/numpy and ffmpeg built with libflite. No paid APIs or remote assets.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np, math, random, pathlib, subprocess, wave, json, tempfile
ROOT=pathlib.Path(__file__).resolve().parents[1]; OUT=ROOT/'media/originals';OUT.mkdir(parents=True,exist_ok=True)
W,H,FPS,DUR=960,540,15,44
TMP=pathlib.Path(tempfile.mkdtemp(prefix='shuttlebug-scene-'))
FONT='/usr/share/fonts/truetype/open-sans/OpenSans-Regular.ttf';BOLD='/usr/share/fonts/truetype/open-sans/OpenSans-Bold.ttf'
def font(s,b=False):return ImageFont.truetype(BOLD if b else FONT,s)
LINES=[(6,'Marcus','rms','Same block. Same windows. But today, everything feels different.'),(14,'Denise','slt','Marcus. The car is downstairs. You got your notebook?'),(19,'Marcus','rms','Yeah, Ma. I got it.'),(23,'Marcus','rms','A new city does not mean a new me. Just a new place to be heard.'),(32,'Denise','slt','Then let us go find your next chapter.')]
SR=44100;N=SR*DUR;audio=np.zeros(N,dtype=np.float64);speech=[]
for i,(start,speaker,voice,line) in enumerate(LINES):
 text=TMP/f'line{i}.txt';text.write_text(line);wav=TMP/f'line{i}.wav'
 subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i',f'flite=textfile={text}:voice={voice}','-ar',str(SR),'-ac','1','-y',str(wav)],check=True)
 with wave.open(str(wav)) as f:a=np.frombuffer(f.readframes(f.getnframes()),dtype=np.int16).astype(float)/32768
 a=a/max(.01,np.max(np.abs(a)))*.68;index=int(start*SR);audio[index:index+len(a)]+=a;speech.append((start,start+len(a)/SR,speaker,line,a))
# Original instrumental cue: quiet minor-key keys, bass, a restrained beat, and synthesized city air.
rng=np.random.default_rng(72);t=np.arange(N)/SR;music=np.zeros(N)
def note(freq,start,length,gain):
 a=int(start*SR);n=min(int(length*SR),N-a)
 if n<=0:return
 z=np.arange(n)/SR;env=(1-np.exp(-z*35))*np.exp(-z*1.4)
 music[a:a+n]+=gain*env*(np.sin(2*np.pi*freq*z)+.22*np.sin(2*np.pi*2*freq*z)+.08*np.sin(2*np.pi*3*freq*z))
chords=[[130.81,155.56,196],[103.83,130.81,155.56],[87.31,103.83,130.81],[98,123.47,146.83]]
for bar in range(15):
 st=bar*3.0
 for j,f in enumerate(chords[bar%4]):note(f*2,st+.1*j,2.7,.018)
 note(chords[bar%4][0]/2,st,2.5,.025)
 for beat in range(4):
  a=int((st+beat*.75)*SR);n=min(int(.14*SR),N-a)
  if n>0:
   z=np.arange(n)/SR;music[a:a+n]+=.016*np.sin(2*np.pi*(55*z+9*(1-np.exp(-z*30))))*np.exp(-z*25)
# Low-level air and a distant train rumble, synthesized rather than sampled.
noise=rng.normal(0,1,N);air=np.convolve(noise,np.ones(90)/90,mode='same')*.017
fade=np.minimum(1,t/2)*np.minimum(1,np.maximum(0,(DUR-t)/3));mix=(audio+music+air)*fade;mix=np.clip(mix,-.96,.96)
with wave.open(str(TMP/'mix.wav'),'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(SR);f.writeframes((mix*32767).astype(np.int16).tobytes())
# Layered, hand-built 2D character and background artwork.
random.seed(12)
def gradient(top,bottom):
 arr=np.zeros((H,W,3),dtype=np.uint8)
 for y in range(H):arr[y,:,:]=np.array(top)*(1-y/H)+np.array(bottom)*(y/H)
 return Image.fromarray(arr)
SKY=gradient((45,49,75),(239,168,112))
def city(t,wide=False):
 im=SKY.copy();d=ImageDraw.Draw(im);d.ellipse((720,75,815,170),fill='#ebbf8a')
 for depth,col in [(0,'#636174'),(1,'#454554'),(2,'#262a3b')]:
  r=random.Random(10+depth);x=-80
  while x<W+80:
   bw=r.randrange(45,110);bh=r.randrange(90+depth*25,210+depth*70);base=400+depth*40;top=base-bh
   d.rectangle((x,top,x+bw,base),fill=col);d.line((x,top,x+bw,top),fill='#a99087',width=2)
   for wx in range(x+9,x+bw-5,15):
    for wy in range(top+13,base-10,24):
     if r.random()>.35:d.rectangle((wx,wy,wx+5,wy+10),fill=['#b79b79','#8f8f9c','#dfb47b'][r.randrange(3)])
   if depth==2:
    for by in range(top+40,base,50):d.line((x+5,by,x+bw-8,by),fill='#171d2b',width=3)
   x+=bw+7
 d.rectangle((0,452,W,H),fill='#1c2331');d.rectangle((0,466,W,476),fill='#616074')
 trainx=int((t*63)%1350)-400
 for c in range(4):
  xx=trainx+c*165;d.rounded_rectangle((xx,418,xx+160,460),8,fill='#868e99',outline='#a9a7a8',width=2)
  for k in range(6):d.rectangle((xx+12+k*23,426,xx+27+k*23,443),fill='#2d354a')
  d.line((xx+5,450,xx+155,450),fill='#ac4641',width=3)
 d.line((0,478,W,478),fill='#0f1725',width=7)
 for i in range(3):
  bx=(t*14+i*105)%W;by=100+i*14;d.line((bx-5,by,bx,by+3,bx+5,by),fill='#3b4357',width=1)
 return im
ROOM=gradient((110,87,78),(58,48,50));d=ImageDraw.Draw(ROOM)
d.rectangle((0,0,W,378),fill='#77615b');d.rectangle((0,379,W,H),fill='#49414a');d.polygon([(0,378),(960,378),(960,540),(0,540)],fill='#4a3939')
for x in range(-900,1700,140):d.line((480,260,x,540),fill='#6b4b40',width=2)
for y in [395,426,469,523]:d.line((0,y,W,y),fill='#6b4b40',width=2)
d.rectangle((64,61,465,327),fill='#272f3d');d.rectangle((56,50,473,62),fill='#d2ab87');d.rectangle((55,322,474,339),fill='#d2ab87')
d.polygon([(465,218),(825,378),(700,540),(130,540)],fill='#795849')
d.rectangle((754,78,939,378),fill='#3c3941');d.rectangle((772,89,930,378),fill='#252a36');d.rectangle((752,68,950,79),fill='#b9977d')
d.rectangle((537,122,672,215),fill='#b79e87');d.rectangle((548,133,661,204),fill='#433c4b');d.line((560,190,590,155,620,174,651,143),fill='#b96a4c',width=4)
# Stacked moving boxes, suitcase, travel tag.
for x,y,ww,hh in [(30,370,130,92),(145,385,110,88),(602,356,113,87)]:
 d.rectangle((x,y,x+ww,y+hh),fill='#b58b63',outline='#604a3f',width=3);d.rectangle((x+ww/2-8,y,x+ww/2+8,y+hh),fill='#c6a981');d.line((x,y+8,x+ww,y+8),fill='#745a46',width=2)
d.text((38,397),'MEMPHIS',font=font(13,True),fill='#523d34')
d.rounded_rectangle((713,397,793,470),9,fill='#243343',outline='#617080',width=3);d.arc((733,380,774,410),180,360,fill='#8d929b',width=5)
d.polygon([(774,409),(797,420),(785,445),(763,432)],fill='#d3ae77');d.text((770,417),'M',font=font(13,True),fill='#55434a')

def mouth_amount(t,speaker):
 for a,b,s,line,w in speech:
  if s==speaker and a<=t<b:
   idx=int((t-a)*SR);seg=w[max(0,idx-400):idx+400];return min(1,float(np.sqrt(np.mean(seg*seg)))*6)
 return 0

def character(t,who):
 im=Image.new('RGBA',(350,500));d=ImageDraw.Draw(im);mom=who=='Denise';skin='#9f6243' if mom else '#a5694c';edge='#372d34';shade='#754834';shirt='#263b4c' if mom else '#a43d3e';pants='#293447';bob=math.sin(t*2.2)*1.5
 # shoes, trousers and knees; relaxed stance shifts with breath.
 for x in [131,193]:
  d.polygon([(x-16,326),(x+17,326),(x+12,451),(x-18,451)],fill=pants,outline=edge)
  d.rounded_rectangle((x-24,439,x+27,464),8,fill='#242833',outline='#77818b',width=2);d.line((x-20,458,x+25,458),fill='#d2c5b4',width=4)
 # torso, shoulder seam, cardigan or red hoodie.
 d.rounded_rectangle((102,192+bob,232,342+bob),25,fill=shirt,outline=edge,width=3)
 if mom:d.polygon([(148,193),(185,193),(195,337),(139,337)],fill='#ca944d');d.line((165,207,166,340),fill='#203141',width=2)
 else:
  d.arc((126,180+bob,209,238+bob),0,180,fill='#d18f77',width=3)
  for x in [155,185]:d.line((x,215+bob,x-2,263+bob),fill='#e4d0ba',width=3)
  d.rounded_rectangle((131,281+bob,206,316+bob),8,outline='#79363d',width=3)
 # arms and animated gesturing hand. Rounded strokes form continuous cutout joints.
 talk=mouth_amount(t,who);gesture=.5+.5*math.sin(t*2.1)
 left=[(110,218+bob),(90,274+bob),(119,294+bob)]
 right=[(222,219+bob),(249,271+bob),(231-(22 if talk>.1 else 0),312-(40*gesture if talk>.1 else 0))]
 for arm in [left,right]:
  d.line(arm,fill=edge,width=29,joint='curve');d.line(arm,fill=shirt,width=23,joint='curve');x,y=arm[-1];d.ellipse((x-12,y-12,x+12,y+12),fill=skin,outline=shade,width=2)
 if not mom:
  d.polygon([(104,271),(160,259),(176,307),(119,319)],fill='#e6c99b',outline='#342e38');d.line((112,277,163,267),fill='#624e49',width=3);d.text((116,285),'BARS',font=font(10,True),fill='#684e4b')
 # neck and softly tilted head.
 d.rounded_rectangle((149,162+bob,186,211+bob),9,fill=shade)
 head=Image.new('RGBA',(190,190));h=ImageDraw.Draw(head)
 h.ellipse((37,72,57,105),fill=skin,outline=shade,width=2);h.ellipse((139,72,158,105),fill=skin,outline=shade,width=2)
 h.rounded_rectangle((50,32,147,155),42,fill=skin,outline=edge,width=3)
 h.pieslice((49,35,146,155),90,180,fill='#965b42')
 if mom:
  h.ellipse((39,7,155,78),fill='#242632');h.ellipse((44,20,76,108),fill='#242632');h.ellipse((127,20,158,110),fill='#242632')
  for cx,cy in [(51,26),(76,14),(103,12),(129,23),(45,57),(145,55)]:h.ellipse((cx-16,cy-13,cx+16,cy+13),fill='#2e2c36',outline='#42404a',width=1)
  for x in [46,150]:h.ellipse((x-7,100,x+7,119),outline='#d7ae5f',width=3)
 else:
  h.rounded_rectangle((48,20,149,62),20,fill='#262633')
  rr=random.Random(7)
  for k in range(35):
   x=rr.randrange(54,144);y=rr.randrange(20,55);h.ellipse((x-6,y-6,x+6,y+6),fill=['#252632','#31313c','#3c3840'][k%3])
 blink=(t%4.7<.14);gaze=2 if (t>13 and not mom) else 0
 for x in [77,120]:
  h.line((x-11,72,x+9,70),fill='#392f35',width=3)
  if blink:h.line((x-9,87,x+9,87),fill='#3d3035',width=3)
  else:
   h.ellipse((x-10,80,x+10,91),fill='#e9d6bd');h.ellipse((x-3+gaze,80,x+4+gaze,91),fill='#352d33');h.ellipse((x-1+gaze,81,x+1+gaze,84),fill='white')
 h.line((99,88,95,108,104,110),fill=shade,width=2)
 hh=2+talk*13
 h.ellipse((82,124-hh/2,115,124+hh/2),fill='#48292e',outline='#673a36')
 if talk>.25:h.rectangle((86,120-hh/2,111,124-hh/2),fill='#dfcab6')
 else:h.line((84,125,110,125),fill='#d28b77',width=2)
 angle=math.sin(t*1.7)*1.4+(2*math.sin(t*3) if talk>.15 else 0);head=head.rotate(angle,Image.Resampling.BICUBIC)
 im.alpha_composite(head,(71,int(33+bob)))
 return im

def room(t):
 im=ROOM.copy().convert('RGBA');window=city(t).crop((120,80,760,510)).resize((395,255)).convert('RGBA');im.alpha_composite(window,(67,66))
 d=ImageDraw.Draw(im);d.rectangle((250,65,263,323),fill='#bba087');d.rectangle((66,180,462,190),fill='#bba087');d.rectangle((54,323,476,339),fill='#d4b394')
 # Both characters are visible. Denise enters from the door as she calls Marcus.
 mom=character(t,'Denise').resize((211,302),Image.Resampling.LANCZOS)
 x=int(740-max(0,min(1,(t-12)/3))*110);im.alpha_composite(mom,(x,139))
 marcus=character(t,'Marcus').resize((285,407),Image.Resampling.LANCZOS);im.alpha_composite(marcus,(292,92))
 return im.convert('RGB')

def centered(d,text,y,size,color='white',bold=False):
 f=font(size,bold);box=d.textbbox((0,0),text,font=f);d.text(((W-box[2])/2,y),text,font=f,fill=color)

def frame(t):
 if t<5:
  im=city(t);d=ImageDraw.Draw(im);d.rectangle((0,0,W,H),fill=None);shade=Image.new('RGB',(W,H),'#10131f');im=Image.blend(im,shade,.25);d=ImageDraw.Draw(im)
  d.text((62,80),'SHUTTLEBUG ORIGINAL',font=font(17,True),fill='#ebaa7c');d.text((60,118),'FROM THE BLOCK',font=font(49,True),fill='#fff1df');d.text((60,174),'TO THE BEACH',font=font(49,True),fill='#fff1df');d.text((63,254),'EPISODE 1  /  THE MOVE',font=font(20,True),fill='#efb692');d.text((64,300),'NEW YORK  ·  MORNING',font=font(14),fill='#d1bcae')
 elif t<12:
  im=room(t);z=1+(t-5)*.012
  cw=int(W/z);ch=int(H/z);im=im.crop((int((W-cw)*.45),int((H-ch)*.48),int((W-cw)*.45)+cw,int((H-ch)*.48)+ch)).resize((W,H),Image.Resampling.LANCZOS)
 elif t<19:
  im=room(t);im=im.crop((390,80,950,395)).resize((W,H),Image.Resampling.LANCZOS)
 elif t<31:
  im=room(t);im=im.crop((240,89,725,362)).resize((W,H),Image.Resampling.LANCZOS)
 elif t<38:
  im=room(t);z=1.03-(t-31)*.004;cw=int(W/z);ch=int(H/z);im=im.crop((0,0,cw,ch)).resize((W,H),Image.Resampling.LANCZOS)
 else:
  im=city(t);im=Image.blend(im,Image.new('RGB',(W,H),'#111320'),.62);d=ImageDraw.Draw(im);centered(d,'THE MOVE',170,60,bold=True);centered(d,'Opening scene preview',253,23,'#e6b28d');centered(d,'Draft animation · Temporary synthetic voices',304,15,'#cebfba');centered(d,'Full Episode 1 remains in production',332,15,'#cebfba')
 # Cinematic bars plus small, honest production label.
 d=ImageDraw.Draw(im);d.rectangle((0,0,W,34),fill='#10131c');d.rectangle((0,H-34,W,H),fill='#10131c');d.text((24,10),'SHUTTLEBUG  /  THE MOVE',font=font(11,True),fill='#d7c6b4');d.text((W-183,10),'SCENE PREVIEW · DRAFT',font=font(10,True),fill='#c5b6af')
 # Burned-in accessible dialogue, also supplied as selectable WebVTT.
 for a,b,s,line,_ in speech:
  if a<=t<=b+.15:
   f=font(19,True);words=(s.upper()+': '+line).split();lines=[];line1=''
   for word in words:
    test=line1+' '+word
    if d.textlength(test,font=f)>W-100:lines.append(line1.strip());line1=word
    else:line1=test
   lines.append(line1.strip());yy=H-58-25*(len(lines)-1)
   for line in lines:
    bbox=d.textbbox((0,0),line,font=f);x=(W-bbox[2])/2;d.rounded_rectangle((x-10,yy-3,x+bbox[2]+10,yy+26),5,fill='#181923');d.text((x,yy),line,font=f,fill='#fff0dc');yy+=25
 fade=min(1,t/1.2,(DUR-t)/1.2)
 if fade<1:im=Image.blend(Image.new('RGB',(W,H),'black'),im,max(0,fade))
 return im

# Render a genuine MP4, not a slideshow or a browser-only animation.
proc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-i',str(TMP/'mix.wav'),'-c:v','libx264','-preset','medium','-crf','25','-pix_fmt','yuv420p','-c:a','aac','-b:a','96k','-movflags','+faststart','-shortest',str(OUT/'the-move-scene-1-preview.mp4')],stdin=subprocess.PIPE)
for i in range(FPS*DUR):
 t=i/FPS;im=frame(t);proc.stdin.write(im.tobytes())
 if i%150==0:print(f'Rendered {i}/{FPS*DUR}',flush=True)
proc.stdin.close();assert proc.wait()==0
frame(25).save(OUT/'the-move-scene-1-poster.jpg',quality=90)
def stamp(t):return f'{int(t//3600):02}:{int(t//60)%60:02}:{int(t)%60:02}.{int((t%1)*1000):03}'
(OUT/'the-move-scene-1.en.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(f'{i+1}\n{stamp(a)} --> {stamp(b)}\n{s}: {line}' for i,(a,b,s,line,_) in enumerate(speech))+'\n')
(ROOT/'production/the-move-scene-1.md').write_text('''# From the Block to the Beach — The Move\n\n## Opening scene preview, revision 1\n\nThis is NEW provisional dialogue based on the recovered synopsis and character names Marcus and Denise. The earlier expanded screenplay was not found in the saved app files. This preview does not reproduce or replace that missing screenplay. Do not label it as the complete 35-minute episode.\n\nStyle: original 2D cutout animation, New York sunrise and apartment departure. Animated city/train, character entrance, gestures, head motion, blinking and audio-driven mouths. Temporary generic libflite synthetic voices; original procedural instrumental and ambient sound. No external art, licensed songs, celebrity voices or purchased assets.\n\n'''+ '\n\n'.join(f'{a:.1f}–{b:.1f}s — **{s}:** {line}' for a,b,s,line,_ in speech)+'\n\nNext: recover/confirm the full screenplay, refine character designs and replace temporary voices before producing the remaining scenes.\n')
print('COMPLETE',OUT/'the-move-scene-1-preview.mp4',flush=True)

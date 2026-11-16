"""Manually reviewed titles only. Never synthesize narration or republish the canceled original."""
import json,pathlib,urllib.request,urllib.parse,subprocess,concurrent.futures
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'media/library';OUT.mkdir(parents=True,exist_ok=True)
CAT=ROOT/'catalog.js';catalog=json.loads(CAT.read_text().split('=',1)[1].rstrip(';\n'))
DATE='2026-11-16'
BLENDER=[
 ('spring','Spring','3d95fb3d-c866-42c8-9db1-fe82f48ccb95',2019,'Adventure','A shepherd girl and her dog awaken ancient spirits and bring a frozen valley back to life.','https://studio.blender.org/projects/spring/pages/about/','No dialogue','no-dialogue',None),
 ('cosmos','Cosmos Laundromat: First Cycle','f507dfdc-e73e-45a4-9778-d758cbe1ce96',2015,'Fantasy','A mysterious visitor offers a lonely sheep a chance to experience a completely different life.','https://gooseberry.blender.org/license/','English','recorded-human','Unrated · Mature themes, including a suicide attempt')
]
FILENAMES=['BBS 1.01 Baud.mp4','BBS 1.02 Sysops and Users.mp4','BBS 2.01 Make It Pay.mp4','BBS 2.02 Fidonet.mp4','BBS 2.03 Artscene.mp4','BBS 3.01 HPAC.mp4','BBS 3.02 No Carrier.mp4','BBS 3.03 Compression.mp4']
NAMES=['Baud','Sysops and Users','Make It Pay','Fidonet','Artscene','HPAC','No Carrier','Compression']
DESCRIPTIONS=[
 'Meet the pioneers who connected computers over telephone lines and started the earliest online communities.',
 'Operators and callers share their memories of building friendships, handling problems, and running a bulletin board.',
 'The rise of commercial bulletin boards, told by the people who tried to turn online communities into businesses.',
 'A look at the volunteer network that carried messages between bulletin boards around the world.',
 'Meet the artists who used text characters and color to create a distinctive online art movement.',
 'People from the hacking, phreaking, anarchist and cracking communities recall the dial-up underground.',
 'Participants reflect on the changing role of dial-up communities as the Internet grew.',
 'The people behind early file-compression tools revisit a dispute that changed the software industry.'
]
def get(url):
 with urllib.request.urlopen(url,timeout=30) as r:return json.load(r)
def probe(url):
 p=subprocess.run(['ffprobe','-v','error','-rw_timeout','20000000','-show_entries','format=duration:stream=codec_name,codec_type,width,height','-of','json',url],capture_output=True,text=True,check=True,timeout=65)
 d=json.loads(p.stdout);assert any(s.get('codec_name')=='h264' for s in d['streams']);assert any(s.get('codec_name')=='aac' for s in d['streams']);return d
def still(url,id,at='120'):
 subprocess.run(['ffmpeg','-v','error','-y','-ss',at,'-i',url,'-frames:v','1','-vf','scale=640:-1','-q:v','3',str(OUT/(id+'.jpg'))],capture_output=True,check=True,timeout=90)
def blender(item):
 id,title,uuid,year,genre,description,rights,language,audio,advisory=item
 api='https://video.blender.org/api/v1/videos/'+uuid;d=get(api)
 assert d['channel']['name']=='blender_open_movies'
 files=sorted([f for f in d['files'] if f['resolution']['id'] in [360,480,720]],key=lambda f:f['resolution']['id'])
 url=next(f['fileUrl'] for f in files if f['resolution']['id']==480);verified=probe(url);still(url,id,'100')
 # Both official film closing cards explicitly state Creative Commons Attribution 4.0.
 # Spring's API tag differs; the actual film card at ~456s is the permission record.
 m=dict(id=id,title=title,type='Movies',genre=genre,year=year,series=None,episode=None,duration=float(verified['format']['duration']),description=description,image='/media/library/'+id+'.jpg',sources=[dict(label=f['resolution']['label'],url=f['fileUrl']) for f in files],captions=[],credit='© Blender Foundation | '+('cloud.blender.org/spring' if id=='spring' else 'gooseberry.blender.org'),license='CC BY 4.0',licenseUrl='https://creativecommons.org/licenses/by/4.0/',rights=rights,source=d['url'],rightsRecord=api,checked=DATE,added=DATE,collection='new-2026-11-16',language=language,audioType=audio,audioEvidence=('https://studio.blender.org/projects/spring/pages/about/' if id=='spring' else 'https://gooseberry.blender.org/about/'),changes='Complete original film and recorded soundtrack with closing credits. Streaming encode; thumbnail is a cropped film frame. No new narration or dub.')
 if advisory:m['advisory']=advisory
 print('Verified',id,m['duration'],flush=True);return m

def bbs(n):
 id='bbs'+str(n);filename=FILENAMES[n-1];url='https://archive.org/download/ddff-bbs-the-documentary/'+urllib.parse.quote(filename)
 d=probe(url);h=next(s['height'] for s in d['streams'] if s['codec_type']=='video');assert h==480
 still(url,id)
 m=dict(id=id,title='BBS: The Documentary — '+NAMES[n-1],type='TV',genre='Documentary',year=2005,series='BBS: The Documentary',episode=n,duration=float(d['format']['duration']),description=DESCRIPTIONS[n-1],image='/media/library/'+id+'.jpg',sources=[dict(label='480p',url=url),dict(label='240p',url=f'https://archive.org/download/BBS.The.Documentary/BBS.The.Documentary.ep{n}_512kb.mp4')],cors=False,captions=[],credit='BBS: The Documentary · Jason Scott / TEXTFILES.COM · Original interview participants credited in the film',license='CC BY-SA 2.0',licenseUrl='https://creativecommons.org/licenses/by-sa/2.0/',rights='https://ascii.textfiles.com/archives/865',source='https://archive.org/details/ddff-bbs-the-documentary',rightsRecord='https://ascii.textfiles.com/archives/865',checked=DATE,added=DATE,collection='new-2026-11-16',language='English',audioType='recorded-human',audioEvidence='https://ascii.textfiles.com/archives/865',qualityNote='Archival standard-definition footage',changes='Complete documentary episode with original interviews, soundtrack and credits. Internet Archive streaming encode; thumbnail is a cropped film frame. No new narration or dub.')
 print('Verified',id,m['duration'],flush=True);return m
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 new=list(ex.map(blender,BLENDER))+list(ex.map(bbs,range(1,9)))
assert all(m['audioType'] in ['recorded-human','no-dialogue'] for m in new)
ids={m['id'] for m in new};catalog=[m for m in catalog if m['id'] not in ids and m['id'] not in ['block','block-scene-1']]+new
CAT.write_text('window.SHUTTLEBUG_CATALOG = '+json.dumps(catalog,indent=2)+';\n')
print('Added',len(new),'titles; catalog total',len(catalog),'duration',round(sum(m['duration'] for m in new)/3600,2),'hours',flush=True)

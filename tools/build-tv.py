"""Build packaged webOS UI; retain hosted media URLs and exact web catalog rights gate."""
from pathlib import Path
import json,re,shutil
root=Path(__file__).resolve().parents[1];out=root/'.tv-build';out.mkdir(exist_ok=True)
for name in ['app.js','catalog.js','config.js','styles.css','video-ads.js']:
 s=(root/name).read_text()
 if name=='catalog.js':s=re.sub(r'"/(captions|media)/',r'"https://shuttlebug.onrender.com/\1/',s)
 if name=='video-ads.js':s=s.replace("location.origin","'https://shuttlebug.onrender.com'").replace("new URL(url,location.href)","new URL(url,'https://shuttlebug.onrender.com/')").replace("location.search","location.search")
 (out/name).write_text(s)
s=(root/'index.html').read_text();s=re.sub(r'/assets/[a-f0-9]{12}/','',s);s=s.replace('src="/video-ads.js"','src="video-ads.js"');s=s.replace('</head>','<script>window.SHUTTLEBUG_TV=true;</script></head>');s=s.replace('href="/','href="https://shuttlebug.onrender.com/');(out/'index.html').write_text(s);(out/'test-ads.html').write_text(s.replace('window.SHUTTLEBUG_TV=true;',"window.SHUTTLEBUG_TV=true;if(!location.search)location.search='?ads=test';"))
shutil.copyfile(root/'icons/icon-192.png',out/'icon.png');shutil.copyfile(root/'icons/icon-512.png',out/'largeicon.png')
(out/'appinfo.json').write_text(json.dumps({'id':'com.ahogentertainment.shuttlebug','version':'0.1.0','vendor':'A Hog Entertainment','type':'web','title':'Shuttlebug','main':'index.html','icon':'icon.png','largeIcon':'largeicon.png','resolution':'1920x1080','disableBackHistoryAPI':True,'requiredACG':[]},indent=2))
print(out)

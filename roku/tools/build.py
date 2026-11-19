"""Generate Roku metadata only from the intersection of the rights register and catalog."""
from pathlib import Path
import json,hashlib
root=Path(__file__).resolve().parents[2];dest=root/'roku/data';dest.mkdir(exist_ok=True)
cat=json.loads((root/'catalog.js').read_text().split('=',1)[1].rstrip(';\n'));rights=json.loads((root/'compliance/rights-register.json').read_text());byid={r['id']:r for r in rights};items=[]
for m in cat:
 r=byid.get(m['id'],{})
 if r.get('rightsStatus')!='reviewed' or m.get('rightsStatus')!='reviewed':continue
 for k in ['license','licenseUrl','rights','source','credit','changes']:assert m.get(k)==r.get(k),(m['id'],k)
 sources=[{'url':s['url'],'format':'mp4','label':s['label']} for s in m['sources'] if s['url'].startswith('https://') and s['url'].lower().endswith('.mp4')]
 if not sources:continue
 sources.sort(key=lambda s:0 if s['label']=='480p' else 1)
 items.append(dict(id=m['id'],title=m['title'],description=m['description'],genre=m['genre'],kind=m['type'],year=m['year'],duration=m['duration'],sources=sources,image=m.get('image') or 'pkg:/images/splash.jpg',**{k:r[k] for k in ['license','licenseUrl','rights','source','credit','changes']}))
(dest/'catalog.json').write_text(json.dumps(items,indent=2)+'\n')
(dest/'rights-snapshot.json').write_text(json.dumps([r for r in rights if r['id'] in {m['id'] for m in items}],indent=2)+'\n')
(dest/'build-info.json').write_text(json.dumps({'catalogCount':len(items),'rightsRegisterSHA256':hashlib.sha256((root/'compliance/rights-register.json').read_bytes()).hexdigest(),'rightsEndpoint':'https://shuttlebug.onrender.com/compliance/rights-register.json','paidAds':False,'testAdsDefault':False},indent=2)+'\n')
print('Built Roku catalog:',len(items),'reviewed titles; held records excluded')

"""Refresh curated open-film metadata from the official publisher; never auto-publish search results."""
import json, urllib.request, pathlib, concurrent.futures
ITEMS=[('bbb','Big Buck Bunny','Movies','Animation',2008,'bf1f3fb5-b119-4f9f-9930-8e20e892b898','https://peach.blender.org/about/'),('ed','Elephants Dream','Movies','Sci-fi',2006,'cccc3e60-0291-4ecc-aa56-39b2e2c7d0d5','https://orange.blender.org/blog/creative-commons-license-2/'),('sintel','Sintel','Movies','Fantasy',2010,'0eb052d0-fd51-43e6-aa33-ecdbf77a5d40','https://durian.blender.org/sharing/'),('caminandes2','Caminandes: Gran Dillama','TV','Animation',2013,'fb70d459-48d2-4db5-adba-813c84f9200a','https://studio.blender.org/remixing/'),('caminandes3','Caminandes: Llamigos','TV','Animation',2016,'23f3ef79-15dc-44c5-aa45-cf92e78a4509','https://studio.blender.org/remixing/')]
def load(item):
 id,title,kind,genre,year,uuid,rights=item
 api='https://video.blender.org/api/v1/videos/'+uuid
 d=json.load(urllib.request.urlopen(api,timeout=30))
 assert d['licence']['id'] in (None, 1) and d['channel']['name']=='blender_open_movies', 'Review publisher or rights change'
 # Legacy publisher metadata omits licenses; the curated rights URL is authoritative.
 files=sorted([f for f in d['files'] if f['resolution']['id'] in [360,480,720] and f['fileUrl'].endswith('.mp4')],key=lambda f:f['resolution']['id'])
 assert files
 captions=json.load(urllib.request.urlopen(api+'/captions',timeout=30))['data']
 return dict(id=id,title=title,type=kind,genre=genre,year=year,series='Caminandes' if kind=='TV' else None,episode=2 if id=='caminandes2' else 3 if id=='caminandes3' else None,duration=d['duration'],description=d['description'].split('\n')[0].strip(),image='https://video.blender.org'+d['thumbnailPath'],sources=[dict(label=f['resolution']['label'],url=f['fileUrl']) for f in files],captions=[dict(lang=c['language']['id'],label=c['language']['label'],url='https://video.blender.org'+c['captionPath']) for c in captions],credit='© '+str(year)+' Blender Foundation'+(' / www.bigbuckbunny.org' if id=='bbb' else ' / www.sintel.org' if id=='sintel' else ' / studio.blender.org'),license='Creative Commons Attribution',rights=rights,source=d['url'],rightsRecord=api,checked='2026-11-15',changes='Complete film with original credits; no editorial changes. Publisher streaming encode.')
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex: catalog=list(ex.map(load,ITEMS))
# Version-specific permission records checked against publisher pages and closing film cards.
licenses={'bbb':('3.0','https://peach.blender.org/about/'),'ed':('2.5','https://orange.blender.org/press/'),'sintel':('3.0','https://durian.blender.org/sharing/'),'caminandes2':('3.0','https://video.blender.org/w/fb70d459-48d2-4db5-adba-813c84f9200a'),'caminandes3':('4.0','https://video.blender.org/w/23f3ef79-15dc-44c5-aa45-cf92e78a4509')}
for m in catalog:
 version,rights=licenses[m['id']]
 m.update(license='CC BY '+version,licenseUrl='https://creativecommons.org/licenses/by/'+version+'/',rights=rights)
 if m['id']=='ed':m['credit']='© 2006 Blender Foundation / Netherlands Media Art Institute | www.elephantsdream.org'
 if m['id'].startswith('caminandes'):m['credit']='© Blender Foundation | www.caminandes.com'

catalog.append(dict(id='block',title='From the Block to the Beach',type='Originals',genre='Drama · Music',year=2026,description='A young rapper moves from New York to Memphis and begins his musical journey. Episode 1: The Move. Planned runtime: 35 minutes. Episode 2: The First Track.',credit='Shuttlebug Original · In production',sources=[]))
pathlib.Path('catalog.js').write_text('window.SHUTTLEBUG_CATALOG = '+json.dumps(catalog,indent=2)+';\n')
print('Saved',len(catalog),'curated entries')

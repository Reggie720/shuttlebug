from pathlib import Path
import json,xml.etree.ElementTree as E,zipfile,hashlib
root=Path(__file__).resolve().parents[1];repo=root.parent
items=json.loads((root/'data/catalog.json').read_text());rights=json.loads((repo/'compliance/rights-register.json').read_text());byid={r['id']:r for r in rights}
assert items and len({m['id'] for m in items})==len(items)
for m in items:
 assert byid[m['id']]['rightsStatus']=='reviewed'
 for key in ['license','licenseUrl','rights','source','credit','changes']:assert m[key]==byid[m['id']][key]
 assert m['sources'] and all(s['url'].startswith('https://') and s['format'] in ['mp4','hls'] for s in m['sources'])
 assert m['image'].startswith(('https://','pkg:/'))
 for c in m['subtitleTracks']:assert c['TrackName'].startswith('https://')
assert all(m['sources'][0]['format']=='hls' for m in items if m['id'].startswith('sideways'))
assert {m['id'] for m in items if m['subtitleTracks']}=={'valkaama','sideways4'}
assert not {r['id'] for r in rights if r['rightsStatus']!='reviewed'}.intersection(m['id'] for m in items)
assert json.loads((root/'data/build-info.json').read_text())['rightsRegisterSHA256']==hashlib.sha256((repo/'compliance/rights-register.json').read_bytes()).hexdigest()
for p in (root/'components').glob('*.xml'):
 tree=E.parse(p)
 for script in tree.findall('.//script'):
  assert (root/script.attrib['uri'].replace('pkg:/','')).is_file()
scene=(root/'components/ShuttlebugScene.brs').read_text();task=(root/'components/AdTask.brs').read_text()
assert 'm.pendingPlay = m.current.id' in scene and 'checkRights()' in scene
assert 'getAds(' not in task and 'GetAds(' not in task
assert 'Roku_Ads()' in task and 'ShowAds(TestAdPod' in task
assert 'enableAdMeasurements' not in task
assert (root/'media/test-commercial.mp4').read_bytes()==(repo/'ads/test-commercial.mp4').read_bytes()
manifest=(root/'manifest').read_text();assert 'bs_libs_required=roku_ads_lib' in manifest
with zipfile.ZipFile(root/'packages/Shuttlebug_Roku_Developer.zip') as z:
 assert z.testzip() is None
 assert 'manifest' in z.namelist() and 'source/main.brs' in z.namelist()
 assert z.read('data/catalog.json')==(root/'data/catalog.json').read_bytes()
 for name in z.namelist():
  if not name.endswith('/'):assert z.read(name)==(root/name).read_bytes()
 for name in z.namelist():assert not name.startswith(('node_modules/','roku/')) and '..' not in name
print(f'PASS package structure, SceneGraph script links, {len(items)} cleared titles, held-title exclusion, rights snapshot and unpaid local test creative')

assert 'm.mode = "resumingAfterAd"' in scene
assert 'm.top.SetFocus(true)' in scene
assert 'duration="12"' in (root/'components/ShuttlebugScene.xml').read_text()
assert 'onLocalAdState' in scene and 'm.adVideo.control = "stop"' in scene

source_catalog=json.loads((repo/'catalog.js').read_text().split('=',1)[1].rstrip(';\n'))
source_byid={x['id']:x for x in source_catalog}
for item in items:
 original=source_byid[item['id']]
 assert item['added']==(original.get('added') or '')
 assert item['series']==(original.get('series') or '')
 assert item['season']==original.get('season') and item['episode']==original.get('episode')
 assert not item['contentRating'] or original.get('ratingVerified') is True
ui=E.parse(root/'components/ShuttlebugScene.xml')
rows=ui.find('.//RowList')
assert rows is not None and rows.attrib['itemComponentName']=='PosterCard'
assert 'rowItemSelected' in scene and 'rowItemFocused' in scene
assert (root/'components/PosterCard.xml').is_file()

# Cert-facing package resources must have the exact dimensions, not store sizes.
import struct
entries=dict(line.split('=',1) for line in manifest.splitlines() if line and not line.startswith('#'))
assert len(entries)==len([line for line in manifest.splitlines() if line and not line.startswith('#')])
assert entries['supports_input_launch']=='1' and entries['rsg_version']=='1.3'
for key,size in [('mm_icon_focus_fhd',(540,405)),('mm_icon_focus_hd',(290,218)),('splash_screen_hd',(1280,720)),('splash_screen_sd',(720,480))]:
 image=(root/entries[key].removeprefix('pkg:/')).read_bytes()
 assert image[:8]==b'\x89PNG\r\n\x1a\n'
 assert struct.unpack('>II',image[16:24])==size,(key,size)
assert 'InitClientCertificates' not in (root/'components/CatalogTask.brs').read_text()
assert 'SetCertificatesFile("common:/certs/ca-bundle.crt")' in (root/'components/CatalogTask.brs').read_text()
print('PASS manifest image sizes, required flags, verified TLS trust store and package resources')

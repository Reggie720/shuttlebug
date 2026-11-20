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

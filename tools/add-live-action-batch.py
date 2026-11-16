"""Bounded publisher-approved live-action episodes. No synthetic audio or automatic imports."""
import json, pathlib, urllib.request, subprocess

ROOT = pathlib.Path(__file__).resolve().parents[1]
HOST = 'https://videos.side-ways.net'
RIGHTS = 'https://side-ways.net/en/webseries/'
EPISODES = [
    (1, 'e49d8227-8565-4f54-86c7-78e40e1cc451', 'Strictly Moneyless', 'Meet Elf Pavlik, a traveler who has chosen to live without money and help the communities he visits.', 'English'),
    (2, '76212048-1204-48ef-924d-f3cabeec15b1', 'Buy Housing Together', 'In Nantes, a group pools small monthly contributions to buy homes for people experiencing homelessness.', 'French with English subtitles'),
    (4, '5150622b-2281-4366-8d90-3634b336f048', 'Let Us Build Together', 'Neighbors in Belgium build a wind turbine together and share what they learn along the way.', 'French with English subtitles'),
]

def get(url):
    with urllib.request.urlopen(url, timeout=30) as response:
        return response.read()

def probe(path):
    data = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration:stream=codec_name,codec_type', '-of', 'json', str(path)]))
    assert {'h264', 'aac'} <= {s['codec_name'] for s in data['streams']}
    return float(data['format']['duration'])

new = []
review = pathlib.Path('/tmp/shuttle-sideways-review')
review.mkdir(exist_ok=True)
(ROOT / 'media/library').mkdir(exist_ok=True)
(ROOT / 'captions').mkdir(exist_ok=True)
for number, uuid, title, description, language in EPISODES:
    api = HOST + '/api/v1/videos/' + uuid
    data = json.loads(get(api))
    assert data['channel']['name'] == 'episodes' and data['account']['name'] == 'sideways'
    assert data['licence']['id'] == 2
    files = sorted([f for p in data['streamingPlaylists'] for f in p['files'] if f['resolution']['id'] in [360, 480, 720]], key=lambda f: f['resolution']['id'])
    selected = next(f for f in files if f['resolution']['id'] == 480)
    local = review / f'side{number}.mp4'
    if not local.exists() or local.stat().st_size != selected['size']:
        local.write_bytes(get(selected['fileUrl']))
    duration = probe(local)
    poster = ROOT / f'media/library/sideways{number}.jpg'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '45', '-i', str(local), '-frames:v', '1', '-vf', 'scale=640:-1', str(poster)], check=True, capture_output=True)
    captions = []
    if number != 1:
        records = json.loads(get(api + '/captions'))['data']
        record = next(c for c in records if c['language']['id'] == 'en' and not c['automaticallyGenerated'])
        body = get(record['fileUrl'])
        assert body.startswith(b'WEBVTT') and b'-->' in body
        caption_path = f'/captions/sideways{number}-en.vtt'
        (ROOT / caption_path.lstrip('/')).write_bytes(body)
        captions = [dict(lang='en', label='English', url=caption_path)]
    new.append(dict(id=f'sideways{number}', title='SideWays — ' + title, type='TV', genre='Documentary', year=2018,
        series='SideWays', episode=number, duration=duration, description=description, image=f'/media/library/sideways{number}.jpg',
        sources=[dict(label=f['resolution']['label'], url=f['fileUrl']) for f in files], captions=captions,
        defaultCaptions='en' if captions else None, language=language,
        qualityNote='Publisher upload: 2018 · Short documentary episode',
        credit='Sideways, Roving WebSeries · Hélène Legay and Benoît Cassegrain · Original participants and music credited in each episode',
        license='CC BY-SA 3.0', licenseUrl='https://creativecommons.org/licenses/by-sa/3.0/', rights=RIGHTS,
        source='https://side-ways.net/en/episode' + str(number), rightsRecord=api, checked='2026-11-16', added='2026-11-16',
        collection='live-action-2026-11-16', audioType='recorded-human', audioEvidence=RIGHTS,
        changes='Complete publisher streaming encode with original interviews, soundtrack and credits. No synthetic narration or dub. Thumbnail is a resized film frame. Publisher English subtitle file copied unchanged where available.'))
    print('Verified', title, round(duration, 2), flush=True)

catalog_path = ROOT / 'catalog.js'
catalog = json.loads(catalog_path.read_text().split('=', 1)[1].rstrip(';\n'))
ids = {m['id'] for m in new}
catalog = [m for m in catalog if m['id'] not in ids] + new
catalog_path.write_text('window.SHUTTLEBUG_CATALOG = ' + json.dumps(catalog, indent=2) + ';\n')
print('Catalog:', len(catalog), 'titles', flush=True)

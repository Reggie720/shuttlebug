"""Release gate for reviewed category metadata. Run automatically before packaging."""
import json, math
from pathlib import Path

FEATURE_SECONDS = 40 * 60  # Shuttlebug's editorial boundary for standalone films.

def validate(items):
    errors = []
    seen = set()
    for m in items:
        name = m.get('id') or '<missing id>'
        def fail(message): errors.append(f'{name}: {message}')
        if not m.get('id') or name in seen: fail('a unique ID is required')
        seen.add(name)
        if not m.get('title') or not isinstance(m.get('genre'), str) or not m['genre'].strip(): fail('title and reviewed genre are required')
        if not isinstance(m.get('year'), int) or m['year'] < 1995: fail('release year must be 1995 or newer')
        duration = m.get('duration')
        if not isinstance(duration, (int, float)) or not math.isfinite(duration) or duration <= 0:
            fail('a positive verified runtime is required')
            continue
        if m.get('type') == 'TV':
            if m.get('format') != 'episode' or not m.get('series'): fail('TV titles need format=episode and a series name')
            episode = m.get('episode')
            if episode is not None and (not isinstance(episode, int) or episode < 1): fail('episode must be a positive number or null when unnumbered')
        elif m.get('type') in ['Movies', 'Originals']:
            if m.get('format') not in ['feature', 'short']: fail('standalone films need an explicit feature or short format')
            if m.get('series') or m.get('episode') is not None: fail('standalone films cannot carry TV series/episode metadata')
            if m.get('format') == 'short' and duration >= FEATURE_SECONDS: fail('review short format: runtime is 40 minutes or longer')
            if m.get('format') == 'feature' and duration < FEATURE_SECONDS: fail('review feature format: runtime is under 40 minutes')
        else:
            fail('type must be Movies, TV or Originals')
        if m.get('sources') and not all(m.get(k) for k in ['credit', 'rights', 'license', 'licenseUrl', 'source']): fail('playable titles need rights and attribution metadata')
    return errors

if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    items = json.loads((root / 'catalog.js').read_text().split('=', 1)[1].rstrip(';\n'))
    errors = validate(items)
    if errors:
        raise SystemExit('Catalog review required:\n' + '\n'.join(errors))
    print(f'PASS: {len(items)} titles have valid format, genre, year, series and rights metadata.')

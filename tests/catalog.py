"""Check catalog rules reject common classification mistakes before release."""
import copy
import json
import runpy
from pathlib import Path

root = Path(__file__).resolve().parents[1]
validate = runpy.run_path(str(root / 'tools/validate-catalog.py'))['validate']
items = json.loads((root / 'catalog.js').read_text().split('=', 1)[1].rstrip(';\n'))
assert not validate(items)
feature = next(m for m in items if m.get('format') == 'feature')
episode = next(m for m in items if m['type'] == 'TV')
for source, changes in [
    (feature, {'format': None}),
    (feature, {'format': 'short'}),
    (feature, {'year': 1994}),
    (episode, {'series': None}),
    (episode, {'format': 'feature'}),
]:
    invalid = copy.deepcopy(source)
    invalid.update(changes)
    assert validate([invalid]), f'Release gate accepted {changes}'
print('PASS: catalog release gate rejects missing and inconsistent categories.')

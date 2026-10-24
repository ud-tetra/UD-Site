#!/usr/bin/env python3
"""Reassemble hash-verified large files from temporary connector transport."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main():
    metadata = ROOT / '.transport/lamp-manifest.json'
    if not metadata.is_file():
        print('No pending archive transport'); return
    specs = json.loads(metadata.read_text())['files']
    current = json.loads((ROOT / 'manifests/current.json').read_text())
    release = json.loads((ROOT / current['manifest']).read_text())
    for index, spec in enumerate(specs):
        target = ROOT / spec['path']
        assert target.resolve().parent == (ROOT / 'releases/lamp').resolve() or spec['path'] == 'site/assets/sources.json'
        record = next(r for r in release['files'] + release['release_archives'] if r['path'] == spec['path'])
        assert record['sha256'] == spec['sha256'] and record['size_bytes'] == spec['size_bytes']
        temporary = ROOT / f'build/assembled-{index}'; temporary.parent.mkdir(exist_ok=True)
        digest = hashlib.sha256(); total = 0
        with temporary.open('wb') as output:
            for part in spec['parts']:
                path = ROOT / part['path']
                assert path.resolve().parent == (ROOT / '.transport/payloads').resolve()
                data = path.read_bytes()
                assert len(data) == part['size_bytes'] and hashlib.sha256(data).hexdigest() == part['sha256']
                output.write(data); digest.update(data); total += len(data)
        assert digest.hexdigest() == spec['sha256'] and total == spec['size_bytes']
        target.parent.mkdir(parents=True, exist_ok=True); temporary.replace(target)
        for part in spec['parts']: (ROOT / part['path']).unlink()
        print(json.dumps({'status': 'ASSEMBLED', 'path': spec['path'], 'sha256': digest.hexdigest(), 'size_bytes': total}))
    metadata.unlink()

if __name__ == '__main__': main()

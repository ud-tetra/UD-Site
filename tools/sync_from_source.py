#!/usr/bin/env python3
"""One-way, hash-bound import of committed public Sites source; dry-run by default."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PROJECT = 'appgprj_6acee9ef84dc81918f8143dc74e64657'

def git(source, *args):
    return subprocess.check_output(['git', '-C', str(source), *args])

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--site-version', type=int, required=True)
    p.add_argument('--lamp-archive', type=Path)
    p.add_argument('--apply', action='store_true')
    p.add_argument('--allow-removals', action='store_true')
    a = p.parse_args()
    source = a.source.resolve()
    if a.site_version < 1: p.error('site-version must be positive')
    hosting = json.loads((source / '.openai/hosting.json').read_text())
    if hosting.get('project_id') != PROJECT or hosting.get('static', {}).get('directory') != 'dist':
        p.error('Expected public atlas project with committed dist output')
    if git(source, 'status', '--porcelain', '--untracked-files=no').strip():
        p.error('Source has uncommitted tracked changes')
    commit = git(source, 'rev-parse', 'HEAD').decode().strip()
    date = git(source, 'show', '-s', '--format=%cI', 'HEAD').decode().strip()
    tracked = [s for s in git(source, 'ls-files', '-z').decode().split('\0') if s]
    records = []
    files = {}
    for rel in sorted(tracked):
        original = source / rel
        if original.is_symlink() or not original.is_file(): p.error('Non-regular source file: ' + rel)
        name = Path(rel).name.lower()
        if name.startswith('.env') or name in ('credentials.json', '.netrc', '.npmrc'):
            p.error('Refusing possible runtime credentials: ' + rel)
        destination = 'site/' + rel[5:] if rel.startswith('dist/') else 'source/' + rel
        data = original.read_bytes()
        files[destination] = original
        records.append({'path': destination, 'original_path': rel,
                        'size_bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
    web = [r for r in records if r['path'].startswith('site/')]
    if not any(r['path'] == 'site/index.html' for r in web): p.error('Missing static entrypoint')
    archives = []
    if a.lamp_archive:
        archive = a.lamp_archive.resolve()
        with zipfile.ZipFile(archive) as z:
            meta = json.loads(z.read('Unified-Dynamics-LAMP/EXPORT-MANIFEST.json'))
            if meta['source_commit'] != commit or meta['sites_version'] != a.site_version:
                p.error('LAMP package does not match this source/version')
            expected = {r['original_path'][5:]: r['sha256'] for r in web}
            if meta['web_files_sha256'] != expected:
                p.error('LAMP package web hashes do not match the source')
        dest = 'releases/lamp/' + archive.name
        files[dest] = archive
        archives.append({'path': dest, 'sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
                         'size_bytes': archive.stat().st_size, 'kind': 'standalone-lamp-export'})
    manifest = {'schema_version': 1, 'project_id': PROJECT, 'sites_version': a.site_version,
                'source_commit': commit, 'source_commit_date': date,
                'public_url': 'https://unified-dynamics-public.ben-w-mayes.chatgpt.site',
                'source_files': len(records), 'web_files': len(web),
                'files': records, 'release_archives': archives}
    current_file = ROOT / 'manifests/current.json'
    old = {}
    if current_file.is_file():
        pointer = json.loads(current_file.read_text())
        old = json.loads((ROOT / pointer['manifest']).read_text())
        if a.site_version < old['sites_version']: p.error('Refusing a version rollback')
    old_paths = {r['path'] for r in old.get('files', [])}
    removed = sorted(old_paths - set(files))
    if removed and not a.allow_removals: p.error('Removed upstream paths require --allow-removals: ' + str(removed))
    added, changed = [], []
    for rel, original in files.items():
        target = ROOT / rel
        if not target.exists(): added.append(rel)
        elif hashlib.sha256(target.read_bytes()).digest() != hashlib.sha256(original.read_bytes()).digest(): changed.append(rel)
    version_path = f'manifests/releases/sites-v{a.site_version}.json'
    serialized = json.dumps(manifest, indent=2, ensure_ascii=False) + '\n'
    historical = ROOT / version_path
    if historical.exists() and historical.read_text() != serialized:
        p.error('Immutable version manifest already exists with different contents')
    summary = {'mode': 'apply' if a.apply else 'dry-run', 'sites_version': a.site_version,
               'source_commit': commit, 'source_files': len(records), 'web_files': len(web),
               'added_files': len(added), 'changed_files': len(changed), 'removed_files': removed,
               'release_archives': archives}
    if a.apply:
        for rel in added + changed:
            target = ROOT / rel; target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(files[rel], target)
        for rel in removed: (ROOT / rel).unlink()
        historical.parent.mkdir(parents=True, exist_ok=True)
        historical.write_text(serialized)
        current_file.write_text(json.dumps({'schema_version': 1, 'sites_version': a.site_version,
                                           'source_commit': commit, 'manifest': version_path}, indent=2) + '\n')
        (ROOT / 'reports').mkdir(exist_ok=True)
        # Stable receipt: rerunning an identical sync does not alter this record.
        (ROOT / 'reports/sync-receipt.json').write_text(json.dumps({
            'status': 'SYNCED', 'sites_version': a.site_version, 'source_commit': commit,
            'source_files': len(records), 'web_files': len(web),
            'release_archives': archives, 'manifest': version_path}, indent=2) + '\n')
    print(json.dumps(summary, indent=2))

if __name__ == '__main__': main()

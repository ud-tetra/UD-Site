#!/usr/bin/env python3
"""Validate mirrored release bytes and local web behavior without rebuilding research."""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import shutil
import subprocess
from urllib.parse import unquote, urlsplit
import zipfile

ROOT = Path(__file__).resolve().parents[1]

class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.links = []; self.ids = set(); self.external_assets = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a: self.ids.add(a['id'])
        for attr in ('href', 'src', 'action'):
            if a.get(attr): self.links.append(a[attr])
        u = a.get('src') if tag in ('script', 'img', 'iframe') else a.get('href') if tag == 'link' else None
        if u and (urlsplit(u).scheme in ('http', 'https') or u.startswith('//')): self.external_assets.append(u)

def check_site(web, base=''):
    errors = []; pages = {}; links = 0; json_count = 0; js_count = 0; fetches = 0
    for p in web.rglob('*.html'):
        q = Page(); q.feed(p.read_text(encoding='utf-8')); pages[p.resolve()] = q
    for p, q in pages.items():
        for url in q.links:
            u = urlsplit(url)
            if u.scheme or u.netloc: continue
            path = unquote(u.path)
            if path.startswith('/'):
                if base:
                    if path != base and not path.startswith(base + '/'):
                        errors.append(f'Outside base path: {p.relative_to(web)} -> {url}'); continue
                    path = path[len(base):] or '/'
                target = web / path.lstrip('/')
            else: target = p.parent / path if path else p
            if target.is_dir(): target /= 'index.html'
            target = target.resolve(); links += 1
            if not target.is_file(): errors.append(f'Missing file: {p.relative_to(web)} -> {url}')
            elif u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:
                errors.append(f'Missing anchor: {p.relative_to(web)} -> {url}')
    for p in web.rglob('*.json'):
        try: json.loads(p.read_text(encoding='utf-8')); json_count += 1
        except Exception as e: errors.append(f'Invalid JSON: {p}: {e}')
    if not shutil.which('node'): errors.append('Node.js is required for JavaScript syntax checks')
    else:
        for p in sorted(web.rglob('*')):
            if p.suffix in ('.js', '.mjs'):
                result = subprocess.run(['node', '--check', str(p)], capture_output=True, text=True)
                js_count += 1
                if result.returncode: errors.append(result.stderr)
    for p in (web / 'assets').glob('*.js'):
        for path in re.findall(r'''fetchJSON\(['"](/[^'"]+)['"]\)''', p.read_text()):
            fetches += 1
            if not (web / path.lstrip('/')).is_file(): errors.append('Missing fetch data: ' + path)
    return {'html_pages': len(pages), 'local_links_and_fragments': links, 'json_files': json_count,
            'javascript_syntax_checks': js_count, 'literal_fetch_inputs': fetches,
            'external_render_assets': sorted({u for q in pages.values() for u in q.external_assets}), 'errors': errors}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--web-root', type=Path)
    p.add_argument('--base-path', default='')
    p.add_argument('--report', type=Path)
    a = p.parse_args()
    pointer = json.loads((ROOT / 'manifests/current.json').read_text())
    manifest = json.loads((ROOT / pointer['manifest']).read_text())
    errors = []
    for r in manifest['files'] + manifest['release_archives']:
        target = ROOT / r['path']
        if not target.is_file() or target.is_symlink(): errors.append('Missing/nonregular mirror file: ' + r['path']); continue
        if target.stat().st_size != r['size_bytes'] or hashlib.sha256(target.read_bytes()).hexdigest() != r['sha256']:
            errors.append('Hash mismatch: ' + r['path'])
    expected = {r['path'] for r in manifest['files']}
    actual = {f.relative_to(ROOT).as_posix() for d in ('site', 'source') for f in (ROOT / d).rglob('*') if f.is_file()}
    if actual != expected: errors.append('Managed file inventory differs: ' + str(sorted(actual ^ expected)))
    for r in manifest['release_archives']:
        with zipfile.ZipFile(ROOT / r['path']) as z:
            if z.testzip() is not None: errors.append('Archive CRC failed: ' + r['path'])
    if manifest['source_files'] != len(manifest['files']) or pointer['source_commit'] != manifest['source_commit']:
        errors.append('Manifest metadata mismatch')
    web = a.web_root.resolve() if a.web_root else ROOT / 'site'
    if a.web_root:
        for r in manifest['files']:
            if not r['path'].startswith('site/'): continue
            rel = r['path'][5:]; target = web / rel
            if not target.is_file(): errors.append('Deployment file missing: ' + rel); continue
            # Only presentation URLs and SEO files may change during preparation.
            allowed = rel in ('sitemap.xml', 'robots.txt') or (a.base_path and (target.suffix == '.html' or rel == 'assets/app.js'))
            if not allowed and hashlib.sha256(target.read_bytes()).hexdigest() != r['sha256']:
                errors.append('Deployment artifact/data changed: ' + rel)
    result = check_site(web, a.base_path.rstrip('/')); errors.extend(result.pop('errors'))
    report = {'status': 'PASS' if not errors else 'FAIL', 'sites_version': manifest['sites_version'],
              'source_commit': manifest['source_commit'], 'source_files_hash_checked': len(manifest['files']),
              'release_archives_checked': len(manifest['release_archives']),
              'layout': a.base_path or 'domain root', **result,
              'scientific_proofs_revalidated': False, 'apache_runtime_tested': False, 'errors': errors}
    if a.report:
        a.report.parent.mkdir(parents=True, exist_ok=True); a.report.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2)); raise SystemExit(bool(errors))

if __name__ == '__main__': main()

#!/usr/bin/env python3
"""Prepare an isolated static deployment without modifying mirrored release files."""
import argparse
import json
from pathlib import Path
import re
import shutil
from urllib.parse import urlsplit
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path, default=ROOT / 'build/public_html')
    p.add_argument('--base-path', default='')
    p.add_argument('--origin')
    p.add_argument('--apache', action='store_true')
    a = p.parse_args(); base = a.base_path.rstrip('/')
    if base and not re.fullmatch(r'(?:/[A-Za-z0-9_-]+)+', base): p.error('Invalid base-path')
    origin = a.origin.rstrip('/') if a.origin else None
    if origin:
        u = urlsplit(origin)
        if u.scheme not in ('http', 'https') or not u.netloc or u.path or u.query or u.fragment or u.username or u.password:
            p.error('origin must be an http(s) origin without a path')
    output = a.output.resolve(); build = ROOT / 'build'
    if build not in output.parents or output == build: p.error('output must be a directory strictly beneath build/')
    if output.exists(): p.error('Output already exists; choose a fresh directory or remove the previous generated build first')
    shutil.copytree(ROOT / 'site', output)
    changes = []
    if base:
        for f in output.rglob('*.html'):
            text = f.read_text(encoding='utf-8')
            text = re.sub(r'''(\b(?:href|src|action)\s*=\s*["'])(/(?!/))''', lambda m: m[1] + base + '/', text, flags=re.I)
            f.write_text(text, encoding='utf-8'); changes.append(f.relative_to(output).as_posix())
        f = output / 'assets/app.js'; text = f.read_text(encoding='utf-8')
        assert text.count('a.href=href;') == 1 and text.count('await fetch(path)') == 1
        helper = ('const udDeploymentBase=' + json.dumps(base) + ';\n'
                  'const udDeploymentURL=u=>typeof u==="string"&&u.startsWith("/")&&!u.startsWith("//")?udDeploymentBase+u:u;\n')
        text = text.replace("'use strict';", "'use strict';\n" + helper, 1)
        text = text.replace('a.href=href;', 'a.href=udDeploymentURL(href);').replace('await fetch(path)', 'await fetch(udDeploymentURL(path))')
        f.write_text(text, encoding='utf-8'); changes.append('assets/app.js')
    if origin:
        routes = sorted('/' + f.relative_to(output).as_posix().removesuffix('index.html') for f in output.rglob('index.html'))
        xml = '<?xml version="1.0" encoding="utf-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        xml += ''.join('<url><loc>' + escape(origin + base + r) + '</loc></url>\n' for r in routes)
        (output / 'sitemap.xml').write_text(xml + '</urlset>\n')
        (output / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: ' + origin + base + '/sitemap.xml\n')
        changes += ['sitemap.xml', 'robots.txt']
    if a.apache: shutil.copyfile(ROOT / 'deploy/apache/.htaccess', output / '.htaccess')
    (output / '.nojekyll').write_text('')
    receipt = {'base_path': base, 'origin': origin, 'apache': a.apache, 'changed_presentation_files': changes,
               'source_unchanged': True, 'downloads_and_data_unchanged': True}
    (ROOT / 'reports/local-deployment.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({'output': str(output), **receipt}, indent=2))

if __name__ == '__main__': main()

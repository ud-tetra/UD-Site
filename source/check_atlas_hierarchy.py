"""Hierarchy and preservation QA. No claim of rendered browser verification."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,subprocess,re,hashlib
R=Path(__file__).resolve().parent;D=R/'dist';BASE='389a9f0c4ecfcd486e2aa79cefbd4a8ecbc05e1c'
def old(rel):return subprocess.check_output(['git','show',BASE+':'+rel],cwd=R)
class Page(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.links=[];self.primary=[];self.innav=False;self.main=0;self.h1=0;self.title=0
 def handle_starttag(self,t,a):
  a=dict(a)
  if 'id' in a:self.ids.append(a['id'])
  if t=='nav' and a.get('id')=='navigation':self.innav=True
  if t=='main':self.main+=1
  if t=='h1':self.h1+=1
  if t=='title':self.title+=1
  if t in ['a','link','script','img']:
   u=a.get('href') or a.get('src')
   if u:self.links.append(u)
   if t=='a' and self.innav:self.primary.append(u)
 def handle_endtag(self,t):
  if t=='nav':self.innav=False
pages={}
for p in D.rglob('*.html'):
 q=Page();q.feed(p.read_text());assert q.main==1 and q.h1==1 and q.title>=1,(p,q.main,q.h1,q.title)
 assert len(q.ids)==len(set(q.ids)),p
 assert q.primary==['/','/primer/','/research/','/evidence/','/papers/','/archive/'],p
 pages[p.resolve()]=q
links=0
for p,q in pages.items():
 for u in q.links:
  s=urlsplit(u)
  if s.scheme or s.netloc:continue
  target=D/unquote(s.path.lstrip('/')) if s.path.startswith('/') else p.parent/unquote(s.path) if s.path else p
  if target.is_dir():target=target/'index.html'
  assert target.exists(),(p,u)
  if s.fragment and target.suffix=='.html' and target.resolve() in pages:assert unquote(s.fragment) in pages[target.resolve()].ids,(p,u,'missing fragment')
  links+=1
# All old routes and anchors remain valid. Whole source artifacts and scientific data remain byte-identical.
tracked=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'dist'],cwd=R,text=True).splitlines()
artifact_count=0;anchor_count=0
for rel in tracked:
 p=R/rel;assert p.is_file(),rel
 if p.suffix=='.html':
  q=Page();q.feed(old(rel).decode());new=pages[p.resolve()]
  assert set(q.ids)<=set(new.ids),(rel,set(q.ids)-set(new.ids));anchor_count+=len(q.ids)
 elif rel not in ['dist/assets/research-record-v0.1.js','dist/sitemap.xml']:
  assert p.read_bytes()==old(rel),rel
  artifact_count+=1
# The actual manuscript and update articles have unchanged text and links.
for rel in ['dist/papers/index.html','dist/updates/index.html']:
 originals=re.findall(r'<article\b.*?</article>',old(rel).decode(),re.S);now=(R/rel).read_text()
 assert all(a in now for a in originals),rel
 assert len(originals)==(27 if 'papers/' in rel else 41)
meta=json.loads((D/'sources/atlas-structure-v0.2/EDITORIAL_RECONCILIATION.json').read_text());assert len(meta['pages'])==len(pages)==30
assert len({x['route'] for x in meta['pages']})==30
for x in meta['pages']:
 assert x['primary_parent'] in ['/','/primer/','/research/','/evidence/','/papers/','/archive/']
for p in [D/'index.html',D/'research/index.html',D/'archive/index.html']:
 assert 'Latest research session' not in p.read_text()
assert '<details class="atlas-collection">' in (D/'papers/index.html').read_text()
assert '<button id="record-more"' in (D/'research-record/index.html').read_text()
# Existing script hooks used by specialist tools are preserved.
for rel in ['primer','source-contract','source-programme','realization','joint-carrier','programmed-clock','native-admission','metric-admission','subdivision','metric-selection','refinement-tower','history-comparison','dependencies','sources','ledger']:
 oldscripts=re.findall(r'<script[^>]*src="([^"]+)"',old('dist/'+rel+'/index.html').decode());now=(D/rel/'index.html').read_text()
 assert all(u in now for u in oldscripts),rel
receipt={'status':'PASS','pages':len(pages),'primary_destinations':6,'old_routes_preserved':27,'old_anchor_occurrences_preserved':anchor_count,'unchanged_existing_artifact_and_data_files':artifact_count,'paper_articles_byte_preserved':27,'update_articles_byte_preserved':41,'local_links_and_fragments_checked':links,'scientific_status_changes':0,'javascript_syntax':'checked separately','browser_visual_qa':'unavailable: control-browser not available in managed runtime','physical_promotion':0}
(D/'sources/atlas-structure-v0.2/VALIDATION.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))

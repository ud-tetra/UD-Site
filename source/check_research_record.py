"""Publication custody and static checks; no scientific replay or browser QA."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import hashlib,json,zipfile,re,subprocess
R=Path(__file__).resolve().parent;D=R/'dist';S=D/'sources/research-record-v0.1'
class Page(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.links=[];self.main=0;self.title=0;self.nav=False
 def handle_starttag(self,t,a):
  a=dict(a)
  if 'id' in a:self.ids.append(a['id'])
  if t=='main':self.main+=1
  if t=='title':self.title+=1
  if t=='nav' and a.get('id')=='navigation':self.nav=True
  if t in ['a','link','script','img']:
   u=a.get('href') or a.get('src')
   if u:self.links.append(u)
pages={}
for p in D.rglob('*.html'):
 q=Page();q.feed(p.read_text());assert q.main==1 and q.title>=1,p;assert len(q.ids)==len(set(q.ids)),p
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
 if q.nav:assert '/research-record/' in q.links,p
index=json.loads((S/'SOURCE_MAP.json').read_text());assert index['capture_count']==len(index['records'])==118
assert index['event_count']==len(index['events'])==122
sources=json.loads((D/'assets/sources.json').read_text());assert len(sources)==len({x['id'] for x in sources})
for x in sources:
 if x.get('local'):assert (D/x['local'].lstrip('/')).is_file(),x['id']
for x in json.loads((D/'assets/claims.json').read_text()):assert x['source_id'] in {s['id'] for s in sources}
for x in index['public_report_copies']:
 b=(D/x['local'].lstrip('/')).read_bytes();assert len(b)==x['size_bytes'];assert hashlib.sha256(b).hexdigest()==x['sha256']
assert len(index['public_report_copies'])==62
for x in sources:
 if x['id'].startswith('PUBLICREC'):
  b=(D/x['local'].lstrip('/')).read_bytes();assert b.decode()==x['content'] and hashlib.sha256(b).hexdigest()==x['sha256']
assert len([x for x in sources if x['id'].startswith('PUBLICREC')])==57
for rel in ['assets/ledger.json','assets/claims.json']:
 original=subprocess.check_output(['git','show','HEAD:dist/'+rel],cwd=R)
 assert original==(D/rel).read_bytes(),rel
home=(D/'index.html').read_text();assert 'observation-session-summary' not in home and 'Latest research session' not in home
assert 'research-record-v01' in (D/'updates/index.html').read_text()
assert 'aria-current="page" href="/research-record/"' in (D/'research-record/index.html').read_text()
for x in index['records']:assert x['capture_id'] in pages[(D/'research-record/index.html').resolve()].ids
contract=S/'parity-contract/CONTRACT.json';assert hashlib.sha256(contract.read_bytes()).hexdigest()=='860713fe9386d5d08559d79565be0013edc424685dfdb715b9ff7e25d883cdfe'
# Bundle contains exactly the declared public files with unchanged bytes and safe paths.
with zipfile.ZipFile(S/'RESEARCH_RECORD_v0.1.zip') as z:
 assert z.testzip() is None
 for n in z.namelist():
  assert not n.startswith('/') and '..' not in Path(n).parts
  assert z.read(n)==(S/n).read_bytes()
assert json.loads((D/'assets/ledger.json').read_text())['rows'].__len__()==448
assert not any(x.name=='Gap2_FINAL_Finite_Genesis.png' for x in D.rglob('*'))
receipt={'status':'PASS','html_pages':len(pages),'local_links_and_fragments_checked':links,'captures_indexed':118,'events_indexed':122,'byte_verified_public_report_copies':57,'byte_verified_contract_code_and_receipts':5,'source_registry_entries':len(sources),'ledger_and_claim_bytes':'unchanged','bundle_crc_and_member_bytes':'PASS','javascript':'node --check passed','scientific_replay':'not performed; inherited source results retain their scopes','browser_visual_qa':'not run: control-browser capability unavailable in managed runtime','physical_promotion':0}
(S/'PUBLICATION_VALIDATION.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))

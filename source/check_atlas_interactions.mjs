// Logic tests with DOM-shaped fixtures. Not a browser or visual QA claim.
import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const rows=Array.from({length:30},(_,i)=>({id:'record-'+i,textContent:i===29?'Parity contract':'Clock '+i,hidden:false}));
function node(){return {hidden:false,value:'',textContent:'',events:{},addEventListener(t,f){this.events[t]=f}}}
const query=node(),count=node(),empty=node(),more=node(),win=node();
const lookup={'#record-query':query,'#record-count':count,'#record-empty':empty,'#record-more':more};
const location={hash:''};
const context={document:{querySelector:s=>lookup[s],querySelectorAll:()=>rows},window:win,location};
vm.runInNewContext(fs.readFileSync('dist/assets/research-record-v0.1.js','utf8'),context);
assert.equal(rows.filter(r=>!r.hidden).length,8);
assert.equal(more.hidden,false);
more.events.click();assert.equal(rows.filter(r=>!r.hidden).length,20);
query.value='parity';query.events.input();assert.equal(rows.filter(r=>!r.hidden).length,1);assert.equal(rows[29].hidden,false);assert.equal(more.hidden,true);
query.value='no result';query.events.input();assert.equal(rows.filter(r=>!r.hidden).length,0);assert.equal(empty.hidden,false);
query.value='';query.events.input();location.hash='#record-29';win.events.hashchange();assert.equal(rows[29].hidden,false);
let scrolled=0;const outer={tagName:'DETAILS',open:false,parentElement:null};const inner={tagName:'DETAILS',open:false,parentElement:outer};const target={parentElement:inner,scrollIntoView(){scrolled++}};const w=node();
vm.runInNewContext(fs.readFileSync('dist/assets/atlas-hierarchy-v0.2.js','utf8'),{window:w,location:{hash:'#old-paper'},document:{getElementById:()=>target}});
assert.equal(outer.open,true);assert.equal(inner.open,true);assert.equal(scrolled,1);
console.log(JSON.stringify({status:'PASS',checks:['bounded initial record list','pagination','search','empty state','archival deep link visibility','nested collection anchor reveal'],verification_scope:'isolated JavaScript logic; no rendered browser QA'}));

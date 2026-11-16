const {JSDOM}=require(process.env.JSDOM_MODULE||'jsdom');
const fs=require('node:fs');const assert=require('node:assert/strict');
const dom=new JSDOM(fs.readFileSync('index.html','utf8'),{url:'https://shuttlebug.onrender.com',runScripts:'outside-only',pretendToBeVisual:true});
const vm=require('node:vm');const context=dom.getInternalVMContext();const w=dom.window;w.matchMedia=()=>({matches:false});w.scrollTo=()=>{};w.confirm=()=>true;
w.HTMLDialogElement.prototype.showModal=function(){this.open=true};w.HTMLDialogElement.prototype.close=function(){this.open=false;this.dispatchEvent(new w.Event('close'))};
w.HTMLMediaElement.prototype.load=function(){};w.HTMLMediaElement.prototype.pause=function(){};
w.HTMLMediaElement.prototype.play=function(){return Promise.resolve()};
for(const file of ['catalog.js','config.js','app.js'])vm.runInContext(fs.readFileSync(file,'utf8'),context);
const $=s=>w.document.querySelector(s),all=s=>[...w.document.querySelectorAll(s)];
function click(s){assert($(s),'Missing '+s);$(s).click()}
function run(s){return vm.runInContext(s,context)}
function route(page){run(`page=${JSON.stringify(page)};genre='All';render()`)}
route('Movies');assert.equal(all('.browse-grid .tile').length,6);
click('[data-genre="Fantasy"]');assert.equal(all('.browse-grid .tile').length,2);
$('#search').value='Caminandes';$('#search').dispatchEvent(new w.Event('input'));assert.equal(all('.tile').length,2);
$('#search').value='no-such-title';$('#search').dispatchEvent(new w.Event('input'));assert.match($('#content').textContent,/No matches/);$('#search').value='';
route('TV');assert.equal(all('.tile').length,16);click('[data-title="caminandes3"]');assert($('#modal').open);assert.equal(all('#quality option').length,3);assert.match($('#player').src,/video.blender.org.*480.mp4/);assert.match($('#details').textContent,/Blender Foundation/);
click('#saveMovie');assert.equal(JSON.parse(w.localStorage.getItem('shuttle-list'))[0],'caminandes3');click('[data-action="close"]');assert.equal($('#player'),null);
route('My List');assert.equal(all('.tile').length,1);click('.tile');click('#saveMovie');click('[data-action="close"]');route('My List');assert.equal(all('.tile').length,0);
route('Originals');assert.equal(all('.tile').length,0);assert.equal($('#player'),null);assert.match($('#content').textContent,/No originals available/);
route('Settings');click('[data-action="tv"]');assert(w.document.body.classList.contains('tv-mode'));assert.equal(w.localStorage.getItem('shuttle-tv'),'true');click('[data-action="tv"]');assert(!w.document.body.classList.contains('tv-mode'));
click('[data-action="licenses"]');assert.equal(all('.license-entry').length,22);click('[data-action="close"]');
run('licenses();privacy()');assert.match($('#details').textContent,/Privacy & advertising/);click('[data-action="allow-ads"]');assert.equal(w.localStorage.getItem('shuttle-ads'),'"allowed"');assert.equal($('#adsense-script'),null);assert($('#advertisement').hidden);
run("progress={bbb:{time:42,duration:596}};render()");route('Home');assert.match($('#content').textContent,/Continue Watching/);route('Settings');click('[data-action="clear"]');assert.equal(w.localStorage.getItem('shuttle-progress'),'{}');
run(`window.SHUTTLEBUG_CONFIG.sponsor={name:'Test sponsor',message:'Test creative',url:'https://example.com'};renderAds()`);assert(!$('#advertisement').hidden);assert.equal($('#advertisement a').rel,'sponsored noopener');assert.match($('#advertisement').textContent,/ADVERTISEMENT/);
run(`window.SHUTTLEBUG_CONFIG.sponsor={name:'Bad',message:'',url:'javascript:alert(1)'};renderAds()`);assert($('#advertisement').hidden);
run(`window.SHUTTLEBUG_CONFIG.sponsor=null;window.SHUTTLEBUG_CONFIG.adsense={enabled:true,publisher:'ca-pub-1234567890123456',slot:'12345678',consentReady:false};renderAds()`);assert.equal($('#adsense-script'),null);
run(`window.SHUTTLEBUG_CONFIG.adsense.consentReady=true;localStorage.setItem('shuttle-ads','"declined"');renderAds()`);assert.equal($('#adsense-script'),null);
run(`localStorage.setItem('shuttle-ads','"allowed"');renderAds()`);assert.match($('#adsense-script').src,/pagead2.googlesyndication.com/);assert.equal($('.adsbygoogle').dataset.adSlot,'12345678');
// Canceled original cannot be opened or exposed through search.
run("openTitle('block-scene-1')");assert.equal($('#player'),null);assert.equal($('#modal').open,false);assert(!w.SHUTTLEBUG_CATALOG.some(m=>['block','block-scene-1'].includes(m.id)));
run("openTitle('valkaama')");assert($('#player'));assert.equal($('#player').hasAttribute('crossorigin'),false);assert.equal($('#player track').default,true);assert.match($('#details').textContent,/English subtitles/);click('[data-action="close"]');
route('TV');assert.equal(all('#content h2').length,4);assert.match($('#content').textContent,/Pepper & Carrot/);
// Homepage curation and natural-audio provenance for the new release.
route('Home');assert.equal($('.hero h1').textContent,'Spring');assert.equal($('.hero [data-title]').dataset.title,'spring');assert.match($('#content').textContent,/Start Here/);assert.match($('#content').textContent,/Longer Episodes/);
const newTitles=w.SHUTTLEBUG_CATALOG.filter(m=>m.collection==='new-2026-11-16');assert.equal(newTitles.length,10);assert(newTitles.every(m=>['recorded-human','no-dialogue'].includes(m.audioType)&&m.audioEvidence));
assert.equal(w.SHUTTLEBUG_CATALOG.filter(m=>m.series==='BBS: The Documentary').length,8);assert(w.SHUTTLEBUG_CATALOG.filter(m=>m.series==='BBS: The Documentary').every(m=>m.duration>1200));
run("openTitle('bbs1')");assert.equal($('#player').hasAttribute('crossorigin'),false);assert.equal(all('#quality option').length,2);assert.match($('#details').textContent,/Archival standard-definition/);click('[data-action="close"]');
// New live-action series keeps original speech and publisher subtitles.
const sideTitles=w.SHUTTLEBUG_CATALOG.filter(m=>m.series==='SideWays');assert.equal(sideTitles.length,3);assert.deepEqual(Array.from(sideTitles,m=>m.episode),[1,2,4]);assert(sideTitles.every(m=>m.audioType==='recorded-human'&&m.license==='CC BY-SA 3.0'));
run("openTitle('sideways2')");assert.equal($('#player track').default,true);assert.match($('#player track').src,/sideways2-en.vtt/);assert.equal(all('#quality option').length,3);click('[data-action="close"]');
for(const m of sideTitles){assert(fs.existsSync('.'+m.image));for(const c of m.captions)assert(fs.readFileSync('.'+c.url,'utf8').startsWith('WEBVTT'));}
// Catalog/manifest/service-worker contracts are checked without mocking their production code.
const cat=w.SHUTTLEBUG_CATALOG;for(const m of cat.filter(m=>m.sources.length)){assert(m.credit);if(!m.preview)assert(m.rights&&m.source&&m.license);for(const s of m.sources)assert(s.url.startsWith('/media/')||['video.blender.org','archive.org','videos.side-ways.net'].includes(new URL(s.url).hostname));}
const manifest=JSON.parse(fs.readFileSync('manifest.json'));assert.equal(manifest.start_url,'/');assert.equal(manifest.display,'standalone');for(const i of manifest.icons)assert(fs.existsSync('.'+i.src));
const listeners={};const ctx={self:{location:{origin:'https://shuttlebug.onrender.com'},addEventListener:(k,v)=>listeners[k]=v},URL};vm.runInNewContext(fs.readFileSync('sw.js','utf8')+';self.testShell=SHELL;',ctx);for(const url of ['https://video.blender.org/test.mp4','https://shuttlebug.onrender.com/config.js']){let intercepted=false;listeners.fetch({request:{url,method:'GET',headers:{has:()=>false}},respondWith:()=>intercepted=true});assert.equal(intercepted,false);}
const html=fs.readFileSync('index.html','utf8');
const linkedAssets=[...html.matchAll(/(?:src|href)="(\/assets\/[a-f0-9]{12}\/(?:catalog\.js|app\.js|config\.js|styles\.css))"/g)].map(m=>m[1]);assert.equal(linkedAssets.length,4);
for(const asset of linkedAssets){assert.equal(fs.readFileSync('.'+asset,'utf8'),fs.readFileSync(asset.split('/').pop(),'utf8'));if(!asset.endsWith('/config.js'))assert(ctx.self.testShell.includes(asset));else{let intercepted=false;listeners.fetch({request:{url:'https://shuttlebug.onrender.com'+asset,method:'GET',headers:{has:()=>false}},respondWith:()=>intercepted=true});assert.equal(intercepted,false);}}
const releaseEntry=ctx.self.testShell.find(p=>p.startsWith('/releases/'));assert.equal(fs.readFileSync('.'+releaseEntry,'utf8'),html);
console.log('PASS: navigation rendering, genres, search, library, quality controls, credits, watchlist save/remove, originals, TV settings, dialog replacement, progress clearing, sponsor rendering/URL safety, ad consent and configuration gates, catalog, manifest/icons, no remote-film/config caching.');dom.window.close();

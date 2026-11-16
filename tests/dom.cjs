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
route('Movies');assert.equal(all('.browse-grid .tile').length,3);
click('[data-genre="Fantasy"]');assert.equal(all('.browse-grid .tile').length,1);
$('#search').value='Caminandes';$('#search').dispatchEvent(new w.Event('input'));assert.equal(all('.tile').length,2);
$('#search').value='no-such-title';$('#search').dispatchEvent(new w.Event('input'));assert.match($('#content').textContent,/No matches/);$('#search').value='';
route('TV');assert.equal(all('.tile').length,2);click('[data-title="caminandes3"]');assert($('#modal').open);assert.equal(all('#quality option').length,3);assert.match($('#player').src,/video.blender.org.*480.mp4/);assert.match($('#details').textContent,/Blender Foundation/);
click('#saveMovie');assert.equal(JSON.parse(w.localStorage.getItem('shuttle-list'))[0],'caminandes3');click('[data-action="close"]');assert.equal($('#player'),null);
route('My List');assert.equal(all('.tile').length,1);click('.tile');click('#saveMovie');click('[data-action="close"]');route('My List');assert.equal(all('.tile').length,0);
route('Originals');click('.tile');assert.equal($('#player'),null);assert.match($('#details').textContent,/In production/);click('[data-action="close"]');
route('Settings');click('[data-action="tv"]');assert(w.document.body.classList.contains('tv-mode'));assert.equal(w.localStorage.getItem('shuttle-tv'),'true');click('[data-action="tv"]');assert(!w.document.body.classList.contains('tv-mode'));
click('[data-action="licenses"]');assert.equal(all('.license-entry').length,5);click('[data-action="close"]');
run('licenses();privacy()');assert.match($('#details').textContent,/Privacy & advertising/);click('[data-action="allow-ads"]');assert.equal(w.localStorage.getItem('shuttle-ads'),'"allowed"');assert.equal($('#adsense-script'),null);assert($('#advertisement').hidden);
run("progress={bbb:{time:42,duration:596}};render()");route('Home');assert.match($('#content').textContent,/Continue Watching/);route('Settings');click('[data-action="clear"]');assert.equal(w.localStorage.getItem('shuttle-progress'),'{}');
run(`window.SHUTTLEBUG_CONFIG.sponsor={name:'Test sponsor',message:'Test creative',url:'https://example.com'};renderAds()`);assert(!$('#advertisement').hidden);assert.equal($('#advertisement a').rel,'sponsored noopener');assert.match($('#advertisement').textContent,/ADVERTISEMENT/);
run(`window.SHUTTLEBUG_CONFIG.sponsor={name:'Bad',message:'',url:'javascript:alert(1)'};renderAds()`);assert($('#advertisement').hidden);
run(`window.SHUTTLEBUG_CONFIG.sponsor=null;window.SHUTTLEBUG_CONFIG.adsense={enabled:true,publisher:'ca-pub-1234567890123456',slot:'12345678',consentReady:false};renderAds()`);assert.equal($('#adsense-script'),null);
run(`window.SHUTTLEBUG_CONFIG.adsense.consentReady=true;localStorage.setItem('shuttle-ads','"declined"');renderAds()`);assert.equal($('#adsense-script'),null);
run(`localStorage.setItem('shuttle-ads','"allowed"');renderAds()`);assert.match($('#adsense-script').src,/pagead2.googlesyndication.com/);assert.equal($('.adsbygoogle').dataset.adSlot,'12345678');
// Catalog/manifest/service-worker contracts are checked without mocking their production code.
const cat=w.SHUTTLEBUG_CATALOG;for(const m of cat.filter(m=>m.sources.length)){assert(m.credit&&m.rights&&m.source&&m.license);for(const s of m.sources)assert(new URL(s.url).hostname==='video.blender.org');}
const manifest=JSON.parse(fs.readFileSync('manifest.json'));assert.equal(manifest.start_url,'/');assert.equal(manifest.display,'standalone');for(const i of manifest.icons)assert(fs.existsSync('.'+i.src));
const listeners={};const ctx={self:{location:{origin:'https://shuttlebug.onrender.com'},addEventListener:(k,v)=>listeners[k]=v},URL};vm.runInNewContext(fs.readFileSync('sw.js','utf8'),ctx);for(const url of ['https://video.blender.org/test.mp4','https://shuttlebug.onrender.com/config.js']){let intercepted=false;listeners.fetch({request:{url,method:'GET',headers:{has:()=>false}},respondWith:()=>intercepted=true});assert.equal(intercepted,false);}
console.log('PASS: navigation rendering, genres, search, library, quality controls, credits, watchlist save/remove, originals, TV settings, dialog replacement, progress clearing, sponsor rendering/URL safety, ad consent and configuration gates, catalog, manifest/icons, no remote-film/config caching.');dom.window.close();

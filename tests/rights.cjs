const {JSDOM}=require(process.env.JSDOM_MODULE||'jsdom');
const fs=require('node:fs');const assert=require('node:assert/strict');
const dom=new JSDOM(fs.readFileSync('index.html','utf8'),{url:'https://shuttlebug.onrender.com',runScripts:'outside-only',pretendToBeVisual:true});
const vm=require('node:vm');const context=dom.getInternalVMContext();const w=dom.window;w.matchMedia=()=>({matches:false});w.scrollTo=()=>{};w.confirm=()=>true;
w.HTMLDialogElement.prototype.showModal=function(){this.open=true};w.HTMLDialogElement.prototype.close=function(){this.open=false;this.dispatchEvent(new w.Event('close'))};
w.HTMLMediaElement.prototype.load=function(){};w.HTMLMediaElement.prototype.pause=function(){};
w.HTMLMediaElement.prototype.play=function(){return Promise.resolve()};
for(const file of ['catalog.js','config.js','app.js']){vm.runInContext(fs.readFileSync(file,'utf8'),context);}
const $=s=>w.document.querySelector(s),all=s=>[...w.document.querySelectorAll(s)];
function click(s){assert($(s),'Missing '+s);$(s).click()}
function run(s){return vm.runInContext(s,context)}
function route(page){run(`page=${JSON.stringify(page)};genre='All';render()`)}

route('Movies');assert.equal(all('.tile').length,6);assert.equal(all('[data-title="sita"]').length,0);run("openTitle('sita')");assert.equal($('#player'),null);route('TV');assert.equal(all('.tile').length,11);run('licenses()');assert.equal(all('.license-entry').length,17);assert.equal(w.SHUTTLEBUG_CATALOG.filter(m=>m.rightsStatus==='hold').length,18);console.log('PASS actual rights gate: 17 reviewed, 18 held, held deep-link blocked, correct credits');dom.window.close();

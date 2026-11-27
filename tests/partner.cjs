const {chromium}=require('playwright');const assert=require('node:assert/strict');const fs=require('node:fs');
(async()=>{const browser=await chromium.launch({executablePath:process.env.PLAYWRIGHT_USE_BUNDLED ? undefined : '/usr/bin/chromium',args:['--no-sandbox']});const p=await browser.newPage({viewport:{width:1920,height:1080}});const errors=[];p.on('pageerror',e=>errors.push(e.message));await p.goto(process.env.TEST_URL||'http://127.0.0.1:8765/?ads=test');await p.locator('.hero').waitFor();
assert.equal(await p.locator('.hero h1').innerText(),'Big Buck Bunny');await p.locator('[data-page="Movies"]').click();await p.locator('.browse-grid').first().waitFor();assert.equal(await p.locator('[data-title="sita"]').count(),0);await p.locator('[data-title="bbb"]').click();await p.locator('[data-action="play"]').click();await p.locator('.test-ad video').waitFor();await p.waitForFunction(()=>document.querySelector('.test-ad video')?.currentTime>0.3);assert.match(await p.locator('.test-ad').innerText(),/NO PAID REVENUE/);await p.waitForFunction(()=>!document.querySelector('.test-ad'),{},{timeout:15000});await p.waitForFunction(()=>document.querySelector('#player').currentTime>0.2,{},{timeout:45000});const decoded=await p.locator('#player').evaluate(v=>({width:v.videoWidth,duration:v.duration}));assert(decoded.width>0);await p.locator('#player').evaluate(v=>{v.currentTime=31;v.dispatchEvent(new Event('timeupdate'));});await p.locator('.test-ad').waitFor();await p.getByText('End test ad',{exact:true}).click();await p.waitForFunction(()=>!document.querySelector('.test-ad'));await p.evaluate(()=>document.dispatchEvent(new KeyboardEvent('keydown',{key:'MediaPause',keyCode:19,bubbles:true})));assert(await p.locator('#player').evaluate(v=>v.paused));await p.evaluate(()=>document.dispatchEvent(new KeyboardEvent('keydown',{key:'MediaPlay',keyCode:415,bubbles:true})));await p.waitForFunction(()=>!document.querySelector('#player').paused);await p.locator('[data-action="fullscreen"]').click();await p.waitForFunction(()=>!!document.fullscreenElement);await p.evaluate(()=>document.exitFullscreen());await p.waitForFunction(()=>!document.fullscreenElement);await p.evaluate(()=>document.dispatchEvent(new KeyboardEvent('keydown',{key:'GoBack',keyCode:461,bubbles:true})));await p.locator('#player').waitFor({state:'detached'});assert.equal(await p.locator('#player').count(),0);
await p.locator('[data-page="Home"]').click();await p.locator('[data-page="Home"]').focus();await p.keyboard.press('ArrowRight');assert.equal(await p.evaluate(()=>document.activeElement.dataset.page),'TV');await p.goto('http://127.0.0.1:8765/');await p.locator('.hero [data-title]').click();await p.locator('[data-action="play"]').click();await p.waitForTimeout(500);assert.equal(await p.locator('.test-ad').count(),0);assert.deepEqual(errors,[]);
// Partner inquiries must prepare mail, never pretend a lead was submitted.
for (const width of [390,1440]) {
 await p.setViewportSize({width,height:900});
 await p.goto('http://127.0.0.1:8765/partners.html');
 assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 await p.getByText('Discuss your films',{exact:true}).click();
 assert.equal(await p.locator('[name=interest]').inputValue(),'Film licensing');
 for(const [name,value] of Object.entries({name:'Example Person',company:'Example Films',email:'example@example.com',message:'Sample film inquiry <script>literal text</script>'})) await p.locator(`[name=${name}]`).fill(value);
 await p.getByRole('button',{name:'Prepare email'}).click();
 await p.locator('#email-status').filter({hasText:'not sent'}).waitFor();
 assert.match(await p.locator('#prepared-message').inputValue(),/<script>literal text/);
 await p.goto('http://127.0.0.1:8765/demo.html');
 assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 await p.getByRole('link',{name:'Start watching',exact:true}).click();
 await p.locator('.hero').waitFor();
}
// Real decoding and automatic return for the owned house promos.
await p.goto('http://127.0.0.1:8765/');await p.locator('.hero [data-title]').click();
for(const name of ['Deep_Bumper_10s_Quiet.mp4','Deep_Dance_10s.mp4']) {
 await p.getByRole('button',{name:'Preview commercial break',exact:true}).click();
 await p.locator('.house-bumper video').waitFor();
 assert((await p.locator('.house-bumper video').getAttribute('src')).endsWith(name));
 await p.waitForFunction(()=>document.querySelector('.house-bumper video')?.currentTime>0.2);
 assert((await p.locator('.house-bumper video').evaluate(v=>v.videoWidth))>0);
 await p.locator('.house-bumper').waitFor({state:'detached',timeout:15000}).catch(async e=>{console.log('BUMPER STATE',await p.locator('.house-bumper video').evaluate(v=>({time:v.currentTime,duration:v.duration,paused:v.paused,seeking:v.seeking,ended:v.ended,ready:v.readyState,error:v.error?.message})));throw e;});
}
await p.locator('#player').evaluate(v=>v.dispatchEvent(new Event('ended')));
await p.locator('.house-bumper').waitFor();await p.getByRole('button',{name:'Finish commercial break',exact:true}).click();
assert.match(await p.locator('#playStatus').innerText(),/Finished/);
assert.deepEqual(errors,[]);await browser.close();console.log('PASS rights hold, real film decode, test pre/mid-roll decode, resume, media keys, fullscreen, Back, remote arrows, paid ads disabled',decoded);})().catch(e=>{console.error(e);process.exit(1)});

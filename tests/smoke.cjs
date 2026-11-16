const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const base=process.env.TEST_URL||'http://127.0.0.1:8765';
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',args:['--no-sandbox']});
 const context=await browser.newContext({viewport:{width:1440,height:1000}});
 const page=await context.newPage();let errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(base);await page.locator('.hero').waitFor();assert.match(await page.title(),/Home/);
 for(const nav of ['TV','Movies','Originals','My List','Settings','Home']){await page.locator(`[data-page="${nav}"]`).click();await page.waitForURL('**/#'+encodeURIComponent(nav));assert(await page.locator(`[data-page="${nav}"]`).getAttribute('aria-current')==='page');}
 await page.locator('[data-page="Movies"]').click();assert.equal(await page.locator('.browse-grid .tile').count(),4);
 await page.locator('[data-genre="Fantasy"]').click();assert.equal(await page.locator('.browse-grid .tile').count(),1);
 await page.locator('#search').fill('no-such-title');assert.match(await page.locator('#content').innerText(),/No matches/);
 await page.locator('#search').fill('caminandes');assert.equal(await page.locator('.browse-grid .tile').count(),2);
 await page.locator('#search').fill('');await page.locator('[data-page="TV"]').click();await page.locator('[data-title="caminandes3"]').click();
 await page.locator('#player').waitFor();await page.locator('#saveMovie').click();await page.keyboard.press('Escape');
 await page.locator('[data-page="My List"]').click();assert.equal(await page.locator('.tile').count(),1);await page.reload();assert.equal(await page.locator('.tile').count(),1);
 await page.locator('.tile').click();await page.waitForFunction(()=>document.getElementById('player').readyState>=1,{},{timeout:45000});
 await page.locator('[data-action="play"]').click();await page.waitForFunction(()=>document.getElementById('player').currentTime>1,{},{timeout:30000});
 const media=await page.locator('#player').evaluate(v=>({duration:v.duration,time:v.currentTime,width:v.videoWidth}));assert(media.width>0);console.log('REAL PLAYBACK',media);
 await page.locator('[data-action="play"]').click();await page.locator('#player').evaluate(v=>{v.currentTime=25;v.dispatchEvent(new Event('timeupdate'));});await page.keyboard.press('Escape');
 await page.locator('[data-page="Home"]').click();assert.match(await page.locator('#content').innerText(),/Continue Watching/);
 await page.locator('[data-page="Settings"]').click();await page.locator('[data-action="tv"]').click();assert(await page.locator('body').evaluate(el=>el.classList.contains('tv-mode')));await page.reload();assert(await page.locator('body').evaluate(el=>el.classList.contains('tv-mode')));
 await page.locator('[data-action="licenses"]').first().click();assert.equal(await page.locator('.license-entry').count(),9);
 // Replacing one dialog with another must not erase its new contents.
 await page.evaluate(()=>{licenses();privacy();});await page.waitForTimeout(100);assert.match(await page.locator('#details').innerText(),/Privacy & advertising/);await page.keyboard.press('Escape');
 await page.locator('[data-action="tv"]').click();
 await page.locator('[data-page="Originals"]').click();await page.getByText('No originals available right now.',{exact:true}).waitFor();assert.equal(await page.locator('[data-title="block"]').count(),0);assert.equal(await page.locator('#player').count(),0);
 await page.locator('[data-page="Home"]').click();await page.locator('[data-page="Home"]').focus();await page.keyboard.press('ArrowRight');assert.equal(await page.evaluate(()=>document.activeElement.dataset.page),'TV');
 const manifest=await page.evaluate(async()=>await(await fetch('/manifest.json')).json());assert.equal(manifest.display,'standalone');for(const icon of manifest.icons)assert((await context.request.get(base+icon.src)).ok());
 await page.evaluate(async()=>await navigator.serviceWorker.ready);await page.reload();await page.waitForFunction(()=>!!navigator.serviceWorker.controller);await context.setOffline(true);await page.reload();await page.locator('.hero').waitFor();assert(await page.locator('#connection').isVisible());await context.setOffline(false);
 assert.equal(await page.locator('#advertisement').isVisible(),false);
 await page.screenshot({path:'/tmp/shuttlebug-desktop.png',fullPage:true});
 await context.close();
 const phone=await browser.newContext({viewport:{width:390,height:844},isMobile:true,deviceScaleFactor:1});const mobile=await phone.newPage();await mobile.goto(base);await mobile.locator('.hero').waitFor();assert(await mobile.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));await mobile.screenshot({path:'/tmp/shuttlebug-phone.png',fullPage:true});await mobile.locator('[data-page="Settings"]').click();assert(await mobile.locator('[data-action="install"]').isVisible());
 assert.deepEqual(errors,[]);await browser.close();console.log('PASS navigation, filters, search, watchlist persistence, actual video decode/play, progress, TV layout persistence, credits, dialog replacement, originals, remote arrows, manifest/icons, offline shell, ads disabled, phone layout.');
})().catch(e=>{console.error(e);process.exit(1)});

const {spawnSync}=require('node:child_process');const path=require('node:path');const fs=require('node:fs');const os=require('node:os');const temp=fs.mkdtempSync(path.join(os.tmpdir(),'shuttlebug-brs-'));
for(const test of ['logic','controller']){
const inputs=test==='logic'?['source/Logic.brs']:['source/Logic.brs','components/ShuttlebugScene.brs'];
const r=spawnSync(path.resolve('node_modules/.bin/brs'),['--root',temp,...inputs.map(p=>path.resolve(p)),path.resolve('tests/'+test+'.brs')],{encoding:'utf8'});
process.stdout.write(r.stdout||'');process.stderr.write(r.stderr||'');
if(r.status!==0||!r.stdout.includes('PASS ')||r.stdout.includes('FAIL'))process.exit(1);

}
fs.rmSync(temp,{recursive:true,force:true});

"""Version app assets together so a cached catalog cannot hide a newly published library."""
from pathlib import Path
import hashlib,re,shutil
root=Path(__file__).resolve().parents[1]
version=hashlib.sha256(b''.join((root/p).read_bytes() for p in ['app.js','catalog.js','config.js','styles.css'])).hexdigest()[:12]
asset_dir=root/'assets'/version
asset_dir.mkdir(parents=True,exist_ok=True)
for name in ['app.js','catalog.js','config.js','styles.css']:
    shutil.copyfile(root/name,asset_dir/name)
p=root/'index.html';s=p.read_text()
s=re.sub(r'/(?:assets/[a-f0-9]{12}/)?((?:app|catalog|config)\.js|styles\.css)(?:\?v=[^"\s]+)?',lambda m:'/assets/'+version+'/'+m[1],s);p.write_text(s)
# A review entry point has the same content and absolute asset URLs as Home.
# Retain past releases so a cached HTML page can still load its matching assets.
release_dir=root/'releases'/version
release_dir.mkdir(parents=True,exist_ok=True)
(release_dir/'index.html').write_text(s)
p=root/'sw.js';s=p.read_text();s=re.sub(r"const RELEASE = '[^']+';", "const RELEASE = '"+version+"';",s);p.write_text(s)
print(version)

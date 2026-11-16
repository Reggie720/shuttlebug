"""Version app assets together so a cached catalog cannot hide a newly published library."""
from pathlib import Path
import hashlib,re
root=Path(__file__).resolve().parents[1]
version=hashlib.sha256(b''.join((root/p).read_bytes() for p in ['app.js','catalog.js','config.js','styles.css'])).hexdigest()[:12]
p=root/'index.html';s=p.read_text()
s=re.sub(r'(/(?:app|catalog|config)\.js|/styles\.css)(?:\?v=[^"\s]+)?',lambda m:m[1]+'?v='+version,s);p.write_text(s)
p=root/'sw.js';s=p.read_text();s=re.sub(r"const RELEASE = '[^']+';", "const RELEASE = '"+version+"';",s);p.write_text(s)
print(version)

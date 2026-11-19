from pathlib import Path
import zipfile,hashlib,json
root=Path(__file__).resolve().parents[1];out=root/'packages/Shuttlebug_Roku_Developer.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for folder in ['source','components','data','images','media']:
  for p in sorted((root/folder).rglob('*')):
   if p.is_file():
    info=zipfile.ZipInfo(p.relative_to(root).as_posix(),date_time=(1980,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,p.read_bytes())
 info=zipfile.ZipInfo('manifest',date_time=(1980,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,(root/'manifest').read_bytes())
with zipfile.ZipFile(out) as z:
 assert 'manifest' in z.namelist() and 'source/main.brs' in z.namelist()
 assert not any(n.startswith(('node_modules/','roku/')) for n in z.namelist())
(root/'packages/SHA256SUMS').write_text(hashlib.sha256(out.read_bytes()).hexdigest()+'  '+out.name+'\n')
print('Built sideload ZIP',out.stat().st_size,'bytes')

"""Validate publishable content, local links, and actual multi-frame GIF files."""
from pathlib import Path
import json,re,subprocess,hashlib
ROOT=Path(__file__).resolve().parents[1]
errors=[]
components=json.loads((ROOT/'assets/components.json').read_text())
assert [c['id'] for c in components]==list(range(1,31))
skill=(ROOT/'SKILL.md').read_text();assert skill.startswith('---\nname: cooper-video-editing-skill\n')
for path in ROOT.rglob('*'):
 if not path.is_file() or any(x in path.parts for x in ['node_modules','.git']):continue
 if path.suffix not in ['.md','.js','.cjs','.css','.html','.json','.py','.yaml']:continue
 text=path.read_text()
 # No machine-specific paths, signed download URLs or binding credentials.
 if path.name != 'validate.py':
  for pattern in [r'/Users/[^/\s]+/',r'q-sign-(?:signature|algorithm)=',r'Bearer\s+mrb1\.']:
   if re.search(pattern,text):errors.append(f'{path.relative_to(ROOT)}: prohibited private content')
 if path.suffix=='.md':
  for href in re.findall(r'\]\(([^)]+)\)',text):
   if not href.startswith(('http://','https://','#','mailto:')) and not (path.parent/href.split('#')[0]).exists():errors.append(f'{path.relative_to(ROOT)}: missing link {href}')
for c in components:
 for key in ['gifBlue','gifGreen']:
  p=ROOT/c[key]
  if not p.exists():errors.append(f'Missing {p.name}');continue
  r=subprocess.run(['ffprobe','-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=nb_read_frames,width,height','-of','json',str(p)],capture_output=True,text=True,check=True)
  s=json.loads(r.stdout)['streams'][0]
  if int(s['nb_read_frames'])<20 or s['width']!=640 or s['height']!=360:errors.append(f'Invalid animation {p.name}')
for name in ['font-yansong.gif','font-flower.gif','font-noto.gif']:
 p=ROOT/'docs/assets/gifs'/name
 if not p.exists():errors.append(f'Missing {name}')
media=ROOT/'docs/assets/media'
expected={name+ext for name in ['person','screen','wool','oil'] for ext in ['.svg','.png']}
if {p.name for p in media.iterdir() if p.is_file()}!=expected:errors.append('Unexpected media file in anonymous public package')
provenance=ROOT/'assets/media-provenance.json'
if provenance.exists():
 for item in json.loads(provenance.read_text())['files']:
  if hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest()!=item['sha256']:errors.append('Media provenance mismatch: '+item['path'])
else:errors.append('Missing anonymous media provenance')
font=ROOT/'docs/assets/fonts/NotoSerifSC.ttf'
if font.stat().st_size<1_000_000:errors.append('Font unexpectedly small or incomplete')
print(json.dumps({'components':len(components),'sceneGifs':60,'fontGifs':3,'errors':errors},ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))

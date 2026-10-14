"""Build all public entry pages from core rules and structured component manifest."""
from pathlib import Path
import json,re,html
ROOT=Path(__file__).resolve().parents[1]
components=json.loads((ROOT/'assets/components.json').read_text())
core=(ROOT/'references/core.md').read_text().replace('](../', '](')
front='---\nname: cooper-video-editing-skill\ndescription: 为面向 AI 新手的中文口播进行精剪、字幕、B-roll、蓝白或黑绿包装；包含人物前后层次、雾面玻璃、羽化卡、SVG、知识卡鱼眼巡游、增长可视化的 30 个代码动效与 GIF。用于应用或延续 Cooper 的剪辑规范、制作可编辑包装和实际视频验收。\n---\n\n'
sections=[]
for c in components:
 i=c['id'];sections.append(f'''### {i:02} · {c['name']}

**适用**：{c['trigger']}。**状态**：{c['status']}。

{c['description']} {c['rules']}

**验收**：{c['acceptance']} [交互预览](https://cooperchx.github.io/cooper-video-editing-skill/?scene={i}) · [代码](docs/app.js)

| 蓝白 | 黑＋正绿 |
|---|---|
| ![{i:02} 蓝白 {c['name']}]({c['gifBlue']}) | ![{i:02} 黑绿 {c['name']}]({c['gifGreen']}) |
''')
tail='''
## 详细规则与交付状态

- [口播精剪、字幕、镜头、素材、声音与阅读节奏](references/editorial.md)
- [视觉系统、主题、形状材质与候选方向](references/visual-system.md)
- [字体来源、样张、授权与替代边界](references/typography.md)
- [代码运行、参数接口、Remotion / ChatCut 适配](references/runtimes.md)
- [验证记录与实际能力边界](references/validation.md)
- [组件数据](assets/components.json) · [设计参数](assets/tokens.json) · [许可与素材范围](NOTICE.md)

本版包含 30 个浏览器场景、60 个双主题动效 GIF、3 个字体 GIF。匿名人物、虚构界面与代码纹理用于展示版式；连续口播、动态抠像、音轨与最终 MP4 仍需接入项目。新增的三类候选效果尚未实现，不算在 30 项之内。
'''
body=core+'\n'+'\n'.join(sections)+tail
(ROOT/'SKILL.md').write_text(front+body)
(ROOT/'README.md').write_text(body)
(ROOT/'references/components.md').write_text('# 组件规则索引\n\n详见根目录 [SKILL.md](../SKILL.md) 的 30 项图鉴。机器可读参数见 [components.json](../assets/components.json)。代码见 [app.js](../docs/app.js)。\n')
# Minimal Markdown renderer for this repository, no remote scripts or build dependencies.
def inline(t):
 t=html.escape(t)
 t=re.sub(r'!\[([^]]*)\]\(([^)]+)\)',r'<img loading="lazy" alt="\1" src="\2">',t)
 t=re.sub(r'\[([^]]*)\]\(([^)]+)\)',r'<a href="\2">\1</a>',t)
 t=re.sub(r'`([^`]+)`',r'<code>\1</code>',t)
 t=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',t)
 return t

def markdown(s):
 out=[];fence=False;table=False
 for line in s.splitlines():
  if line.startswith('```'):
   out.append('</code></pre>' if fence else '<pre><code>');fence=not fence;continue
  if fence:out.append(html.escape(line)+'\n');continue
  if line.startswith('|'):
   if re.match(r'^\|[ :|\-]+\|$',line):continue
   if not table:out.append('<div class="table-wrap"><table>');table=True
   out.append('<tr>'+''.join('<td>'+inline(v.strip())+'</td>' for v in line.strip('|').split('|'))+'</tr>');continue
  if table:out.append('</table></div>');table=False
  m=re.match(r'^(#{1,6}) (.*)',line)
  if m:out.append(f'<h{len(m[1])}>{inline(m[2])}</h{len(m[1])}>')
  elif line.strip():out.append('<p>'+inline(line)+'</p>')
 if table:out.append('</table></div>')
 return '\n'.join(out)
# Root-relative Markdown files become actual rendered documentation pages.
def hrefs(s,base=''):
 def swap(m):
  target=m[1]
  if target.startswith(('http:','https:','#')):return m[0]
  if target.startswith('../'):target=target[3:]
  if target.startswith('docs/'):target=target[5:]
  if target.startswith('references/') and target.endswith('.md'):target=Path(target).stem+'.html'
  elif target=='SKILL.md':target='guide.html'
  elif target.endswith('.md') or target.startswith('assets/') and not target.startswith('assets/gifs'):
   target='https://github.com/cooperchx/cooper-video-editing-skill/blob/main/'+target
  return 'href="'+target+'"'
 s=re.sub(r'href="([^"]+)"',swap,s)
 s=re.sub(r'src="(?:\.\./)?docs/', 'src="',s)
 return s
style='''body{max-width:1160px;margin:auto;padding:32px 24px 80px;background:#f4f3ee;color:#132b59;font:16px/1.8 system-ui,sans-serif}a{color:#294acb;text-underline-offset:3px}h1{font-size:40px;line-height:1.25}h2{margin-top:64px;border-top:1px solid #bdcdf6;padding-top:28px}h3{margin-top:40px}p{max-width:1040px}img{display:block;width:100%;height:auto;border-radius:8px}table{width:100%;border-collapse:collapse;table-layout:fixed}td{vertical-align:top;padding:12px;border:1px solid #c8d1e2;overflow-wrap:anywhere}.table-wrap{overflow:auto}code{font:14px ui-monospace,monospace;background:#e8ebf1;padding:2px 5px}pre{padding:18px;overflow:auto;background:#e8ebf1;border-radius:8px}nav{position:sticky;top:0;background:#f4f3eef2;padding:12px 0;backdrop-filter:blur(10px)}@media(max-width:650px){body{padding:16px}h1{font-size:30px}td{padding:4px;font-size:12px}}'''
def page(title,content):return '<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+title+'</title><style>'+style+'</style><nav><a href="index.html">交互动效</a> · <a href="guide.html">完整 Skill 图鉴</a> · <a href="https://github.com/cooperchx/cooper-video-editing-skill">GitHub</a></nav><main>'+hrefs(markdown(content))+'</main></html>'
(ROOT/'docs/guide.html').write_text(page('Cooper · 完整剪辑 Skill 与 GIF 图鉴',body))
for f in (ROOT/'references').glob('*.md'):
 if f.stem in ['core','components']:continue
 (ROOT/f'docs/{f.stem}.html').write_text(page(f.stem,f.read_text()))
print('Built SKILL.md, README.md and static documentation pages')

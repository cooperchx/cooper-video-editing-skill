# 当前字体规范：全部使用得意黑

用户最新决定覆盖早期字体方案：**一级标题、二级标题、正文、字幕、卡片、花字、图表数字、SVG 标签和匿名示意素材文字，统一为得意黑 Smiley Sans。** 当前页面不再混用研宋、花仿宋或 Noto Serif SC。

![得意黑动态样张](../docs/assets/gifs/font-smiley.gif)

## 来源与许可

官方：[atelier-anchor/smiley-sans](https://github.com/atelier-anchor/smiley-sans)，版本 [v2.0.1](https://github.com/atelier-anchor/smiley-sans/releases/tag/v2.0.1)。字体采用 SIL OFL 1.1；完整许可保存在 [OFL.txt](../docs/assets/fonts/OFL.txt)。仓库包含未修改的 `SmileySans-Oblique.ttf` 和网页用 `SmileySans-Oblique.ttf.woff2`。

## 排版要求

得意黑字身窄而斜，中文和数字有明确的黑体重量。保留字体本身造型，不额外伪斜、伪粗或强行拉伸。标题与字幕的层级通过字号、颜色、位置、间距和停留时间区分。

提问卡文字先几何居中，再考虑倾斜字形做视觉检查。标题不溢出卡片，数字和单位不互相挤压，字幕按语义换行；保持已确认的轻柔阴影与底部安全区。

字体覆盖不等于任意语言全覆盖：更换具体文案后检查中文、字母、数字、箭头、特殊标点及缺字。缺字时说明情况，不悄悄恢复旧宋体。口播中很长的正文先拆句或分卡，不靠压缩字形解决。

## 实现

网页的 CSS 家族名为 `SmileySans`，加载本仓库 WOFF2。DOM、SVG 和字体简写均使用同一家族；素材中的文字也通过同一字体重新绘制。等待 `document.fonts.ready` 后再测量和取帧。

网页顶部仍可加载获授权的本地字体作临时比较；文件不上传，刷新恢复得意黑。正式项目中所有文字角色应保持得意黑，除非用户后来明确修改。

ChatCut、Remotion、浏览器的字体环境各自独立。接入时核实文件加载或可用字体标识，不能仅在配置里写下名称就宣称换字成功；实际检查标题、字幕和 SVG 数字的输出字形。

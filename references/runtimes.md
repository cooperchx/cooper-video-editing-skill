# 代码复用与渲染器适配

## 仓库里的真实实现

`docs/app.js` 是 30 个场景的可运行 JavaScript 实现，`docs/style.css` 提供材质、层级与双主题，`assets/components.json` 是组件清单，`assets/tokens.json` 是设计参数。浏览器逻辑画布为 1600×900，导出制作默认映射到 1920×1080。

当前公开示例全部为原创代码占位素材：匿名讲述者、虚构软件界面、两种纹理插画，不含用户照片、录屏或源视频帧。静态人物轮廓来自同一匿名绘图，只用于说明层级。网页展示构图和代码动画；它没有接入整段口播、连续抠像、音轨或 MP4 导出器。

## 本地运行与 GIF 重建

```sh
npm ci
npx playwright install chromium
npm run build:placeholders # 可选：重建匿名占位素材
npm run dev
# 浏览器打开 http://localhost:8765
npm run render:gifs
npm run check
npm test
```

依赖：Node 22+、Python 3、ffmpeg、Playwright Chromium。可设置 `CHROME_PATH` 使用本机兼容 Chromium。GIF 默认 640×360、10 fps、96 色，适合文档预览，不代表最终视频质量。

```sh
node scripts/render-gifs.cjs --themes=blue --ids=2,8,18,24 --width=640 --fps=10
```

执行后写入 `docs/assets/gifs/`，渲染记录写入 `assets/gif-render-report.json`。字体样张涉及单独授权文件，不能仅靠仓库中的开源替代自动重建商业字体样张。

## 浏览器逐帧接口

```js
await motionLibrary.ready;
motionLibrary.setTheme('blue'); // 'teal' = 黑＋正绿
motionLibrary.select(24, {autoplay: false});
motionLibrary.configure({title: '风格\n怎么选？', sub: '动画 / 漫剧', lens: 18});
motionLibrary.seek(2.0); // 秒；倒退与重新定位应得到同一结果
const state = motionLibrary.getState();
```

可编辑字段：`title`、`sub`、`accent`、`textScale`、`frost`、`lens`。其中内部多个子卡标签、数据值与坐标目前属于场景代码里的示例常量，**不是所有内容都已暴露为参数**；用于项目时必须按文稿和实际数据改代码，或扩展组件 props。

嵌入链接示例：`index.html?embed=1&scene=18&theme=blue&t=2`。纯画布隐藏控制面板，固定时间便于取帧。媒体鱼眼 17 支持本地图片/视频；视频素材是播放媒体，逐帧导出前需额外把媒体 currentTime 与场景时间同步。

## Remotion 接入

用 `useCurrentFrame()` / fps 算当前秒数，把逐帧逻辑迁入 React 组件；不能用 requestAnimationFrame 的墙钟推进离线渲染。素材使用 Remotion 对应视频/音频组件并绑定源起点；字体在开始渲染前加载。

已有独立参考工程：[素材鱼眼](https://github.com/cooperchx/remotion-fisheye-media-effect)、[原财务卡巡游](https://github.com/cooperchx/remotion-finance-card-tour)。第二个是早期参考复刻，并未自动同步本库后来的“知识文案＋中心限定畸变”修订。要复用最新样式，以本库 18 为准。

本仓库提供浏览器实现及移植规则，没有声称所有 30 个场景已经成为已验收的 Remotion 包。独立参考工程保留自己的许可与运行命令。

## ChatCut 接入

使用时读取已安装 ChatCut 插件的当前基础、Motion Graphics、口播剪辑与验证技能；先检查当前项目、时间线、字体、资产和工具 schema。不要硬编码旧项目 ID，也不要从本 Skill 猜测当前插件参数。

- 创建新时间线或副本，保留原剪辑；按用户授权范围选择替换。
- 包装代码可转为帧驱动 JSX；必要素材和字幕分轨。浏览器 CSS 的支持程度必须在当前渲染器实测。
- 特别检查 `backdrop-filter`、SVG filter、阴影、perspective、嵌套 3D 与图层顺序。旧版 ChatCut 导出无法用 backdrop-filter 直接采样背景；当前版本仍需验证，不能依赖浏览器结果推断。
- 真玻璃受限时使用半透填色、薄边、柔影和独立柔化背景的风格化材质，明确降级；人后效果受限时改成不挡人的邻近卡片，不能把静态抠像装成动态跟踪。
- 先验证短片的入场、稳定态、退场，再批量应用；完整播放与实际导出分别验收。

## 数据、蒙版和鱼眼约束

数据 09、25–30 的当前数值都是演示。液体先按圆面积反解高度；曲线使用真实序列、单位和时间轴；计数与形状同步，不能只改显示数字。

人像、蒙版、背景采用同一源时刻、裁切、缩放、帧率。每次剪切和变速后重算映射，检查头发、肩部、手部边缘。

巡游 18 的内容层使用 SVG displacement，中心半径内位移平滑归零，外框和阴影独立绘制。不要对整张卡做统一 lens warp，也不要对两套主题分别写出不同的变形边界。素材鱼眼 17 是 WebGL 像素采样，应检查目标浏览器 GPU/软件渲染支持。

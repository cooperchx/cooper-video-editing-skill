# 字体角色、来源与接入

## 不能合并成一个“同款字体”的四种状态

| 角色 | 当前识别与状态 | 复用要求 |
|---|---|---|
| 一级厚重标题参考 | 用户图中含「厚重的 Heavy 1987」，具体字体未核实 | 以原图字形为参考，先确认字库名称与文件，不能猜名字后标为同款 |
| 已认可卡片外观 | Aa研宋，文件内家族 AaYS Regular | 商业字库；仓库保留栅格 GIF 样张，不分发字体文件或字形全集 |
| 二级标题和字幕偏好 | 花仿宋 FlowerFangSong，版本 1.50 | 从作者发布渠道取得完整字体并确认授权、缺字和实际渲染；不要用少量网页分包冒充完整字库 |
| 公开网页默认 | Noto Serif SC | 开源替代，随仓库附 SIL OFL 1.1；不是研宋或花仿宋 |

### Aa研宋：当前卡片外观参考

![Aa研宋字体动态样张](../docs/assets/gifs/font-yansong.gif)

笔画较有重量，适合短标题、数字和卡片强调。来源记录指向 [Aa研宋产品页](https://www.17font.com/font/detail/cfa8a530b64811ed8a8467619fd45aaa.html)。某个公开代码仓库里存在字体文件并不自动授予再分发权。本仓库不提供商业字库下载，不把示例字形转成任意文字的可提取字形集。

### 花仿宋：用户指定二级标题与字幕

![花仿宋字体动态样张](../docs/assets/gifs/font-flower.gif)

字形修长、宋体衬线明显、带自身倾斜风格。小尺寸细笔画需在平台压缩后检查，不以增加粗黑描边补救。作者发布页将其标为免费商用，见 [猫啃网花仿宋说明](https://www.maoken.com/freefonts/12311.html) 与 [字体分发信息](https://fonts.zeoseven.com/items/12/)。使用者应按取得版本随附的许可使用；本库只保留有限文字的渲染样张。

### Noto Serif SC：公开可运行替代

![Noto Serif SC动态样张](../docs/assets/gifs/font-noto.gif)

[Google Fonts 官方源码](https://github.com/google/fonts/tree/main/ofl/notoserifsc)，[本库 OFL 许可](../docs/assets/fonts/OFL.txt)。中文宋体骨架、字形覆盖广，便于其他 Agent 离线复用。示例中的字号与换行已经用此字体重新检查，但不同字体的度量不完全相同。

## 加载实际字体

网页顶部「加载获授权的本地字体」接受 TTF/OTF/WOFF/WOFF2，仅在浏览器本地加载，不上传、不永久保存；刷新恢复默认字体。当前入口替换场景字体，用来观察整体度量，不是完整的多角色字体管理器。正式制作中应分别配置 heading/body/caption 字体。

CSS 中 `YanSong` 是历史兼容别名，公开仓库指向 **Noto Serif SC**，不代表装入了研宋。更换时同时处理别名以及 SVG、Canvas 中显式的字体设置。通过 `document.fonts.load()` / `document.fonts.ready` 等待加载，再测量与渲染。

ChatCut、Remotion、浏览器是不同字体环境：先查询当前可用字体和加载方式。固定标题可由已授权字体转有限字形路径；修改文字需重新生成路径。动态字幕必须保证完整字库覆盖，不能复用旧标题轮廓假装支持任意换字。

样张 GIF 是有限文案的外观演示，不是字体文件，也不是字体授权证书。

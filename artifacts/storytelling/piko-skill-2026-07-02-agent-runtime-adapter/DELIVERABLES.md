# Deliverables

## 1. 图文版本

入口：

`C:\PycharmProjects\Piko\artifacts\storytelling\piko-skill-2026-07-02-agent-runtime-adapter\article_visual\index.html`

定位：

- 白底长图文页面，接近公众号/知识文章排版。
- 包含标题、开场判断、机制图、五个 contract 卡片、视频首屏图例、实操步骤、真实限制、总结行动。
- 未使用外部版权图片；图表和截图位均为原创 HTML/CSS 绘制。

## 2. 视频版本

入口：

`C:\PycharmProjects\Piko\artifacts\storytelling\piko-skill-2026-07-02-agent-runtime-adapter\video_draft\index.html`

定位：

- 9:16 HyperFrames HTML 草稿。
- 普通 `file://` 打开时会自动轮播预览，不再黑屏。
- HyperFrames 渲染仍使用 registered paused timeline。

检查结果：

- `npx.cmd hyperframes validate --json`: ok
- `npx.cmd hyperframes inspect --json`: ok
- `npx.cmd hyperframes snapshot --at 1,5,12 --output snapshots`: ok

预览命令：

```powershell
cd C:\PycharmProjects\Piko\artifacts\storytelling\piko-skill-2026-07-02-agent-runtime-adapter\video_draft
npx.cmd hyperframes preview
```

渲染命令：

```powershell
cd C:\PycharmProjects\Piko\artifacts\storytelling\piko-skill-2026-07-02-agent-runtime-adapter\video_draft
npx.cmd hyperframes render --quality draft --output agent-runtime-adapter-draft.mp4
```


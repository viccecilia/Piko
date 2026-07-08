# 我让 Codex 每天扫描 GitHub 高星 AI 项目

竖屏 9:16 HyperFrames HTML 草稿。

## 内容

- `index.html`：75 秒短视频草稿，画幅 1080x1920。
- `SCRIPT.md`：对应口播稿，按场景拆分。
- `STORYBOARD.md`：视频结构、画面和口播节奏。

## 风格

- 知识类技术视频。
- 无真人出镜。
- 不使用外部图片。
- 主要用卡片、流程图、能力地图、字幕和 Gate 表达。

## 验证建议

在本目录运行：

```powershell
npx hyperframes lint --json
npx hyperframes validate --json
npx hyperframes inspect --json
```

确认无错误后，再打开 Studio 预览：

```powershell
npx hyperframes preview
```

用户确认后再渲染：

```powershell
npx hyperframes render --quality draft --output github-5-agent-frameworks-draft.mp4
```

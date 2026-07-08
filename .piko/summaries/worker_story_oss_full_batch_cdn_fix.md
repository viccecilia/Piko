# STORY + OSS Full Batch CDN Guardrail Fix

修改了什么

- 移除了 `artifacts/storytelling/piko-skill-radar-demo/index.html` 中的外部 GSAP CDN 依赖。
- 移除了 `artifacts/storytelling/github-5-agent-frameworks/video_draft/index.html` 中的外部 GSAP CDN 依赖。
- 移除了 `artifacts/storytelling/piko-skill-2026-07-02-agent-runtime-adapter/video_draft/index.html` 中的外部 GSAP CDN 依赖。
- 二次复验返工中，确认并再次清理了 `artifacts/storytelling/piko-skill-2026-07-02-agent-runtime-adapter/video_draft/index.html` 残留的 `cdn.jsdelivr.net` script 和 `window.gsap` fallback block。
- 三个 HTML artifact 均改为本地 CSS/local timeline metadata，不再需要默认联网。
- 在 `tests/test_storytelling_artifacts.py` 增加 HTML artifact guardrail 测试，扫描 `artifacts/storytelling/**/*.html`，禁止 `http://` 和 `https://` 外部资源引用。

每个任务状态

- 修复阻断外部 CDN 依赖：完成
- 补充 STORY HTML 外链扫描测试：完成
- 重跑局部测试：完成
- 重跑 STORY package verify：完成
- 重跑 discovery tests：完成
- 重跑全量 pytest：完成

验证结果

- `rg "https?://|cdn\.jsdelivr|gsap" artifacts/storytelling -g "*.html"`：无命中
- `python -m pytest tests\test_storytelling_artifacts.py -q`：3 passed
- `python -m packages.storytelling.story_package --verify`：status=passed
- `python -m pytest tests\test_discovery_search.py -q`：69 passed
- `python -m pytest`：162 passed, 3 skipped

协作验收结果

- 原阻断项已修复：storytelling HTML artifact 不再引用外部 CDN。
- 新增测试会防止后续 STORY HTML artifact 再默认联网。
- 未进入发布、上传、部署、commit、push、默认联网、默认 LLM、voice cloning 或 active template replacement。

未完成/风险

- 无阻断风险。
- 这些 HTML 仍是 draft artifact；视频最终渲染如需动画增强，应继续使用本地依赖或内联 CSS，不要引用外部 CDN。

下一轮建议

- 请 Piko-verify 复验 STORY + OSS full batch 的 CDN guardrail fix。
- 重点复查 HTML 外链扫描、新增测试、全量 pytest 和原 STORY/OSS proposal-only 边界。

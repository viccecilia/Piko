# Piko-verify Task Prompt: Verify SKILL-1 To SKILL-5

请一次性验证 SKILL-1 到 SKILL-5 连续批次。

入口 summary：

`C:\PycharmProjects\Piko\.piko\summaries\worker_SKILL-1-to-SKILL-5.md`

验证范围：

```text
SKILL-1-R01 -> SKILL-1-R02
SKILL-2-R01 -> SKILL-2-R02
SKILL-3-R01 -> SKILL-3-R02
SKILL-4-R01 -> SKILL-4-R02 -> SKILL-4-R03
SKILL-5-R01 -> SKILL-5-R02 -> SKILL-5-R03
```

必须检查：

- 所有 SKILL round summary 存在。
- 所有 SKILL stage summary 存在。
- final summary `.piko/summaries/worker_SKILL-1-to-SKILL-5.md` 存在。
- `round_status.json` 是 UTF-8 no BOM 且合法 JSON。
- worker 状态应为 `ready_for_verify`。

必须检查 artifacts：

- Skill runtime registry/manifest artifacts
- Skill lifecycle/drill eval artifacts
- Worker trace correlation artifacts
- Declarative eval suite/report artifacts
- Content quality rubric/scorecard/rewrite artifacts
- Social platform adapter contract artifacts
- One-click distribution dry-run package artifacts

必须运行的验证：

- `python -c "import json; json.load(open('.piko/round_status.json', encoding='utf-8')); print('round_status json ok')"`
- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- SKILL artifact JSON parse probes
- Content quality package probes
- Social distribution dry-run probes
- API/window probes if implemented
- Guardrail scan

核心验收点：

- Skill runtime 是候选治理能力，不自动安装外部 skill。
- Trace correlation 能把 worker run、round、artifact、verify verdict 串起来。
- Declarative eval queue 不替代 Piko-verify，只作为可重复测试入口。
- Content quality engine 能提升标题、引言、结构、证据和平台适配。
- Social distribution skill 默认 dry-run，不真实发布。
- 任何真实平台发布必须需要 human approval + platform credential + per-platform policy check。

安全禁止项：

- 不得发布、上传、部署、commit、push。
- 不得保存 token、cookie、API key、authorization、credentials。
- 不得绕过平台规则或自动群发垃圾内容。
- 不得默认调用 LLM。
- 不得使用未授权图片或长篇复制文本。
- 不得绕过 verification 或放宽 Gate。

通过时：

- 生成 `.piko/summaries/verify_SKILL-1-to-SKILL-5.md`
- 更新 `.piko/round_status.json`：
  - `worker_status=complete`
  - `verification_status=passed`
  - `last_verified_round=SKILL-1-to-SKILL-5`
  - `verification_summary_file=.piko/summaries/verify_SKILL-1-to-SKILL-5.md`
  - `next_round=null`

失败时：

- 生成失败验证报告。
- 更新 `.piko/round_status.json`：
  - `worker_status=needs_fix`
  - `verification_status=failed`
  - `next_round=SKILL-1-to-SKILL-5`

输出格式：

- 验证结论
- 已运行验证
- Stage 完整性检查
- SKILL-1 检查结果
- SKILL-2 检查结果
- SKILL-3 检查结果
- SKILL-4 检查结果
- SKILL-5 检查结果
- API / artifact / window 检查
- Guardrail 检查
- 发现的问题
- 建议返工任务

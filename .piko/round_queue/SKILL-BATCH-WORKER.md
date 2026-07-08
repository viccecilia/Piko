# Piko-worker Task Prompt: SKILL-1 To SKILL-5 Skill Runtime, Content Quality, And Social Distribution

请一次连续执行 SKILL-1 到 SKILL-5，然后停止等待 Piko-verify。

请先读取：

`C:\PycharmProjects\Piko\.piko\round_queue\SKILL-INDEX.md`

执行顺序：

```text
SKILL-1-R01 -> SKILL-1-R02
SKILL-2-R01 -> SKILL-2-R02
SKILL-3-R01 -> SKILL-3-R02
SKILL-4-R01 -> SKILL-4-R02 -> SKILL-4-R03
SKILL-5-R01 -> SKILL-5-R02 -> SKILL-5-R03
```

本批次目标：

- 吸收 2026-07-04 GitHub scan 中最适合 Piko 的能力模式。
- 建立 Piko Skill Runtime v0：manifest、trigger、progressive loading、drill eval、lifecycle。
- 建立 worker trace id 与 verify verdict correlation。
- 建立 promptfoo-style declarative eval queue。
- 建立内容质量引擎：标题钩子、引言、结构、证据、可读性、平台适配。
- 建立社交分发 skill：平台 adapter contract、approval gate、dry-run one-click package。

重点关注：

- 产出物文案质量提升。
- 小红书、公众号、抖音等平台的一键分发准备。
- 一键分发默认必须是 dry-run / package generation，不得真实发布。

全局禁止项：

- 不发布、不上传、不部署。
- 不保存平台账号、token、cookie、API key、authorization。
- 不绕过平台规则。
- 不默认调用 LLM。
- 不使用未授权图片/长文复制。
- 不 vendor 外部源码。
- 不绕过 verification，不放宽 Gate。

必须运行的验证：

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- SKILL 专项测试
- artifacts JSON parse probes
- social distribution dry-run probes
- guardrail scan

最终更新 `.piko/round_status.json`：

```text
current_round=SKILL-1-to-SKILL-5
worker_status=ready_for_verify
verification_status=not_started
last_completed_round=SKILL-5-R03
worker_summary_file=.piko/summaries/worker_SKILL-1-to-SKILL-5.md
next_round=null
```

最终输出格式：

- 修改了什么
- SKILL-1 每个 round 状态
- SKILL-2 每个 round 状态
- SKILL-3 每个 round 状态
- SKILL-4 每个 round 状态
- SKILL-5 每个 round 状态
- 生成的 artifacts
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

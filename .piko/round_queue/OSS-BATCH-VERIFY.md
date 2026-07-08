# Piko-verify Task Prompt: Verify OSS-1 To OSS-5 Open Source Learning Upgrade Batch

请验证 OSS-1 到 OSS-5 总体批次，不要只验单个 round。

验证范围：

```text
OSS-1-R01 -> OSS-1-R02 -> OSS-1-R03
OSS-2-R01 -> OSS-2-R02
OSS-3-R01 -> OSS-3-R02 -> OSS-3-R03
OSS-4-R01 -> OSS-4-R02 -> OSS-4-R03
OSS-5-R01 -> OSS-5-R02
```

必须检查：

- 每个 round summary 存在。
- 每个 stage summary 存在。
- final summary `.piko/summaries/worker_OSS-1-to-OSS-5.md` 存在。
- `round_status.json` 是 UTF-8 no BOM 且合法 JSON。
- OSS research intake artifact 可解析。
- Latest ranked projects artifact 可解析。
- Pattern artifact 可解析。
- Upgrade proposal artifact 可解析。
- Agent framework adapter proposal 可解析。
- Domain plugin proposal 可解析。
- Capability handoff candidates 可解析。
- CAP queue candidates 可解析。
- STORY queue candidates 可解析。

必须运行的验证：

- `python -c "import json; json.load(open('.piko/round_status.json', encoding='utf-8')); print('round_status json ok')"`
- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- 新增 OSS/plugin/domain tests
- artifact JSON parse probes
- CLI/API probes for default domain, `gaming`, demo domain, unknown domain
- guardrail scan

核心验收点：

- OSS-1:
  - Research intake schema 存在。
  - GitHub 5000 星以上扫描规则存在。
  - 无 token/无 opt-in 不伪装真实扫描成功。
  - Relevance scoring 有 score components 和 recommendation。
- OSS-2:
  - Architecture pattern extraction 可用。
  - Upgrade proposals 有 risk、tests_needed、rollback_plan。
  - 没有复制外部源码。
- OSS-3:
  - Mature agent framework adapter proposal 存在。
  - DomainPlugin proposal 存在。
  - Skill replacement/capability handoff proposal 存在。
  - CAP/STORY handoff 明确。
- OSS-4:
  - Domain registry skeleton 存在。
  - 默认 gaming 行为不回归。
  - Domain-aware CLI/API probe 安全。
  - CAP/STORY candidates 不会自动执行。
- OSS-5:
  - Daily loop/operator guide 存在。
  - Final summary 存在。
  - 开源学习闭环不会自动改代码、不会自动发布。

安全禁止项：

- 不得自动安装/vendor 外部 repo。
- 不得复制 license-incompatible code。
- 不得默认联网。
- 不得发布、部署、commit、push。
- 不得默认 LLM。
- 不得绕过 verification 或放宽 Gate。
- 不得破坏 existing gaming discovery behavior。
- 不得自动替换 active skill/capability。

通过时更新：

- 生成 `.piko/summaries/verify_OSS-1-to-OSS-5.md`
- 更新 `.piko/round_status.json`：
  - `worker_status=complete`
  - `verification_status=passed`
  - `last_verified_round=OSS-1-to-OSS-5`
  - `verification_summary_file=.piko/summaries/verify_OSS-1-to-OSS-5.md`
  - `next_round=null`
  - UTF-8 no BOM

失败时更新：

- `worker_status=needs_fix`
- `verification_status=failed`
- `next_round=OSS-1-to-OSS-5`
- 明确返工 round 和阻断原因。

输出格式：

- 验证结论
- 已生成验证报告
- 已运行验证
- Stage 完整性检查
- OSS-1 检查结果
- OSS-2 检查结果
- OSS-3 检查结果
- OSS-4 检查结果
- OSS-5 检查结果
- API / artifact / CLI 检查
- guardrail 检查
- 发现的问题
- 建议返工任务

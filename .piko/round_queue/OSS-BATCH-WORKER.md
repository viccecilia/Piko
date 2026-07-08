# Piko-worker Task Prompt: OSS-1 To OSS-5 Open Source Learning Upgrade Batch

你现在执行 OSS-1 到 OSS-5。目标是建立 Piko 的开源学习闭环：每天吸收 GitHub 上高星成熟项目，提炼可借鉴模式，生成能力图候选和内容候选，但不自动改生产行为。

请先读取：

`C:\PycharmProjects\Piko\.piko\round_queue\OSS-INDEX.md`

然后按顺序执行：

```text
OSS-1-R01 -> OSS-1-R02 -> OSS-1-R03
OSS-2-R01 -> OSS-2-R02
OSS-3-R01 -> OSS-3-R02 -> OSS-3-R03
OSS-4-R01 -> OSS-4-R02 -> OSS-4-R03
OSS-5-R01 -> OSS-5-R02
```

本批目标：

- 建立 OSS research intake schema。
- 建立 GitHub 5000 星以上项目扫描/过滤规则。
- 建立 Piko relevance scoring。
- 提炼 mature agent/skill/workflow/connector/evaluation 项目的架构模式。
- 生成 Piko upgrade proposals。
- 设计 mature agent framework adapter proposal。
- 设计 DomainPlugin / 可插拔领域 proposal。
- 建立 skill replacement/capability handoff 规则。
- 建立 domain registry skeleton 和 domain-aware API/CLI probe。
- 生成 CAP queue candidates。
- 生成 STORY queue candidates。
- 更新 daily open-source learning operator guide。

执行规则：

- 每个 round 必须先读取对应 `OSS-*.md` 文件。
- 每完成一个 round，生成对应 `.piko/summaries/worker_<RoundID>.md`。
- 每完成一个 stage，生成 `.piko/summaries/worker_<StageID>.md`。
- 所有 stage 完成后，生成 `.piko/summaries/worker_OSS-1-to-OSS-5.md`。
- 可以连续执行 OSS-1 到 OSS-5，但不能跳过任何 round。
- 最终停止，等待 Piko-verify。

全局禁止项：

- 不要自动应用第三方代码。
- 不要 vendor 外部 repo。
- 不要复制 GPL/AGPL 或 license-incompatible snippets 到 Piko 源码。
- 不要发送 secrets、credentials、本地私有文件或 proprietary code 到外部服务。
- 不要发布、部署、commit、push。
- 不要默认联网。
- 不要默认调用 LLM。
- 不要绕过 verification 或放宽 Gate。
- 不要自动替换现有 agent/skill/capability。
- 不要自动发布 STORY 内容。

必须运行的验证：

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- 新增 OSS/plugin/domain 测试
- artifact JSON parse probes
- CLI/API probes for default domain, `gaming`, demo domain, unknown domain
- guardrail scan

最终输出格式：

- 修改了什么
- OSS-1 每个 round 状态
- OSS-2 每个 round 状态
- OSS-3 每个 round 状态
- OSS-4 每个 round 状态
- OSS-5 每个 round 状态
- 生成的 artifacts
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

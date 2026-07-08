# Piko-worker Task Prompt: V02-1 To V02-5 Runtime Growth Batch

你现在执行 V02-1 到 V02-5。目标是在 GROW 之后，把 Piko 推进到 v0.2 runtime growth 可演示状态。

请先读取：

`C:\PycharmProjects\Piko\.piko\round_queue\V02-INDEX.md`

然后按顺序执行：

```text
V02-1-R01 -> V02-1-R02
V02-2-R01 -> V02-2-R02 -> V02-2-R03
V02-3-R01 -> V02-3-R02 -> V02-3-R03
V02-4-R01 -> V02-4-R02 -> V02-4-R03
V02-5-R01 -> V02-5-R02
```

本批目标：

- 建立 human approval packet。
- 建立 draft-to-round materializer dry-run。
- 建立最小 DomainPlugin runtime contract。
- 建立 ai_tools demo domain fixture。
- 建立 domain routing surface。
- 建立 AgentRuntimeAdapter contract。
- 建立 local rule-based adapter fixture。
- 建立 framework candidate comparison。
- 建立 declarative eval pack contract。
- 建立 run trace artifact。
- 建立 operator trace window。
- 建立 controlled real pilot readiness。

执行规则：

- 每个 round 必须先读取对应 `V02-*.md` 文件。
- 每完成一个 round，生成对应 `.piko/summaries/worker_<RoundID>.md`。
- 每完成一个 stage，生成 `.piko/summaries/worker_<StageID>.md`。
- 所有 stage 完成后，生成 `.piko/summaries/worker_V02-1-to-V02-5.md`。
- 完成 V02-5-R02 后停止，等待 Piko-verify。

全局禁止项：

- 不要执行 draft tasks，除非有明确 approval artifact；本批默认只做 dry-run。
- 不要自动吸收 OSS candidates。
- 不要自动安装 external dependencies/plugins/connectors/repos/frameworks。
- 不要发布、部署、commit、push。
- 不要默认联网。
- 不要默认调用 LLM。
- 不要替换 active capabilities。
- 不要绕过 verification 或放宽 Gate。
- 不要伪装 live success。

必须运行验证：

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- V02 artifacts JSON parse probes
- Plugin runtime fixture tests
- Adapter contract tests
- Eval/trace artifact tests
- API/window probes if implemented
- Guardrail scan

最终更新 `.piko/round_status.json`：

```text
current_round=V02-1-to-V02-5
worker_status=ready_for_verify
verification_status=not_started
last_completed_round=V02-5-R02
worker_summary_file=.piko/summaries/worker_V02-1-to-V02-5.md
next_round=null
```

最终输出格式：

- 修改了什么
- V02-1 每个 round 状态
- V02-2 每个 round 状态
- V02-3 每个 round 状态
- V02-4 每个 round 状态
- V02-5 每个 round 状态
- 生成的 artifacts
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

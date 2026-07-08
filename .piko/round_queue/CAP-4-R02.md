# Round ID: CAP-4-R02

Round Name: Final Capability Map Verification And Summary

本轮目标:

完成 CAP-0 到 CAP-4 总体验收前准备，确认能力图、替换政策、自动化边界和持续优化闭环都已生成。

本轮任务:
- 执行任务:
  - 检查所有 capability artifacts 是否存在且可解析。
  - 检查 API/window surface 如已实现是否可访问。
  - 写最终 summary `.piko/summaries/worker_CAP-0-to-CAP-4.md`。
  - 更新 `.piko/round_status.json`：
    - `current_round=CAP-0-to-CAP-4`
    - `worker_status=ready_for_verify`
    - `verification_status=not_started`
    - `last_completed_round=CAP-4-R02`
    - `worker_summary_file=.piko/summaries/worker_CAP-0-to-CAP-4.md`
    - `next_round=OSS-1-R01`
    - UTF-8 no BOM
- 测试任务:
  - `python -m pytest tests\test_discovery_search.py -q`
  - `python -m pytest`
  - artifact JSON parse probes
  - guardrail scan
- 协作验收任务:
  - 生成 `.piko/summaries/worker_CAP-4-R02.md`。
  - 生成 `.piko/summaries/worker_CAP-4.md`。
  - 生成 `.piko/summaries/worker_CAP-0-to-CAP-4.md`。

允许修改:

- `packages/*`
- `apps/api/routes/*`
- `apps/web/pages/*`
- `tests/*`
- `docs/*`
- `artifacts/capability_map/*`
- `.piko/summaries/worker_CAP-4-R02.md`
- `.piko/summaries/worker_CAP-4.md`
- `.piko/summaries/worker_CAP-0-to-CAP-4.md`
- `.piko/round_status.json`

禁止修改:

- 不要发布、部署、commit、push。
- 不要默认联网。
- 不要自动安装/替换 capability。
- 不要绕过 verification 或放宽 Gate。

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- artifact JSON parse probes
- guardrail scan

完成定义:

- CAP-0 到 CAP-4 全部完成。
- 每个 round summary、stage summary、final summary 存在。
- 能力图可持续优化，但不会自动越权。
- 下一步可进入 OSS-1-R01。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

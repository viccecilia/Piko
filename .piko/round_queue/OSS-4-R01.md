# Round ID: OSS-4-R01

Round Name: Domain Registry Skeleton

本轮目标:

建立安全的 domain registry skeleton，让未来不同领域可以注册能力，但默认不改变游戏路径。

本轮任务:
- 执行任务:
  - 建立或更新 domain registry skeleton。
  - 默认 domain 必须仍为 gaming。
  - Registry 至少包含 domain_id、status、plugin_path、capabilities、risk_level、enabled_by_default。
  - non-gaming demo domain 必须 `enabled_by_default=false`。
- 测试任务:
  - 测试默认 domain 为 gaming。
  - 测试 unknown domain 安全失败。
  - 测试 demo domain 不触网、不发布。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_OSS-4-R01.md`。

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/oss_research/*`
- `.piko/summaries/worker_OSS-4-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不要默认启用 non-gaming domain。
- 不要破坏现有 discovery/search。

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`
- Domain registry tests。

完成定义:

- 有安全的 domain registry skeleton，且默认行为不变。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

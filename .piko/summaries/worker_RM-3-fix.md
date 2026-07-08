# RM-3 Fix Worker Summary

Fix target: RM-3-R03 Discovery Client Ranking Surface

## 修改了什么

- Updated `/discovery/window` in `apps/api/routes/discovery.py`.
- Added an explicit visible RM-3 ranking section index containing the exact required labels:
  - 游戏类型排行榜
  - 玩家画像/兴趣画像排行榜
  - 必须查攻略的问题排行
  - 已有答案 / 未解决高热问题
  - 冲突答案榜
  - 高风险阻断榜
- Added regression assertions in `tests/test_discovery_search.py` so these labels remain visible.

## 每个任务状态

- RM-3-R03 visible ranking section labels: fixed
- API behavior: unchanged
- Default real-source behavior: unchanged
- RM-4 execution: not entered

## 验证结果

- `python -m pytest tests\test_discovery_search.py -q`: 59 passed
- `python -m pytest`: 139 passed, 3 skipped

## 协作验收结果

- The blocking verifier issue was addressed directly.
- `/discovery/window` now visibly contains all six required RM-3 ranking labels.
- No publish, deploy, crawler, default network collection, default LLM, translation API, Gate relaxation, or verification bypass was introduced.

## 未完成/风险

- None blocking.

## 下一轮建议

- Piko-verify should re-run RM-3 verification.

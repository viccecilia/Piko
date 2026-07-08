# 小红书卡片稿

P1 封面
别急着接入 Agent 框架
先给 Piko 加一道边界

P2 旧痛点
研究框架有两个坑：
只写调研，能力进不了系统；
直接接入，系统规则被绕开。

P3 新能力
AgentRuntimeAdapter boundary
让外部 agent 框架只能通过一个可测接口进入 Piko。

P4 快速判断
值得做，但不能直接替换 pipeline。
它是增强层，不是新主控。

P5 机制卡
五个 contract：
run_task
tool_policy
state_contract
evidence_contract
verification_contract

P6 实操步骤
列框架
抽接口
做离线 fixture
跑 contract tests
交给 CAP 决策

P7 真实限制
proposal only。
风险中等。
重点看 verify 能不能被绕过。

P8 适合谁
适合有 pipeline、有审核、有证据链的团队。
不适合快速 demo 和默认自动发布。

P9 总结
Piko 学 agent 框架，
不是盲目安装，
而是把能力沉淀成边界。


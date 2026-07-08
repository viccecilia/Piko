# 别急着接入 Agent 框架，先给 Piko 加一道适配器边界

今天这个选题，不是介绍某一个新的 AI 框架。

它更像是 Piko 在回答一个更现实的问题：当 LangGraph、OpenAI Agents SDK、LlamaIndex 这类框架都值得学习时，Piko 应该怎么吸收它们，而不是被它们牵着走？

我的判断很直接：不要先接入框架，先定义边界。

这个边界就是 AgentRuntimeAdapter。

## 01 旧痛点：调研和接入之间，缺一层安全缓冲

以前看 agent 框架，很容易有两种结果。

一种是只做调研：写完项目分析、打完分、列出优缺点，但能力没有进入 Piko 的 pipeline。

另一种是直接接入：为了验证一个框架，把运行时、工具调用、状态读写一起放进系统。短期看很快，长期看会破坏 Piko 自己的来源策略、验证流程和发布限制。

Piko 的核心不是“能不能跑 agent”，而是“能不能在可控边界里跑 agent”。

## 02 新能力：AgentRuntimeAdapter boundary

AgentRuntimeAdapter 是一个外部 agent 框架进入 Piko 之前必须通过的接口层。

这个接口只做五件事：run_task、tool_policy、state_contract、evidence_contract、verification_contract。

这样做的好处是，Piko 可以学习框架的能力，但不把控制权交出去。

## 03 快速判断：值得做，但不能直接替换 pipeline

今天的判断是：这个能力值得进入 CAP，但只应该作为增强层。

它不应该马上替换 article_pipeline。

更合理的顺序是：先写 offline fixture，再跑 adapter contract tests，确认新 runtime 不能越权，最后再考虑真实框架接入。

## 04 机制解释：Piko 学的是边界，不是 API

LangGraph 的价值在状态机和 checkpointed workflow。

OpenAI Agents SDK 的价值在 tool policy、agent handoff 和 structured output。

LlamaIndex 的价值在 evidence indexing 和 source-grounded retrieval。

Piko 真正要抽象的是共同边界：任务输入输出、工具权限、状态读写、证据返回、验证材料。

只要边界稳定，底层框架就可以替换；只要边界可测，外部 runtime 就不能越过 Piko 的审核。

## 05 实操步骤

第一步，列候选框架。

第二步，抽共同接口。

第三步，先不接真实 API。

第四步，写 contract tests。

第五步，交给 CAP 决策。结论是 augment，不是 replace。

## 06 真实限制

这个能力现在还是 proposal。

风险主要有三个：adapter 太宽，会变成隐藏运行时；adapter 太窄，看不到真实框架价值；测试只覆盖 happy path，就无法证明 verify 真的不可绕过。

所以它必须先用 offline fixture 和 adapter contract tests 证明边界有效。

## 07 适合谁

它适合已经有内容 pipeline、研究 pipeline、审核 pipeline 的团队。

也适合希望把 agent 框架引入生产系统，但又不想让框架接管系统规则的人。

不适合只做一次性 demo 的团队，也不适合没有 verification 机制的项目。

## 08 总结和行动

今天的结论只有一句：Piko 学 agent 框架，先学边界，再学接入。

接下来最值得做的三件事：

- 做 AgentRuntimeAdapter 的最小离线 fixture。
- 补 adapter contract tests。
- 明确 verify、source policy、publishing disabled 三个不可绕过的闸门。


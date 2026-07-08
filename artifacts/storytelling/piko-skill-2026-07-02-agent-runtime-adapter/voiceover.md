# Voiceover

别急着给 Piko 接入新的 Agent 框架。先加一道适配器边界。

以前研究 LangGraph、OpenAI Agents SDK、LlamaIndex，很容易走偏。

要么只写调研，能力进不了系统。

要么直接接入运行时，把来源策略、审核闸门、发布限制都暴露出去。

今天选的是 AgentRuntimeAdapter boundary。

它只让外部框架做一件事：执行一个边界清楚的任务。

返回结构化结果、证据卡引用、还有验证输入。

机制很简单，五个 contract。

第一，run_task，一次一个任务。

第二，tool_policy，声明工具权限和外部副作用。

第三，state_contract，只读写允许的状态。

第四，evidence_contract，只返回证据引用，不搬运长原文。

第五，verification_contract，必须进入 Piko verify，不能绕过审核。

所以今天的判断是：值得做，但只能先做增强层。

先写 offline fixture，再跑 adapter contract tests。

确认三件事：不默认调用外部 API，不绕过 verify，不自动发布。

Piko 真正要学的，不是某个框架的 API。

而是让所有外部 agent 框架，都必须遵守同一套边界。


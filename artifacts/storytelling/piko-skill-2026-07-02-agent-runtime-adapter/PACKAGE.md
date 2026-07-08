# Piko Skill Short Video Package - 2026-07-02

Topic: AgentRuntimeAdapter boundary
Angle: Piko studies agent frameworks without blindly installing them.
Source artifacts:
- C:\PycharmProjects\Piko\artifacts\oss_research\agent_framework_adapter_proposal.json
- C:\PycharmProjects\Piko\artifacts\oss_research\capability_handoff_candidates.json
- C:\PycharmProjects\Piko\artifacts\oss_research\latest_ranked_projects.json

## 1. Title Candidates

1. 别急着接入 Agent 框架，先给 Piko 加一道适配器边界
2. Piko 今天学到的不是 LangGraph，而是怎么安全学习 Agent 框架
3. 一个 AgentRuntimeAdapter，让新框架进来但不能绕过审核

## 2. Fixed Story Structure

### 强标题

别急着接入 Agent 框架，先给 Piko 加一道适配器边界。

### 旧痛点

以前研究 LangGraph、OpenAI Agents SDK、LlamaIndex 这类框架，很容易走向两个极端：要么只写调研文章，能力进不了系统；要么直接接入运行时，把 Piko 原来的来源策略、审核闸门、发布限制都暴露给新框架。

这对 Piko 不划算。框架越强，越需要边界。

### 新能力

今天选的是 AgentRuntimeAdapter boundary。它把外部 agent 框架包在一个可测试、可审计、可替换的接口后面。

它只允许框架做一件事：执行一个边界清楚的任务，返回结构化结果、证据卡引用和验证输入。

### 快速判断

值得做，但不应该立刻全面替换现有 pipeline。

它适合当作 Piko 的增强层：先接离线 fixture、再做 adapter contract tests、最后才考虑真实运行时。

不适合拿来做默认自动发布，也不适合让任何外部框架绕过 Piko verify。

### 机制解释

这个边界拆成五个小约束。

第一，run_task：一次只执行一个有输入、有输出的任务。
第二，tool_policy：声明允许哪些工具，以及会不会产生外部副作用。
第三，state_contract：只能读写 Piko pipeline 允许的状态字段。
第四，evidence_contract：返回证据卡引用，不把长原文塞回提示词。
第五，verification_contract：必须输出验证材料，不能跳过 Piko 的审核。

换句话说，Piko 学的不是某个框架的 API，而是所有框架进入系统前必须遵守的门禁。

### 实操步骤

1. 先把候选框架放到同一张表里：LangGraph 看状态机，OpenAI Agents SDK 看 handoff 和 structured output，LlamaIndex 看 evidence indexing。
2. 抽出共同能力：任务执行、工具策略、状态读写、证据返回、验证材料。
3. 写一个最小 adapter interface，不接默认 LLM，不默认发 API。
4. 用 offline fixture 跑 contract tests，确认外部 runtime 不能越权读写状态。
5. 把结果交给 CAP，而不是直接替换 article_pipeline。

### 真实限制

这个方案现在只是 proposal，不是已经上线的功能。

风险是中等：adapter 写得太宽，会变成另一个隐藏运行时；写得太窄，又无法测试真实框架价值。

最关键的测试是：verification 不能被绕过，publishing 默认关闭，source policy 仍由 Piko 控制。

### 适合谁

适合正在做 agent 平台、内容自动化、研究到生产闭环的人。

也适合 Piko 这种已经有 pipeline，但想吸收外部 agent 框架能力的项目。

不适合只想快速 demo、马上自动发布、或者不愿意写 contract tests 的团队。

### 总结和行动

今天的结论：Piko 不该盲目接入一个新 agent 框架，而该先定义外部框架进入 Piko 的边界。

三个行动点：
- 先做 AgentRuntimeAdapter 的离线 fixture。
- 再补 adapter contract tests。
- 最后确认 verify、source policy、publishing disabled 三个闸门都不可绕过。

## 3. WeChat Article

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

AgentRuntimeAdapter 不是一个大而全的框架替代品。

它是一个外部 agent 框架进入 Piko 之前必须通过的接口层。

这个接口只做五件事：

1. run_task：一次执行一个边界清楚的任务。
2. tool_policy：声明允许哪些工具和外部副作用。
3. state_contract：只能读写 Piko 允许的状态字段。
4. evidence_contract：返回证据卡引用，不返回大段原文。
5. verification_contract：必须输出验证输入，不能绕过 Piko verify。

这样做的好处是，Piko 可以学习框架的能力，但不把控制权交出去。

## 03 快速判断：值得做，但不能直接替换 pipeline

今天的判断是：这个能力值得进入 CAP，但只应该作为增强层。

它不应该马上替换 article_pipeline。

更合理的顺序是：

先写 offline fixture，再跑 adapter contract tests，确认新 runtime 不能越权，最后再考虑真实框架接入。

尤其要记住三条底线：

- 不默认调用 LLM 或外部 API。
- 不允许绕过 verification。
- 不允许默认自动发布。

## 04 机制解释：Piko 学的是边界，不是 API

LangGraph 的价值在状态机和 checkpointed workflow。

OpenAI Agents SDK 的价值在 tool policy、agent handoff 和 structured output。

LlamaIndex 的价值在 evidence indexing 和 source-grounded retrieval。

这些能力都很有启发，但不能原样塞进 Piko。

Piko 真正要抽象的是共同边界：任务输入输出、工具权限、状态读写、证据返回、验证材料。

只要边界稳定，底层框架就可以替换；只要边界可测，外部 runtime 就不能越过 Piko 的审核。

## 05 实操步骤

第一步，列候选框架。

把 LangGraph、OpenAI Agents SDK、LlamaIndex 放进同一张能力表，分别标注它们擅长什么。

第二步，抽共同接口。

不要照搬框架 API，而是抽出 Piko 需要的五个 contract。

第三步，先不接真实 API。

做一个离线 adapter fixture，用固定输入和固定输出跑通流程。

第四步，写 contract tests。

测试重点不是“能不能跑成功”，而是“能不能阻止越权”。

第五步，交给 CAP 决策。

结论是 augment，不是 replace。它增强现有 pipeline，不替换现有 pipeline。

## 06 真实限制

这个能力现在还是 proposal。

它的风险不低，主要有三个。

第一，adapter 太宽，会变成隐藏运行时。

第二，adapter 太窄，看不到真实框架价值。

第三，如果测试只覆盖 happy path，就无法证明 verify 真的不可绕过。

所以它必须先用 offline fixture 和 adapter contract tests 证明边界有效。

## 07 适合谁

它适合已经有内容 pipeline、研究 pipeline、审核 pipeline 的团队。

也适合希望把 agent 框架引入生产系统，但又不想让框架接管系统规则的人。

不适合只做一次性 demo 的团队，也不适合没有 verification 机制的项目。

## 08 Piko 可借鉴点

Piko 可以把外部 agent 框架当作“可插拔能力源”，而不是“系统主控”。

这会让 Piko 的 OSS 扫描更有用：扫描不是为了追热点，而是为了找到可以被 adapter 吸收的模式。

更重要的是，Piko 可以把每次学习沉淀成 contract，而不是沉淀成一次性的文章。

## 09 总结和行动

今天的结论只有一句：Piko 学 agent 框架，先学边界，再学接入。

接下来最值得做的三件事：

- 做 AgentRuntimeAdapter 的最小离线 fixture。
- 补 adapter contract tests。
- 明确 verify、source policy、publishing disabled 三个不可绕过的闸门。

如果这三点跑通，Piko 才应该进入下一步：让某个真实框架在边界内试运行。

## 4. Xiaohongshu Cards

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

## 5. Voiceover Script

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

## 6. TTS Plan

Voice: Chinese knowledge explainer, neutral young adult, clear diction, slightly fast, no impersonation.
Speed: 1.08x to 1.15x.
Emotion: calm opening, firmer contrast at pain point, rising confidence at mechanism, decisive close.
Pauses:
- Short pause after "先加一道适配器边界".
- Pause before each numbered contract.
- Slight emphasis on "不能绕过审核", "不自动发布", "同一套边界".

Local audio status:
- `npx.cmd hyperframes auth status --json` returned no HeyGen credential.
- Offline voice engine reported Kokoro ready.
- MusicGen was not ready.

Planned files:
- TTS request: C:\PycharmProjects\Piko\artifacts\storytelling\piko-skill-2026-07-02-agent-runtime-adapter\tts\audio_request.json
- Expected voiceover path if generated: C:\PycharmProjects\Piko\artifacts\storytelling\piko-skill-2026-07-02-agent-runtime-adapter\tts\audio_meta.json plus assets\voice outputs.

## 7. Storyboard

0-4s Hook
Visual: Large title card, Piko pipeline line split by a bright adapter gate.
VO: 别急着给 Piko 接入新的 Agent 框架。先加一道适配器边界。
Screen text: 先加边界，再接框架

4-10s Old Pain
Visual: Split screen. Left "只写调研", right "直接接入". Both marked as risky.
VO: 以前研究这些框架，很容易走偏。要么能力进不了系统，要么规则被绕开。
Screen text: 两个坑：空调研 / 乱接入

10-17s New Ability
Visual: AgentRuntimeAdapter card appears between "Frameworks" and "Piko".
VO: 今天选的是 AgentRuntimeAdapter boundary。
Screen text: AgentRuntimeAdapter

17-32s Mechanism
Visual: Five stacked contract cards animate in.
VO: 它有五个 contract：run_task、tool_policy、state_contract、evidence_contract、verification_contract。
Screen text: 五个 contract

32-42s Practical Steps
Visual: Progress rail with five steps.
VO: 先列框架，再抽接口，做离线 fixture，跑 contract tests，最后交给 CAP。
Screen text: 先 fixture，再 tests

42-52s Limits
Visual: Three red gate chips: no default API, no verify bypass, no auto publish.
VO: 重点确认三件事：不默认调用外部 API，不绕过 verify，不自动发布。
Screen text: 三个不可绕过

52-60s Close
Visual: Piko gate closes, frameworks remain outside but connected by adapter.
VO: Piko 真正要学的，不是某个框架 API，而是同一套边界。
Screen text: 学边界，不是追热点

## 8. Screen Text

- 先加边界，再接框架
- 两个坑：空调研 / 乱接入
- AgentRuntimeAdapter
- 五个 contract
- run_task
- tool_policy
- state_contract
- evidence_contract
- verification_contract
- 先 fixture，再 tests
- 不默认 API
- 不绕过 verify
- 不自动发布
- 学边界，不是追热点

## 9. HyperFrames Draft

Draft HTML:
C:\PycharmProjects\Piko\artifacts\storytelling\piko-skill-2026-07-02-agent-runtime-adapter\video_draft\index.html

Preview command:
```powershell
cd C:\PycharmProjects\Piko\artifacts\storytelling\piko-skill-2026-07-02-agent-runtime-adapter\video_draft
npx.cmd hyperframes preview
```

Validation commands:
```powershell
cd C:\PycharmProjects\Piko\artifacts\storytelling\piko-skill-2026-07-02-agent-runtime-adapter\video_draft
npx.cmd hyperframes lint --json
npx.cmd hyperframes validate --json
npx.cmd hyperframes inspect --json
```

Render command after review:
```powershell
cd C:\PycharmProjects\Piko\artifacts\storytelling\piko-skill-2026-07-02-agent-runtime-adapter\video_draft
npx.cmd hyperframes render --quality draft --output agent-runtime-adapter-draft.mp4
```

## 10. Material And Screenshot Needs

- No external copyrighted images.
- Use original vector cards in the HTML draft.
- Optional owned screenshots:
  - latest_ranked_projects.json showing LangGraph, OpenAI Agents SDK, LlamaIndex.
  - agent_framework_adapter_proposal.json showing the five contract fields.
  - capability_handoff_candidates.json showing augment decision and verification needs.
- Optional terminal screenshot after lint/validate passes.

## 11. Why Today

Today's latest queue selected `story_agent_framework_adapter` and `cap_agent_runtime_adapter_boundary`.

The source handoff explicitly says the content angle is: how Piko studies agent frameworks without blindly installing them.

This is valuable because the ranked OSS candidates are all agent-related, but the safest Piko move is to define the adapter boundary before adopting any one framework.

## 12. What Piko Can Borrow

- Treat external frameworks as replaceable engines, not system owners.
- Convert OSS learning into contracts and tests.
- Keep source policy, gates, verification, and publishing controls inside Piko.
- Use evidence-card references instead of moving raw source bodies through prompts.
- Mark the CAP decision as augment first, replace only after proof.

## 13. Risks And Not-Fit Cases

Risks:
- Medium integration risk.
- Adapter can become too broad and hide uncontrolled runtime behavior.
- Tests may miss permission escalation if they only cover success paths.
- Real framework behavior may differ from offline fixture.

Not fit:
- One-off demos.
- Workflows that require immediate default API calls.
- Systems without verification gates.
- Teams that want automatic publishing by default.


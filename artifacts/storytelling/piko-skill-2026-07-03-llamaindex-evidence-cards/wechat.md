# 别急着让 Agent 会跑，先让证据能被找到

很多人做 Agent，第一反应是接框架、接工具、接自动执行。

但 Piko 每天的短视频素材包提醒我们：真正危险的地方，不是 Agent 不够主动，而是它说完以后，我们不知道它依据什么。

如果一个系统今天扫描 OSS，明天写公众号，后天生成短视频脚本，它必须能回答三个问题：

这条判断来自哪个 artifact？  
这个项目为什么被选中？  
风险提示有没有证据支撑？

所以今天的选题不是“如何使用 LlamaIndex 做 RAG”，而是 Piko 可以向 LlamaIndex 学一个更底层的能力：retriever abstraction + document metadata。

## 01 它解决的不是搜索问题，而是证据问题

传统做法很像把资料一次性丢给模型。

模型能总结，但复查很麻烦。尤其当资料来自 GitHub、OSS 扫描、capability map、人工判断时，原始材料和最终结论之间很容易断开。

更稳的做法，是先把资料登记成证据单元。

每个证据单元至少包含：来源、时间、项目、结论摘要、风险、可引用 ID。

这样 Agent 写内容时，引用的不是一大段原文，而是一个可复查的证据卡片。

## 02 Piko 该学什么

Piko 不需要立刻把完整 LlamaIndex 接进来。

更值得学的是接口思想：

第一，资料进入系统时必须带 metadata。  
第二，Agent 输出判断时必须带 evidence card reference。  
第三，验证环节可以顺着 reference 回看来源。

这会让 Piko 的每日内容链路更像一个可审计流水线，而不是一台只会生成文案的机器。

## 03 实操可以从离线 fixture 开始

最小可行步骤很简单。

先读取 `latest_patterns.json`，把里面的每个 pattern 变成一张证据卡片。

比如：

- `llamaindex_retriever_abstraction`
- 来源项目：LlamaIndex
- Piko 映射：source indexing and evidence-card traceability
- 风险：不要把长原文直接送进 prompt

然后要求 storytelling skill 只基于这些卡片写作。

这样，内容生成和证据来源之间就有了稳定连接。

## 04 真实限制

证据卡片不是魔法。

如果源 artifact 是 fixture，就不能说成真实线上结论。  
如果 metadata 不完整，就不能做过强判断。  
如果 Agent 可以绕过 verification，证据链也会失效。

所以它更像一个纪律：让每个判断在进入内容前，都先拥有来源、边界和风险。

## 05 对 Piko 的价值

Piko 的目标不是每天多写一篇，而是每天写得更可复查。

今天选 LlamaIndex，不是因为它是热门 RAG 框架，而是因为它提醒我们：Agent 系统的核心能力之一，是把材料变成可检索、可引用、可验证的证据。

下一步，Piko 可以先做一个离线 evidence-card 生成器，把 OSS research 里的 pattern、risk、piko_relevance 统一成卡片，再让短视频素材包沿着卡片生成。

# 口播文案

别急着让 Agent 会跑，先让证据能被找到。

很多 Agent 项目卡住，不是模型不会写，而是证据链太乱。

今天看一个 OSS pattern：LlamaIndex 的 retriever abstraction，和 document metadata。

Piko 真正该学的，不是立刻接一个 RAG 框架。

而是把资料先变成证据卡片。

每张卡片记录来源、时间、项目、判断、风险。

然后 Agent 写内容时，不搬运长原文，只引用卡片 ID 和摘要。

这样公众号、短视频、能力判断，都能回到同一条证据链。

第一步，把 latest_patterns.json 拆成 evidence cards。

第二步，让 storytelling skill 只基于卡片生成内容。

第三步，在 verification 里检查：有没有未引用来源的强结论。

限制也很清楚。

如果来源是 fixture，就不能说成真实线上趋势。

如果 metadata 太乱，Agent 也会用不稳。

所以今天的结论是：Piko 不是要更会 RAG，而是要让每个判断都可追溯。

下一步，先做离线证据卡片，再谈框架接入。

# Piko 每日 Skill 短视频素材包

日期：2026-07-03  
主题：LlamaIndex 的 retriever abstraction + document metadata，对 Piko 证据卡片链路的启发  
来源：`artifacts/oss_research/latest_patterns.json`、`artifacts/oss_research/latest_ranked_projects.json`  
状态：素材草稿，不发布，不上传，不使用外部版权图片

## 1. 标题候选

1. 别急着让 Agent 会跑，先让证据能被找到
2. Piko 可以学 LlamaIndex 的，不是 RAG，而是证据索引
3. 一个好 Agent，先要有可追溯的证据卡片

## 2. 强标题

别急着让 Agent 会跑，先让证据能被找到。

## 3. 旧痛点

很多 Agent 项目卡住，不是因为模型不会写，而是因为证据链太乱。

今天扫描一个开源项目，明天写一篇能力分析，后天再追问“这句话来自哪里”。如果原始材料、摘要、判断、截图、风险提示没有稳定索引，最后就会变成一堆散落的 Markdown 和 JSON。

对 Piko 来说，这个问题更明显：它不是只要生成内容，而是要把“为什么选它”“Piko 可借鉴点”“风险和不适合点”都留在可验证链路里。

## 4. 新能力

今天选的不是一个要马上接入的功能，而是一个值得 Piko 学习的能力模式：LlamaIndex 里的 retriever abstraction 和 document metadata。

简单说，就是把资料先变成可检索、可标注、可追溯的证据单元，再交给 Agent 生成判断。

Piko 可以借这个思路，把 OSS 扫描结果、capability map、storytelling 素材包之间的关系，整理成“证据卡片”链路。

## 5. 快速判断

值得学，但不建议盲目接入完整框架。

适合 Piko 学的是三件事：第一，资料进入系统时要带 metadata；第二，Agent 引用资料时要返回证据卡片 ID，而不是大段原文；第三，内容生成前后都能追溯到来源。

不适合现在做的是：直接把所有文档塞进 RAG，再让 Agent 自由总结。那会让 prompt 变重，也会增加版权、隐私和误引风险。

## 6. 机制解释

旧流程像“把所有资料丢给一个聪明人读”。问题是，聪明人读完以后，别人很难复查他到底看了哪一段。

新的机制更像一个资料馆：

1. 每份资料先登记：来源、时间、项目、许可证、风险标签。
2. 系统把资料拆成证据卡片：每张卡只承载一个结论或一组事实。
3. Agent 生成内容时，只引用卡片 ID 和简短摘要。
4. 验证环节再根据卡片回看来源，判断结论是否站得住。

这就是 LlamaIndex 给 Piko 的启发：不要把“检索”理解成搜索框，要理解成一个可审计的证据接口。

## 7. 实操步骤

1. 先给每个 artifact 加统一 metadata：生成时间、来源路径、候选类型、Piko relevance、风险。
2. 把 OSS 扫描结果转成 evidence cards：一张卡只放一个 pattern，例如 `llamaindex_retriever_abstraction`。
3. Storytelling skill 只接收卡片摘要和卡片 ID，避免搬运长原文。
4. 生成素材包时，在“今日为什么选它”和“风险”里显式引用证据卡片。
5. 最后跑 verification：检查是否有未引用来源的强结论、是否误称已接入、是否出现自动发布。

## 8. 真实限制

这不是“装上 LlamaIndex，Piko 就自动变强”。

限制一：证据卡片的质量取决于前置扫描，如果扫描结果是 fixture 或字段不完整，结论必须降级表达。

限制二：metadata 不是越多越好。字段太多，Agent 会更难稳定使用；字段太少，又无法复查。

限制三：不要把长原文直接塞进 prompt。Piko 更需要的是可引用的证据摘要，而不是一个无限膨胀的上下文窗口。

## 9. 适合谁

适合正在做内容自动化、OSS 研究、Agent 工作流验证的人。

尤其适合 Piko 这类系统：每天都要从扫描、判断、写作、视频脚本一路走到素材包，但不能让结论失去来源。

不适合只想做一次性 demo 的人。证据卡片链路的价值，通常要在多次复用、复查和迭代后才显现。

## 10. 总结和行动

一句话：Piko 今天最该学的不是“更会 RAG”，而是“让每个判断都能回到证据卡片”。

三个 takeaway：

- 它改变的是证据流，不只是检索方式。
- 人仍然要决定哪些 metadata 真正重要。
- 下一步应先做离线 evidence-card fixture，再考虑框架接入。

行动点：先为 `artifacts/oss_research/latest_patterns.json` 里的每个 pattern 生成证据卡片，再让 storytelling 只基于卡片写作。

## 11. 公众号图文稿

### 别急着让 Agent 会跑，先让证据能被找到

很多人做 Agent，第一反应是接框架、接工具、接自动执行。

但 Piko 每天的短视频素材包提醒我们：真正危险的地方，不是 Agent 不够主动，而是它说完以后，我们不知道它依据什么。

如果一个系统今天扫描 OSS，明天写公众号，后天生成短视频脚本，它必须能回答三个问题：

这条判断来自哪个 artifact？  
这个项目为什么被选中？  
风险提示有没有证据支撑？

所以今天的选题不是“如何使用 LlamaIndex 做 RAG”，而是 Piko 可以向 LlamaIndex 学一个更底层的能力：retriever abstraction + document metadata。

### 01 它解决的不是搜索问题，而是证据问题

传统做法很像把资料一次性丢给模型。

模型能总结，但复查很麻烦。尤其当资料来自 GitHub、OSS 扫描、capability map、人工判断时，原始材料和最终结论之间很容易断开。

更稳的做法，是先把资料登记成证据单元。

每个证据单元至少包含：来源、时间、项目、结论摘要、风险、可引用 ID。

这样 Agent 写内容时，引用的不是一大段原文，而是一个可复查的证据卡片。

### 02 Piko 该学什么

Piko 不需要立刻把完整 LlamaIndex 接进来。

更值得学的是接口思想：

第一，资料进入系统时必须带 metadata。  
第二，Agent 输出判断时必须带 evidence card reference。  
第三，验证环节可以顺着 reference 回看来源。

这会让 Piko 的每日内容链路更像一个可审计流水线，而不是一台只会生成文案的机器。

### 03 实操可以从离线 fixture 开始

最小可行步骤很简单。

先读取 `latest_patterns.json`，把里面的每个 pattern 变成一张证据卡片。

比如：

- `llamaindex_retriever_abstraction`
- 来源项目：LlamaIndex
- Piko 映射：source indexing and evidence-card traceability
- 风险：不要把长原文直接送进 prompt

然后要求 storytelling skill 只基于这些卡片写作。

这样，内容生成和证据来源之间就有了稳定连接。

### 04 真实限制

证据卡片不是魔法。

如果源 artifact 是 fixture，就不能说成真实线上结论。  
如果 metadata 不完整，就不能做过强判断。  
如果 Agent 可以绕过 verification，证据链也会失效。

所以它更像一个纪律：让每个判断在进入内容前，都先拥有来源、边界和风险。

### 05 对 Piko 的价值

Piko 的目标不是每天多写一篇，而是每天写得更可复查。

今天选 LlamaIndex，不是因为它是热门 RAG 框架，而是因为它提醒我们：Agent 系统的核心能力之一，是把材料变成可检索、可引用、可验证的证据。

下一步，Piko 可以先做一个离线 evidence-card 生成器，把 OSS research 里的 pattern、risk、piko_relevance 统一成卡片，再让短视频素材包沿着卡片生成。

## 12. 小红书卡片稿

P1 封面  
别急着让 Agent 会跑  
先让证据能被找到

P2 旧痛点  
Agent 写得很快  
但结论来自哪里？很难复查

P3 新能力  
LlamaIndex 给 Piko 的启发：  
资料先变证据卡片，再交给 Agent

P4 快速判断  
值得学接口思想  
不建议盲目接完整框架

P5 机制  
metadata 记录来源  
retriever 找到证据  
Agent 只引用卡片 ID

P6 实操  
把 `latest_patterns.json`  
拆成 evidence cards

P7 限制  
fixture 不能当真实结论  
长原文不要直接塞进 prompt

P8 适合谁  
做 OSS 研究、内容自动化、Agent 验证的人

P9 总结  
Piko 下一步：  
让每个判断都能回到证据卡片

## 13. 口播文案

别急着让 Agent 会跑，先让证据能被找到。

很多 Agent 项目卡住，不是模型不会写，而是证据链太乱。

今天看一个 OSS pattern：LlamaIndex 的 retriever abstraction，和 document metadata。

Piko 真正该学的，不是立刻接一个 RAG 框架。

而是把资料先变成证据卡片。

每张卡片记录来源、时间、项目、判断、风险。

然后 Agent 写内容时，不搬运长原文，只引用卡片 ID 和摘要。

这样公众号、短视频、能力判断，都能回到同一条证据链。

第一步，把 `latest_patterns.json` 拆成 evidence cards。

第二步，让 storytelling skill 只基于卡片生成内容。

第三步，在 verification 里检查：有没有未引用来源的强结论。

限制也很清楚。

如果来源是 fixture，就不能说成真实线上趋势。

如果 metadata 太乱，Agent 也会用不稳。

所以今天的结论是：Piko 不是要更会 RAG，而是要让每个判断都可追溯。

下一步，先做离线证据卡片，再谈框架接入。

## 14. 自动配音方案

声线：中文知识类清晰讲解声线，不克隆、不模仿任何真人。  
建议 TTS：`zh-CN-YunxiNeural` 或同类年轻清晰男声；也可换成 `zh-CN-XiaoxiaoNeural` 保持更温和。  
语速：`+12%`，略快但不抢字。  
音高：`+0Hz`。  
情绪：前 5 秒有压力感，中段理性解释，结尾有推进感。  
停顿：在“不是立刻接一个 RAG 框架”“而是把资料先变成证据卡片”“限制也很清楚”后加明显停顿。  
计划音频路径：`artifacts/storytelling/piko-skill-2026-07-03-llamaindex-evidence-cards/audio/voiceover.mp3`

## 15. 分镜脚本

| 时间 | 画面 | 口播 | 动效 |
| --- | --- | --- | --- |
| 0-4s | 黑白对比大字：Agent 会跑 vs 证据能找 | 别急着让 Agent 会跑，先让证据能被找到。 | 标题快速推入 |
| 4-10s | 散乱文件卡片：JSON、Markdown、截图 | 很多 Agent 项目卡住，不是模型不会写，而是证据链太乱。 | 卡片轻微抖动后收束 |
| 10-18s | LlamaIndex pattern 卡片出现 | 今天看一个 OSS pattern：retriever abstraction 和 document metadata。 | 卡片从底部上浮 |
| 18-28s | 三步机制：metadata、evidence card、reference | Piko 真正该学的，不是立刻接框架，而是资料先变成证据卡片。 | 三张卡依次点亮 |
| 28-40s | 流程线：artifact -> evidence cards -> storytelling -> verification | Agent 写内容时，只引用卡片 ID 和摘要。 | 进度线横向推进 |
| 40-50s | 实操 checklist | 第一步拆 pattern，第二步基于卡片写作，第三步验证强结论。 | 勾选动效 |
| 50-58s | 风险卡：fixture、metadata、long prompt | 如果来源是 fixture，就不能说成真实线上趋势。 | 风险标签闪现 |
| 58-64s | 总结卡 | Piko 不是要更会 RAG，而是要让每个判断都可追溯。 | 结论定格 |

## 16. 屏幕文字

- 先让证据能被找到
- 痛点：结论很快，来源很散
- 新能力：证据卡片链路
- 学 LlamaIndex 的接口思想
- metadata：来源、时间、风险
- Agent 只引用卡片 ID
- 不搬运长原文
- verification 检查强结论
- 先做离线 fixture
- 每个判断都可追溯

## 17. HyperFrames HTML 草稿

草稿路径：`artifacts/storytelling/piko-skill-2026-07-03-llamaindex-evidence-cards/video_draft/index.html`

可直接浏览器打开预览。若本地 HyperFrames CLI 可用，可在项目根目录尝试：

```powershell
npx hyperframes preview artifacts/storytelling/piko-skill-2026-07-03-llamaindex-evidence-cards/video_draft/index.html
npx hyperframes render artifacts/storytelling/piko-skill-2026-07-03-llamaindex-evidence-cards/video_draft/index.html --out artifacts/storytelling/piko-skill-2026-07-03-llamaindex-evidence-cards/video_draft/render.mp4
```

## 18. 素材/截图需求

- 本地截图 1：`artifacts/oss_research/latest_patterns.json` 中 LlamaIndex 两个 pattern 的片段。
- 本地截图 2：生成后的 evidence card 示例 JSON。
- 本地截图 3：storytelling 输出中“今日为什么选它”和“风险”的引用关系。
- 图形素材：全部用原创 UI 卡片、流程线、标签，不使用外部版权图片。

## 19. 今日为什么选它

昨天已经覆盖了 agent runtime adapter boundary。今天继续讲同一批 OSS 扫描结果，但换成未覆盖的证据链角度：LlamaIndex 的 retriever abstraction 和 document metadata。

它对 Piko 有价值，因为 Piko 的内容生产不是单次生成，而是长期积累的证据、判断、文案和视频素材链路。证据卡片可以减少重复解释、降低误引风险，并让 verification 更具体。

## 20. Piko 可借鉴点

- 建立 `evidence_card_id`，让每条内容判断可追溯。
- 对 artifact 做统一 metadata，包含来源、时间、项目、风险、Piko relevance。
- Storytelling skill 输入只拿摘要和引用，不拿长原文。
- Verification 检查“强结论是否有证据卡片支持”。
- 先离线 fixture 验证，不默认触发外部 API 或发布动作。

## 21. 风险和不适合点

- 不适合把 LlamaIndex 直接当作必选依赖；当前更适合学习模式。
- 不适合把长原文批量塞入 prompt，可能带来版权、隐私和上下文污染。
- 如果 source artifact 是 fixture，所有结论都要标记为扫描样例或内部证据。
- metadata 设计过度会增加维护成本，设计不足会失去可追溯性。
- Agent 不能绕过 Piko verification，否则证据卡片只是形式。

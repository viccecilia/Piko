# 小红书卡片稿

## P1 封面
别急着让 Agent 会跑  
先让证据能被找到

## P2 旧痛点
Agent 写得很快  
但结论来自哪里？很难复查

## P3 新能力
LlamaIndex 给 Piko 的启发：  
资料先变证据卡片，再交给 Agent

## P4 快速判断
值得学接口思想  
不建议盲目接完整框架

## P5 机制
metadata 记录来源  
retriever 找到证据  
Agent 只引用卡片 ID

## P6 实操
把 `latest_patterns.json`  
拆成 evidence cards

## P7 限制
fixture 不能当真实结论  
长原文不要直接塞进 prompt

## P8 适合谁
做 OSS 研究、内容自动化、Agent 验证的人

## P9 总结
Piko 下一步：  
让每个判断都能回到证据卡片

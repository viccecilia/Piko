# Round ID: SOURCE-PROVIDER-2-R02

Round Name: Static Endpoint Package

本轮目标:

生成可部署的静态 endpoint package，包含 JSON 文件、README、校验命令和部署选项。

本轮任务:
- 执行任务:
  - 生成 static endpoint package artifact。
  - 输出路径例如 `artifacts/source_provider/static_endpoint_package/approved-market.json`。
  - README 包含 GitHub Raw/Gist/Cloudflare Pages/Vercel/Netlify 操作说明。
- 测试任务:
  - 测试 package 文件存在且 JSON contract valid。
  - 测试 README 不包含真实凭据。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_SOURCE-PROVIDER-2-R02.md`。

允许修改:

- `docs/*`
- `tests/*`
- `artifacts/source_provider/*`
- `.piko/summaries/worker_SOURCE-PROVIDER-2-R02.md`
- `.piko/round_status.json`

禁止修改:

- 不实际上传远程。

必须运行的验证:

- Static package tests

完成定义:

- operator 可以拿这个包去创建外部 URL。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

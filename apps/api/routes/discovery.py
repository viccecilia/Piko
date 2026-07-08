from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

from packages.discovery.real_source import (
    DiscoveryRealSourceConfigurationError,
    DiscoveryRealSourceDisabledError,
    DiscoveryRealSourceFetchError,
    RealMarketDiscoverySource,
)
from packages.discovery.funnel_trace import discovery_funnel_trace
from packages.discovery.rankings import hot_strategy_rankings
from packages.discovery.rev_pipeline import (
    approved_live_source_registry,
    build_latest_real_market_funnel_report,
    endpoint_fed_rankings,
    operator_result_surface,
    run_real_search_endpoint_adapter,
    source_hints_and_evidence_readiness,
    write_latest_real_market_funnel_report,
    write_publish_readiness_metadata,
    write_source_backed_article_package,
)
from packages.discovery.search_engine import discovery_retrospective_report, search_player_needs
from packages.oss_learning.domain_registry import domain_probe
from packages.shared.schemas import DiscoverySearchRequest


router = APIRouter()


@router.post("/search")
def search_discovery(request: DiscoverySearchRequest) -> dict[str, object]:
    return search_player_needs(request).model_dump(mode="json")


@router.post("/report")
def discovery_report(request: DiscoverySearchRequest) -> dict[str, object]:
    result = search_player_needs(request)
    return discovery_retrospective_report(result.clusters).model_dump(mode="json")


@router.get("/rankings")
def discovery_rankings(limit: int = 5) -> dict[str, object]:
    return hot_strategy_rankings(limit=limit)


@router.get("/domain-probe")
def discovery_domain_probe(domain: str | None = None) -> dict[str, object]:
    return domain_probe(domain)


@router.get("/endpoint-registry")
def endpoint_registry() -> dict[str, object]:
    return approved_live_source_registry()


@router.get("/endpoint-search")
def endpoint_search(mode: str = "fixture", limit: int = 20) -> dict[str, object]:
    return run_real_search_endpoint_adapter(mode=mode, limit=limit)


@router.get("/endpoint-rankings")
def endpoint_rankings(mode: str = "mock-live", limit: int = 5) -> dict[str, object]:
    return endpoint_fed_rankings(mode=mode, limit=limit)


@router.get("/funnel-trace")
def funnel_trace_get() -> dict[str, object]:
    return discovery_funnel_trace(DiscoverySearchRequest(min_game_heat=50, limit=20))


@router.post("/funnel-trace")
def funnel_trace(request: DiscoverySearchRequest) -> dict[str, object]:
    return discovery_funnel_trace(request)


@router.get("/funnel-report")
def funnel_report() -> dict[str, object]:
    write_latest_real_market_funnel_report()
    return build_latest_real_market_funnel_report()


@router.get("/source-hints")
def source_hints() -> dict[str, object]:
    return source_hints_and_evidence_readiness()


@router.get("/article-package")
def article_package() -> dict[str, object]:
    json_path, md_path = write_source_backed_article_package()
    return {
        "status": "completed",
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "publish_ready": False,
        "publishing_performed": False,
    }


@router.get("/publish-readiness")
def publish_readiness() -> dict[str, object]:
    path = write_publish_readiness_metadata()
    return {
        "status": "completed",
        "artifact_path": str(path),
        "publish_ready": False,
        "publishing_performed": False,
    }


@router.get("/operator-result")
def operator_result() -> dict[str, object]:
    return operator_result_surface()


@router.get("/funnel-window", response_class=HTMLResponse)
def funnel_window() -> str:
    return """
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Piko 漏斗透明窗口</title>
    <style>
      :root {
        --bg: #f5f7fb;
        --panel: #ffffff;
        --line: #d8dee8;
        --text: #101828;
        --muted: #5b6472;
        --accent: #0f766e;
        --blue: #1d4ed8;
        --warn: #b45309;
        --danger: #b91c1c;
      }
      * { box-sizing: border-box; }
      body {
        margin: 0;
        background: var(--bg);
        color: var(--text);
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      }
      header {
        background: var(--panel);
        border-bottom: 1px solid var(--line);
        padding: 18px 24px;
      }
      nav {
        display: flex;
        gap: 12px;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 12px;
      }
      nav a {
        color: var(--accent);
        font-weight: 800;
        text-decoration: none;
      }
      h1 {
        margin: 0;
        font-size: clamp(28px, 5vw, 44px);
        line-height: 1.08;
        letter-spacing: 0;
      }
      .subhead {
        max-width: 960px;
        margin-top: 8px;
        color: var(--muted);
        line-height: 1.55;
      }
      main {
        display: grid;
        grid-template-columns: 330px minmax(0, 1fr);
        gap: 0;
        min-height: calc(100vh - 140px);
      }
      aside {
        background: var(--panel);
        border-right: 1px solid var(--line);
        padding: 18px;
      }
      section {
        padding: 18px 22px 40px;
      }
      label {
        display: block;
        margin: 14px 0 6px;
        color: var(--muted);
        font-size: 12px;
        font-weight: 800;
      }
      input, select {
        width: 100%;
        min-height: 38px;
        border: 1px solid var(--line);
        border-radius: 6px;
        padding: 8px 10px;
        font-size: 14px;
        background: white;
      }
      button {
        width: 100%;
        min-height: 40px;
        margin-top: 16px;
        border: 0;
        border-radius: 6px;
        background: var(--accent);
        color: white;
        font-weight: 900;
        cursor: pointer;
      }
      button:disabled { opacity: 0.6; cursor: wait; }
      .safety, .panel, .step, .metric, .cluster {
        border: 1px solid var(--line);
        border-radius: 8px;
        background: var(--panel);
      }
      .safety {
        margin-top: 16px;
        padding: 12px;
        color: var(--muted);
        font-size: 13px;
        line-height: 1.55;
      }
      .metrics {
        display: grid;
        grid-template-columns: repeat(5, minmax(120px, 1fr));
        gap: 10px;
        margin-bottom: 14px;
      }
      .metric { padding: 12px; }
      .metric span {
        color: var(--muted);
        font-size: 12px;
        font-weight: 800;
      }
      .metric strong {
        display: block;
        margin-top: 5px;
        font-size: 26px;
      }
      .flow {
        display: grid;
        grid-template-columns: repeat(6, minmax(120px, 1fr));
        gap: 8px;
        margin-bottom: 14px;
      }
      .flow div {
        border: 1px solid var(--line);
        border-radius: 8px;
        background: white;
        padding: 10px;
        font-size: 13px;
        font-weight: 900;
        text-align: center;
      }
      .step {
        margin-bottom: 12px;
        overflow: hidden;
      }
      .step summary {
        cursor: pointer;
        padding: 14px;
        font-weight: 900;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
      }
      .step-body {
        border-top: 1px solid var(--line);
        padding: 14px;
      }
      .grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 12px;
      }
      .panel { padding: 12px; min-width: 0; }
      h2, h3 { margin: 0 0 10px; letter-spacing: 0; }
      h2 { font-size: 18px; }
      h3 { font-size: 15px; }
      pre {
        max-height: 320px;
        overflow: auto;
        margin: 0;
        border-radius: 6px;
        background: #0f172a;
        color: #e5e7eb;
        padding: 12px;
        font-size: 12px;
        line-height: 1.5;
      }
      .clusters {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 10px;
      }
      .cluster { padding: 12px; }
      .cluster h3 { line-height: 1.35; }
      .muted { color: var(--muted); }
      .chips {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        margin-top: 8px;
      }
      .chip {
        border: 1px solid var(--line);
        border-radius: 999px;
        padding: 3px 8px;
        color: var(--muted);
        font-size: 12px;
        background: #fff;
      }
      .publish_candidate { color: #166534; }
      .watchlist_waiting_for_answer { color: var(--warn); }
      .conflict_explainer { color: var(--blue); }
      .blocked_high_risk { color: var(--danger); }
      .status {
        margin-bottom: 12px;
        color: var(--muted);
        font-size: 13px;
      }
      .error {
        border: 1px solid #fecaca;
        border-radius: 8px;
        background: #fef2f2;
        color: var(--danger);
        padding: 12px;
      }
      @media (max-width: 1050px) {
        main, .grid, .clusters { grid-template-columns: 1fr; }
        aside { border-right: 0; border-bottom: 1px solid var(--line); }
        .metrics { grid-template-columns: repeat(2, minmax(120px, 1fr)); }
        .flow { grid-template-columns: repeat(2, minmax(120px, 1fr)); }
      }
    </style>
  </head>
  <body>
    <header>
      <nav>
        <a href="/discovery/window">返回 Discovery Window</a>
        <a href="/console">控制台</a>
      </nav>
      <h1>Piko 漏斗透明窗口</h1>
      <div class="subhead">
        这里展示 Piko 从“大范围市场信号”到“可写攻略候选”的每一步动作：搜索哪些平台、读取到什么信号、如何聚类、如何评分、为什么进入写作/监控/冲突解释/高风险阻断。默认只使用本地 fixture/批准镜像数据，不会自动触网或发布。
      </div>
    </header>
    <main>
      <aside>
        <label for="query">搜索关键词</label>
        <input id="query" placeholder="例如 save location, crash, Steam Deck" />

        <label for="minGameHeat">最低游戏热度</label>
        <input id="minGameHeat" type="number" min="0" max="100" value="50" />

        <label for="limit">最多展示 topic</label>
        <input id="limit" type="number" min="1" max="100" value="20" />

        <button id="runButton" type="button">运行漏斗分析</button>

        <div class="safety">
          <strong>安全边界</strong><br />
          默认不触网、不 crawler、不抓全文、不保存 raw body、不发布、不部署。这个窗口展示的是 discovery 决策轨迹，不是发布许可。
        </div>
      </aside>
      <section>
        <div id="status" class="status">准备运行。</div>
        <div class="flow">
          <div>1 来源扫描</div>
          <div>2 信号读取</div>
          <div>3 聚类去重</div>
          <div>4 评分判断</div>
          <div>5 漏斗分流</div>
          <div>6 解决路径</div>
        </div>
        <div id="metrics" class="metrics"></div>
        <div id="steps"></div>
      </section>
    </main>
    <script>
      const decisionLabels = {
        publish_candidate: "可写攻略候选",
        watchlist_waiting_for_answer: "高热未解决，进入监控",
        conflict_explainer: "答案冲突，适合解释",
        blocked_high_risk: "高风险阻断",
        ignore: "暂不处理"
      };

      const englishAliasKeys = new Set([
        "platforms",
        "real_collection_performed",
        "mode",
        "raw_game_count",
        "raw_question_count",
        "source_type_counts",
        "source_region_counts",
        "sample_games",
        "sample_questions",
        "cluster_count",
        "clusters",
        "decision_counts",
        "top_by_decision",
        "publish_candidates",
        "watchlist",
        "conflict_explainers",
        "high_risk_blocked",
        "planned_agent_path",
        "handoff_requirements"
      ]);

      function cleanForDisplay(value) {
        if (Array.isArray(value)) return value.map(cleanForDisplay);
        if (!value || typeof value !== "object") return value;
        const output = {};
        for (const [key, item] of Object.entries(value)) {
          if (englishAliasKeys.has(key)) continue;
          output[key] = cleanForDisplay(item);
        }
        return output;
      }

      function asJson(value) {
        return JSON.stringify(cleanForDisplay(value), null, 2);
      }

      function metric(label, value) {
        return `<div class="metric"><span>${label}</span><strong>${value}</strong></div>`;
      }

      function chip(text, extraClass = "") {
        return `<span class="chip ${extraClass}">${text}</span>`;
      }

      function clusterCard(cluster) {
        const decision = cluster.decision || "unknown";
        const labels = [
          chip(decisionLabels[decision] || decision, decision),
          chip(`热度 ${cluster.heat_score}`),
          chip(`证据 ${cluster.evidence_quality}`),
          chip(`机会 ${cluster.content_opportunity_score}`),
          chip(`风险 ${cluster.risk_level}`)
        ].join("");
        return `
          <article class="cluster">
            <h3>${cluster.game_name} - ${cluster.need_key}</h3>
            <p class="muted">${cluster.representative_question}</p>
            <div class="chips">${labels}</div>
            <p class="muted">${(cluster.piko_value_add || []).slice(0, 2).join(" ")}</p>
          </article>
        `;
      }

      clusterCard = function(cluster) {
        const decision = cluster.decision || "unknown";
        const labels = [
          chip(cluster.decision_label || decisionLabels[decision] || decision, decision),
          chip(`热度 ${cluster.heat_score}`),
          chip(`证据 ${cluster.evidence_quality}`),
          chip(`机会 ${cluster.content_opportunity_score}`),
          chip(cluster.risk_label || `风险 ${cluster.risk_level}`)
        ].join("");
        return `
          <article class="cluster">
            <h3>${cluster.game_name} - ${cluster.need_key}</h3>
            <p class="muted">${cluster.representative_question}</p>
            <div class="chips">${labels}</div>
            <p class="muted">${cluster.plain_summary || ""}</p>
          </article>
        `;
      };

      function renderStep(step, index) {
        const clusters = step.outputs && step.outputs.clusters ? step.outputs.clusters : [];
        const topByDecision = step.outputs && step.outputs.top_by_decision ? step.outputs.top_by_decision : null;
        let visual = "";
        if (clusters.length) {
          visual = `<div class="panel"><h3>聚类结果</h3><div class="clusters">${clusters.map(clusterCard).join("")}</div></div>`;
        } else if (topByDecision) {
          const cards = Object.values(topByDecision).flat();
          visual = `<div class="panel"><h3>各漏斗桶代表 topic</h3><div class="clusters">${cards.map(clusterCard).join("")}</div></div>`;
        } else if (step.outputs && step.outputs.publish_candidates) {
          const cards = [
            ...(step.outputs.publish_candidates || []),
            ...(step.outputs.watchlist || []),
            ...(step.outputs.conflict_explainers || []),
            ...(step.outputs.high_risk_blocked || [])
          ];
          visual = `<div class="panel"><h3>分流结果</h3><div class="clusters">${cards.map(clusterCard).join("")}</div></div>`;
        }
        return `
          <details class="step" ${index < 3 ? "open" : ""}>
            <summary>
              <span>${step.title}</span>
              <span class="muted">${step.step_id}</span>
            </summary>
            <div class="step-body">
              <p><strong>动作：</strong>${step.agent_action}</p>
              <p><strong>护栏：</strong>${(step.guardrails || []).join(" / ")}</p>
              ${visual}
              <div class="grid">
                <div class="panel">
                  <h3>输入</h3>
                  <pre>${asJson(step.inputs)}</pre>
                </div>
                <div class="panel">
                  <h3>输出</h3>
                  <pre>${asJson(step.outputs)}</pre>
                </div>
              </div>
            </div>
          </details>
        `;
      }

      function payload() {
        return {
          query: document.getElementById("query").value.trim() || null,
          min_game_heat: Number(document.getElementById("minGameHeat").value || 50),
          limit: Number(document.getElementById("limit").value || 20)
        };
      }

      async function run() {
        const button = document.getElementById("runButton");
        const status = document.getElementById("status");
        button.disabled = true;
        status.textContent = "正在运行漏斗分析...";
        try {
          const response = await fetch("/discovery/funnel-trace", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload())
          });
          if (!response.ok) throw new Error(`HTTP ${response.status}`);
          const data = await response.json();
          document.getElementById("metrics").innerHTML = [
            metric("平台族", data.summary.platform_count),
            metric("游戏信号", data.summary.raw_game_count),
            metric("问题信号", data.summary.raw_question_count),
            metric("聚类 topic", data.summary.cluster_count),
            metric("真实采集", String(data.real_collection_performed))
          ].join("");
          document.getElementById("steps").innerHTML = data.steps.map(renderStep).join("");
          status.textContent = `完成：${data.mode} 模式，publish_ready=false，publishing_performed=false。`;
        } catch (error) {
          status.innerHTML = `<div class="error">${error.message}</div>`;
        } finally {
          button.disabled = false;
        }
      }

      document.getElementById("runButton").addEventListener("click", run);
      run();
    </script>
  </body>
</html>
"""


@router.post("/real-source/collect")
def collect_real_source_discovery(request: dict[str, object]) -> dict[str, object]:
    query = str(request.get("query") or "")
    limit = int(request.get("limit_per_source") or 10)
    try:
        return RealMarketDiscoverySource.from_settings().collect(query=query, limit_per_source=limit)
    except DiscoveryRealSourceDisabledError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except DiscoveryRealSourceConfigurationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except DiscoveryRealSourceFetchError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.get("/window", response_class=HTMLResponse)
def discovery_window() -> str:
    return """
<!doctype html>
<html lang="zh-CN">
  <head>
    <title>Piko 痛点发现窗口</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <style>
      :root {
        --bg: #f7f8fa;
        --panel: #ffffff;
        --line: #d8dee8;
        --text: #111827;
        --muted: #5b6472;
        --accent: #0f766e;
        --accent-dark: #115e59;
        --warn: #b45309;
        --danger: #b91c1c;
        --ok: #166534;
      }

      * { box-sizing: border-box; }

      body {
        margin: 0;
        background: var(--bg);
        color: var(--text);
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      }

      header {
        border-bottom: 1px solid var(--line);
        background: var(--panel);
        padding: 18px 24px;
      }

      h1 {
        margin: 0;
        font-size: 24px;
        line-height: 1.2;
        letter-spacing: 0;
      }

      .subhead {
        margin-top: 6px;
        color: var(--muted);
        font-size: 14px;
      }

      main {
        display: grid;
        grid-template-columns: 320px minmax(0, 1fr);
        min-height: calc(100vh - 80px);
      }

      aside {
        border-right: 1px solid var(--line);
        background: var(--panel);
        padding: 18px;
      }

      section {
        padding: 18px 22px 28px;
      }

      label {
        display: block;
        margin: 14px 0 6px;
        color: var(--muted);
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
      }

      input, select {
        width: 100%;
        min-height: 36px;
        border: 1px solid var(--line);
        border-radius: 6px;
        background: #fff;
        color: var(--text);
        padding: 7px 9px;
        font-size: 14px;
      }

      button {
        width: 100%;
        min-height: 38px;
        margin-top: 16px;
        border: 0;
        border-radius: 6px;
        background: var(--accent);
        color: white;
        cursor: pointer;
        font-size: 14px;
        font-weight: 700;
      }

      button:hover { background: var(--accent-dark); }
      button:disabled { cursor: wait; opacity: 0.6; }

      .safety {
        margin-top: 16px;
        border-top: 1px solid var(--line);
        padding-top: 14px;
        color: var(--muted);
        font-size: 13px;
        line-height: 1.5;
      }

      .metrics {
        display: grid;
        grid-template-columns: repeat(5, minmax(120px, 1fr));
        gap: 10px;
        margin-bottom: 14px;
      }

      .rankings {
        display: grid;
        grid-template-columns: minmax(0, 1.35fr) minmax(280px, 0.9fr);
        gap: 14px;
        margin-bottom: 14px;
      }

      .ranking-panel {
        border: 1px solid var(--line);
        border-radius: 8px;
        background: var(--panel);
        padding: 14px;
      }

      .ranking-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(180px, 1fr));
        gap: 10px;
      }

      .rank-row {
        border-top: 1px solid var(--line);
        padding: 10px 0;
      }

      .rank-row:first-child {
        border-top: 0;
        padding-top: 0;
      }

      .rank-line {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
      }

      .rank-name {
        font-weight: 800;
      }

      .rank-score {
        color: var(--accent-dark);
        font-weight: 800;
        white-space: nowrap;
      }

      .metric, .cluster, .game {
        border: 1px solid var(--line);
        border-radius: 8px;
        background: var(--panel);
      }

      .metric {
        padding: 12px;
      }

      .metric strong {
        display: block;
        margin-top: 4px;
        font-size: 24px;
      }

      .metric span {
        color: var(--muted);
        font-size: 12px;
        text-transform: uppercase;
      }

      .layout {
        display: grid;
        grid-template-columns: minmax(0, 1fr) 340px;
        gap: 14px;
      }

      .list {
        display: grid;
        gap: 10px;
      }

      .cluster, .game {
        padding: 14px;
      }

      .cluster-head {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 12px;
      }

      .title {
        margin: 0;
        font-size: 16px;
        line-height: 1.35;
      }

      .question {
        margin: 5px 0 0;
        color: var(--muted);
        font-size: 13px;
        line-height: 1.45;
      }

      .badge {
        display: inline-flex;
        align-items: center;
        min-height: 24px;
        border-radius: 999px;
        padding: 3px 9px;
        white-space: nowrap;
        font-size: 12px;
        font-weight: 700;
        background: #e5e7eb;
        color: #374151;
      }

      .publish_candidate { background: #dcfce7; color: var(--ok); }
      .watchlist_waiting_for_answer { background: #fef3c7; color: var(--warn); }
      .conflict_explainer { background: #dbeafe; color: #1d4ed8; }
      .blocked_high_risk { background: #fee2e2; color: var(--danger); }
      .ignore { background: #e5e7eb; color: #374151; }

      .score-row {
        display: grid;
        grid-template-columns: repeat(5, minmax(74px, 1fr));
        gap: 8px;
        margin-top: 12px;
      }

      .score {
        border-top: 1px solid var(--line);
        padding-top: 8px;
      }

      .score span {
        display: block;
        color: var(--muted);
        font-size: 11px;
      }

      .score strong {
        font-size: 15px;
      }

      .chips {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        margin-top: 10px;
      }

      .chip {
        border: 1px solid var(--line);
        border-radius: 999px;
        padding: 3px 8px;
        color: var(--muted);
        font-size: 12px;
      }

      .side-title {
        margin: 0 0 10px;
        font-size: 15px;
      }

      .methodology {
        margin: 8px 0 0;
        color: var(--muted);
        font-size: 12px;
        line-height: 1.45;
      }

      .game + .game { margin-top: 10px; }

      .status {
        margin-bottom: 12px;
        color: var(--muted);
        font-size: 13px;
      }

      .error {
        border: 1px solid #fecaca;
        border-radius: 8px;
        background: #fef2f2;
        color: var(--danger);
        padding: 12px;
      }

      @media (max-width: 980px) {
        main, .layout {
          grid-template-columns: 1fr;
        }

        aside {
          border-right: 0;
          border-bottom: 1px solid var(--line);
        }

        .metrics {
          grid-template-columns: repeat(2, minmax(120px, 1fr));
        }

        .rankings, .ranking-grid {
          grid-template-columns: 1fr;
        }
      }
    </style>
  </head>
  <body>
    <span hidden>Piko Discovery Window</span>
    <div class="status">
      Ranking mode: fixture by default. Current hot games Top 5, Must-check guide topics, Answered vs unresolved hot questions, Conflict answer topics, and High-risk blocked topics are candidate-only discovery rankings.
    </div>
    <header>
      <h1>Piko 痛点发现窗口</h1>
      <div class="subhead">玩家痛点发现漏斗。这里只输出候选信号，不代表允许发布。</div>
    </header>
    <main>
      <aside>
        <label for="query">搜索关键词</label>
        <input id="query" placeholder="存档、崩溃、Steam Deck" />

        <label for="decision">筛选结论</label>
        <select id="decision">
          <option value="">全部结论</option>
          <option value="publish_candidate">可进入内容生产</option>
          <option value="watchlist_waiting_for_answer">进入监控区</option>
          <option value="conflict_explainer">冲突解释</option>
          <option value="blocked_high_risk">高风险阻断</option>
          <option value="ignore">暂不处理</option>
        </select>

        <label for="intent">问题类型</label>
        <select id="intent">
          <option value="">全部类型</option>
          <option value="bug_fix">Bug 修复</option>
          <option value="save_file">存档相关</option>
          <option value="settings">设置/性能</option>
          <option value="build">Build/配装</option>
          <option value="map_exploration">地图探索</option>
          <option value="hidden_item">隐藏物品</option>
          <option value="quest_blocker">任务卡点</option>
        </select>

        <label for="minGameHeat">最低游戏热度</label>
        <input id="minGameHeat" type="number" min="0" max="100" value="50" />

        <label for="minOpportunity">最低内容机会分</label>
        <input id="minOpportunity" type="number" min="0" max="100" value="0" />

        <label for="limit">返回数量</label>
        <input id="limit" type="number" min="1" max="100" value="10" />

        <button id="runButton" type="button">开始发现痛点</button>
        <button id="realButton" type="button">真实来源采集（需开关）</button>

        <div class="safety">
          <div><strong>运行模式：</strong> <span id="mode">fixture</span></div>
          <div><strong>真实采集：</strong> <span id="realCollection">false</span></div>
          <div><strong>发布能力：</strong> 已禁用</div>
        </div>
      </aside>

      <section>
        <div id="status" class="status">已准备好。</div>
        <div class="ranking-panel" aria-label="RM-3 ranking sections">
          <h2 class="side-title">RM-3 ranking mode</h2>
          <div class="chips">
            <span class="chip">游戏类型排行榜</span>
            <span class="chip">玩家画像/兴趣画像排行榜</span>
            <span class="chip">必须查攻略的问题排行</span>
            <span class="chip">已有答案 / 未解决高热问题</span>
            <span class="chip">冲突答案榜</span>
            <span class="chip">高风险阻断榜</span>
          </div>
          <p class="methodology">这些榜单默认使用 fixture mode；真实来源仍需显式双 opt-in，Discovery output 仍只是候选信号，不是发布许可。</p>
        </div>
        <div class="rankings">
          <div class="ranking-panel">
            <h2 class="side-title">当前攻略机会热榜 Top 5</h2>
            <div id="topHotGames"></div>
            <p class="methodology" id="rankingMethodology"></p>
          </div>
          <div class="ranking-panel">
            <h2 class="side-title">不同维度排行榜</h2>
            <div class="ranking-grid">
              <div>
                <h3 class="side-title">玩家画像</h3>
                <div id="audienceRankings"></div>
              </div>
              <div>
                <h3 class="side-title">问题类型</h3>
                <div id="typeRankings"></div>
              </div>
              <div>
                <h3 class="side-title">漏斗结论</h3>
                <div id="decisionRankings"></div>
              </div>
              <div>
                <h3 class="side-title">必须查攻略的问题</h3>
                <div id="guideNeedRankings"></div>
              </div>
            </div>
          </div>
        </div>
        <div class="metrics" id="metrics"></div>
        <div class="layout">
          <div class="list" id="clusters"></div>
          <div>
            <h2 class="side-title">热门游戏</h2>
            <div id="games"></div>
          </div>
        </div>
      </section>
    </main>
    <script>
      const decisionLabels = {
        publish_candidate: "可生产",
        watchlist_waiting_for_answer: "监控中",
        conflict_explainer: "冲突解释",
        blocked_high_risk: "高风险",
        ignore: "暂不处理"
      };

      const intentLabels = {
        bug_fix: "Bug 修复",
        location: "位置指引",
        walkthrough: "流程攻略",
        build: "Build/配装",
        settings: "设置/性能",
        compatibility: "兼容性",
        save_file: "存档相关",
        map_exploration: "地图探索",
        hidden_item: "隐藏物品",
        quest_blocker: "任务卡点"
      };

      const answerLabels = {
        answered: "已有答案",
        unanswered: "暂无答案",
        conflicting: "答案冲突",
        partial: "部分答案",
        unknown: "未知"
      };

      const lifecycleLabels = {
        new: "新问题",
        rising: "上升中",
        stable: "稳定",
        declining: "下降中",
        resolved: "已解决",
        stale: "已过期"
      };

      const actionabilityLabels = {
        single_page_answerable: "可单页解答",
        needs_more_sources: "需要更多来源",
        too_broad: "范围过宽",
        too_risky: "风险过高",
        too_visual: "过度依赖视觉"
      };

      const riskLabels = {
        low: "低",
        medium: "中",
        high: "高"
      };

      const nextActionLabels = {
        send_to_evidence_pipeline: "送入证据链",
        add_to_watchlist: "加入监控区",
        prepare_conflict_brief: "准备冲突解释稿",
        block_publish_and_prepare_safety_note: "阻断发布并准备安全提示",
        no_action: "暂不处理",
        review_candidate: "人工复核候选"
      };

      const typeRankingLabels = {
        bug_fix: "Bug 修复",
        save_file: "存档相关",
        settings: "设置/性能",
        build: "Build/配装",
        map_exploration: "地图探索",
        hidden_item: "隐藏物品",
        quest_blocker: "任务卡点",
        walkthrough: "流程攻略"
      };

      function fieldValue(id) {
        return document.getElementById(id).value.trim();
      }

      function numberValue(id, fallback) {
        const value = Number(fieldValue(id));
        return Number.isFinite(value) ? value : fallback;
      }

      function requestPayload() {
        const decision = fieldValue("decision");
        const intent = fieldValue("intent");
        const payload = {
          query: fieldValue("query") || null,
          min_game_heat: numberValue("minGameHeat", 50),
          min_content_opportunity_score: numberValue("minOpportunity", 0),
          limit: numberValue("limit", 10)
        };
        if (decision) payload.decisions = [decision];
        if (intent) payload.search_intents = [intent];
        return payload;
      }

      function metric(label, value) {
        return `<div class="metric"><span>${label}</span><strong>${value}</strong></div>`;
      }

      function chip(value) {
        return `<span class="chip">${value}</span>`;
      }

      function renderMetrics(data) {
        const counts = data.funnel_counts || {};
        document.getElementById("metrics").innerHTML = [
          metric("可生产", counts.publish_candidate || 0),
          metric("监控区", counts.watchlist_waiting_for_answer || 0),
          metric("冲突解释", counts.conflict_explainer || 0),
          metric("高风险", counts.blocked_high_risk || 0),
          metric("总数", (data.clusters || []).length)
        ].join("");
      }

      function renderClusters(clusters) {
        const target = document.getElementById("clusters");
        if (!clusters.length) {
          target.innerHTML = `<div class="cluster">当前筛选条件下没有匹配的话题簇。</div>`;
          return;
        }
        target.innerHTML = clusters.map((cluster) => {
          const decision = cluster.decision || "unknown";
          const label = decisionLabels[decision] || decision;
          const sources = [...(cluster.source_types || []), ...(cluster.source_regions || [])].slice(0, 6);
          const nextAction = nextActionLabels[cluster.recommended_next_action] || cluster.recommended_next_action;
          return `
            <article class="cluster">
              <div class="cluster-head">
                <div>
                  <h2 class="title">${cluster.game_name} - ${cluster.need_key}</h2>
                  <p class="question">${cluster.representative_question}</p>
                </div>
                <span class="badge ${decision}">${label}</span>
              </div>
              <div class="score-row">
                <div class="score"><span>机会分</span><strong>${cluster.content_opportunity_score}</strong></div>
                <div class="score"><span>热度</span><strong>${cluster.heat_score}</strong></div>
                <div class="score"><span>证据</span><strong>${cluster.evidence_quality}</strong></div>
                <div class="score"><span>风险</span><strong>${riskLabels[cluster.risk_level] || cluster.risk_level}</strong></div>
                <div class="score"><span>可执行性</span><strong>${actionabilityLabels[cluster.actionability_label] || cluster.actionability_label}</strong></div>
              </div>
              <div class="chips">
                ${chip(intentLabels[cluster.search_intent] || cluster.search_intent)}
                ${chip(answerLabels[cluster.answer_status] || cluster.answer_status)}
                ${chip(lifecycleLabels[cluster.topic_lifecycle] || cluster.topic_lifecycle)}
                ${sources.map(chip).join("")}
              </div>
              <p class="question">${nextAction}。${cluster.recommended_article_intent}</p>
            </article>
          `;
        }).join("");
      }

      function renderGames(games) {
        const target = document.getElementById("games");
        if (!games.length) {
          target.innerHTML = `<div class="game">当前筛选条件下没有匹配的热门游戏。</div>`;
          return;
        }
        target.innerHTML = games.map((game) => `
          <div class="game">
            <h3 class="title">${game.game_name}</h3>
            <div class="score-row">
              <div class="score"><span>热度</span><strong>${game.heat_score}</strong></div>
              <div class="score"><span>排名</span><strong>${game.steam_player_rank || "-"}</strong></div>
              <div class="score"><span>讨论</span><strong>${game.community_post_velocity}</strong></div>
            </div>
            <div class="chips">${(game.region_signals || []).map(chip).join("")}</div>
          </div>
        `).join("");
      }

      function renderRankRows(targetId, rows, options = {}) {
        const target = document.getElementById(targetId);
        if (!rows || !rows.length) {
          target.innerHTML = `<div class="rank-row">暂无数据。</div>`;
          return;
        }
        target.innerHTML = rows.map((row, index) => {
          const name = options.name ? options.name(row) : (row.game_name || row.value || row.need_key);
          const score = options.score ? options.score(row) : (row.guide_need_score || row.score || 0);
          const detail = options.detail ? options.detail(row) : (row.reason || row.top_need || row.decision || "");
          return `
            <div class="rank-row">
              <div class="rank-line">
                <span class="rank-name">${index + 1}. ${name}</span>
                <span class="rank-score">${score}</span>
              </div>
              <p class="question">${detail}</p>
            </div>
          `;
        }).join("");
      }

      function renderRankings(data) {
        document.getElementById("rankingMethodology").textContent = data.methodology || "";
        renderRankRows("topHotGames", data.top_hot_games || [], {
          name: (row) => row.game_name,
          score: (row) => row.guide_need_score,
          detail: (row) => `${row.game_type}｜最值得写：${row.top_need}｜${row.reason}`
        });
        renderRankRows("audienceRankings", (data.audience_rankings || []).slice(0, 6), {
          name: (row) => `${row.profile_label}：${row.game_name}`,
          score: (row) => row.score,
          detail: (row) => `${row.need_key}｜${row.profile_description}`
        });
        renderRankRows("typeRankings", data.game_type_rankings || [], {
          name: (row) => typeRankingLabels[row.value] || row.value,
          score: (row) => row.score,
          detail: (row) => `${row.topic_count} 个话题｜代表游戏：${row.top_game}｜${row.top_need}`
        });
        renderRankRows("decisionRankings", data.decision_rankings || [], {
          name: (row) => decisionLabels[row.value] || row.value,
          score: (row) => row.score,
          detail: (row) => `${row.topic_count} 个话题｜代表游戏：${row.top_game}｜${row.top_need}`
        });
        renderRankRows("guideNeedRankings", data.top_guide_needs || [], {
          name: (row) => `${row.game_name}：${row.need_key}`,
          score: (row) => row.guide_need_score,
          detail: (row) => `${decisionLabels[row.decision] || row.decision}｜热度 ${row.heat_score}｜证据 ${row.evidence_quality}`
        });
      }

      async function loadRankings() {
        const response = await fetch("/discovery/rankings?limit=5");
        if (!response.ok) throw new Error(`rankings HTTP ${response.status}`);
        renderRankings(await response.json());
      }

      async function runDiscovery() {
        const button = document.getElementById("runButton");
        const status = document.getElementById("status");
        button.disabled = true;
        status.textContent = "正在发现玩家痛点...";
        try {
          const response = await fetch("/discovery/search", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(requestPayload())
          });
          if (!response.ok) throw new Error(`HTTP ${response.status}`);
          const data = await response.json();
          document.getElementById("mode").textContent = data.mode;
          document.getElementById("realCollection").textContent = String(data.real_collection_performed);
          renderMetrics(data);
          renderClusters(data.clusters || []);
          renderGames(data.game_candidates || []);
          status.textContent = `已完成。返回 ${(data.clusters || []).length} 个话题簇。`;
        } catch (error) {
          status.innerHTML = `<div class="error">${error.message}</div>`;
        } finally {
          button.disabled = false;
        }
      }

      function renderRealQuestions(data) {
        const questions = data.questions || [];
        const games = data.games || [];
        renderMetrics({ funnel_counts: {}, clusters: questions });
        renderGames(games.map((game) => ({
          game_name: game.game_name,
          heat_score: game.heat_score || 0,
          steam_player_rank: game.steam_player_rank,
          community_post_velocity: game.community_post_velocity || 0,
          region_signals: game.region_signals || []
        })));
        document.getElementById("clusters").innerHTML = questions.length
          ? questions.map((question) => `
              <article class="cluster">
                <div class="cluster-head">
                  <div>
                    <h2 class="title">${question.game_name} - ${question.source_type}</h2>
                    <p class="question">${question.question_text}</p>
                  </div>
                  <span class="badge conflict_explainer">真实来源</span>
                </div>
                <div class="score-row">
                  <div class="score"><span>互动</span><strong>${question.engagement_count}</strong></div>
                  <div class="score"><span>回复</span><strong>${question.reply_count}</strong></div>
                  <div class="score"><span>增长</span><strong>${question.growth_24h}</strong></div>
                  <div class="score"><span>证据</span><strong>${question.evidence_quality}</strong></div>
                  <div class="score"><span>风险</span><strong>${riskLabels[question.risk_level] || question.risk_level}</strong></div>
                </div>
                <div class="chips">
                  ${chip(question.source_region)}
                  ${(question.tags || []).slice(0, 5).map(chip).join("")}
                </div>
                <p class="question">${question.snippet || "已保留结构化字段；未保存完整正文。"}</p>
              </article>
            `).join("")
          : `<div class="cluster">真实来源没有返回问题记录。</div>`;
      }

      async function runRealSource() {
        const button = document.getElementById("realButton");
        const status = document.getElementById("status");
        button.disabled = true;
        status.textContent = "正在尝试真实来源采集...";
        try {
          const response = await fetch("/discovery/real-source/collect", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query: fieldValue("query"), limit_per_source: numberValue("limit", 10) })
          });
          const data = await response.json();
          if (!response.ok) throw new Error(data.detail || `HTTP ${response.status}`);
          document.getElementById("mode").textContent = data.mode;
          document.getElementById("realCollection").textContent = String(data.real_collection_performed);
          renderRealQuestions(data);
          status.textContent = `真实来源采集完成。返回 ${(data.questions || []).length} 条问题记录。`;
        } catch (error) {
          status.innerHTML = `<div class="error">${error.message}</div>`;
        } finally {
          button.disabled = false;
        }
      }

      document.getElementById("runButton").addEventListener("click", runDiscovery);
      document.getElementById("realButton").addEventListener("click", runRealSource);
      loadRankings();
      runDiscovery();
    </script>
  </body>
</html>
"""

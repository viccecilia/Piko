from fastapi import APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse


router = APIRouter()


VERIFICATION_WINDOW_HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Piko Verification Window</title>
  <style>
    :root {
      color-scheme: light;
      --bg: #f6f5ef;
      --panel: #ffffff;
      --ink: #171717;
      --muted: #65645f;
      --line: #dedbd0;
      --accent: #0f766e;
      --accent-strong: #115e59;
      --pass: #17803d;
      --fail: #b42318;
      --warn: #a15c07;
      --shadow: 0 12px 35px rgba(31, 28, 20, 0.08);
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      min-height: 100vh;
      background: var(--bg);
      color: var(--ink);
      font-family:
        Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
        "Segoe UI", sans-serif;
    }

    button,
    input {
      font: inherit;
    }

    .shell {
      width: min(1180px, calc(100vw - 32px));
      margin: 0 auto;
      padding: 24px 0 32px;
    }

    header {
      display: flex;
      align-items: flex-end;
      justify-content: space-between;
      gap: 20px;
      margin-bottom: 18px;
    }

    h1 {
      margin: 0;
      font-size: 30px;
      line-height: 1.15;
      font-weight: 760;
      letter-spacing: 0;
    }

    .meta {
      margin-top: 6px;
      color: var(--muted);
      font-size: 14px;
    }

    .status {
      min-width: 180px;
      padding: 10px 12px;
      border: 1px solid var(--line);
      background: var(--panel);
      box-shadow: var(--shadow);
      border-radius: 8px;
      text-align: right;
      color: var(--muted);
      font-size: 14px;
    }

    .status strong {
      display: block;
      color: var(--ink);
      font-size: 18px;
      line-height: 1.25;
    }

    .layout {
      display: grid;
      grid-template-columns: 320px minmax(0, 1fr);
      gap: 16px;
      align-items: start;
    }

    .panel {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: var(--shadow);
    }

    .controls {
      padding: 16px;
      position: sticky;
      top: 16px;
    }

    .field {
      display: grid;
      gap: 7px;
      margin-bottom: 13px;
    }

    label {
      color: var(--muted);
      font-size: 13px;
      font-weight: 650;
    }

    input {
      width: 100%;
      min-height: 40px;
      border: 1px solid var(--line);
      border-radius: 7px;
      padding: 9px 10px;
      color: var(--ink);
      background: #fbfaf6;
    }

    input:focus {
      border-color: var(--accent);
      outline: 2px solid rgba(15, 118, 110, 0.16);
    }

    .actions {
      display: flex;
      gap: 10px;
      margin-top: 16px;
    }

    button {
      border: 1px solid transparent;
      border-radius: 7px;
      min-height: 40px;
      padding: 9px 12px;
      cursor: pointer;
      font-weight: 700;
    }

    button.primary {
      background: var(--accent);
      color: #ffffff;
      flex: 1;
    }

    button.primary:hover {
      background: var(--accent-strong);
    }

    button.secondary {
      background: #ffffff;
      border-color: var(--line);
      color: var(--ink);
    }

    button:disabled {
      cursor: wait;
      opacity: 0.68;
    }

    .main {
      display: grid;
      gap: 16px;
    }

    .summary {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 10px;
      padding: 12px;
    }

    .metric {
      border: 1px solid var(--line);
      border-radius: 7px;
      padding: 12px;
      background: #fbfaf6;
      min-height: 86px;
    }

    .metric span {
      display: block;
      color: var(--muted);
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
    }

    .metric strong {
      display: block;
      margin-top: 8px;
      font-size: 22px;
      line-height: 1.15;
      overflow-wrap: anywhere;
    }

    .section {
      padding: 16px;
    }

    h2 {
      margin: 0 0 12px;
      font-size: 18px;
      letter-spacing: 0;
    }

    .brief-grid {
      display: grid;
      grid-template-columns: minmax(0, 1fr) minmax(220px, 0.42fr);
      gap: 12px;
    }

    .text-block {
      border: 1px solid var(--line);
      border-radius: 7px;
      padding: 12px;
      background: #fbfaf6;
      min-height: 92px;
    }

    .text-block .label {
      color: var(--muted);
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      margin-bottom: 7px;
    }

    ul {
      margin: 0;
      padding-left: 20px;
    }

    li {
      margin: 6px 0;
    }

    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 14px;
    }

    th,
    td {
      text-align: left;
      padding: 11px 10px;
      border-bottom: 1px solid var(--line);
      vertical-align: top;
    }

    th {
      color: var(--muted);
      font-size: 12px;
      text-transform: uppercase;
    }

    tr:last-child td {
      border-bottom: 0;
    }

    .pill {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-width: 58px;
      border-radius: 999px;
      padding: 4px 8px;
      font-size: 12px;
      font-weight: 800;
      text-transform: uppercase;
    }

    .pill.pass {
      background: rgba(23, 128, 61, 0.12);
      color: var(--pass);
    }

    .pill.fail {
      background: rgba(180, 35, 24, 0.12);
      color: var(--fail);
    }

    .pill.review {
      background: rgba(161, 92, 7, 0.13);
      color: var(--warn);
    }

    .muted {
      color: var(--muted);
    }

    .json {
      max-height: 330px;
      overflow: auto;
      margin: 0;
      padding: 13px;
      background: #1f2937;
      color: #f9fafb;
      border-radius: 7px;
      font-size: 12px;
      line-height: 1.55;
    }

    .empty {
      min-height: 360px;
      display: grid;
      place-items: center;
      color: var(--muted);
      text-align: center;
      padding: 32px;
    }

    @media (max-width: 860px) {
      header,
      .layout,
      .brief-grid,
      .summary {
        grid-template-columns: 1fr;
      }

      header {
        align-items: stretch;
      }

      .status {
        text-align: left;
      }

      .controls {
        position: static;
      }
    }
  </style>
</head>
<body>
  <div class="shell">
    <header>
      <div>
        <h1>Piko Verification Window</h1>
        <div class="meta">Article pipeline verification surface</div>
      </div>
      <div class="status" aria-live="polite">
        <span>Current result</span>
        <strong id="current-result">Ready</strong>
      </div>
    </header>

    <div class="layout">
      <form id="verify-form" class="panel controls">
        <div class="field">
          <label for="game-id">Game ID</label>
          <input id="game-id" name="game_id" value="game_mock_001" autocomplete="off">
        </div>
        <div class="field">
          <label for="game-name">Game name</label>
          <input id="game-name" name="game_name" value="Example Game" autocomplete="off">
        </div>
        <div class="field">
          <label for="topic">Topic</label>
          <input id="topic" name="topic" value="crash on startup" autocomplete="off">
        </div>
        <div class="actions">
          <button class="primary" id="run-button" type="submit">Run check</button>
          <button class="secondary" id="reset-button" type="button">Reset</button>
        </div>
      </form>

      <main id="output" class="main">
        <section class="panel empty">
          <div>
            <strong>No run loaded</strong>
            <p class="muted">Submit a topic to inspect the generated brief and gate decisions.</p>
          </div>
        </section>
      </main>
    </div>
  </div>

  <script>
    const form = document.getElementById("verify-form");
    const output = document.getElementById("output");
    const runButton = document.getElementById("run-button");
    const resetButton = document.getElementById("reset-button");
    const currentResult = document.getElementById("current-result");

    function escapeHtml(value) {
      return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
    }

    function renderList(items) {
      if (!items || items.length === 0) {
        return '<span class="muted">None</span>';
      }
      return `<ul>${items.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>`;
    }

    function renderGateRows(gates) {
      return gates.map((gate) => {
        const decision = escapeHtml(gate.decision);
        const reasons = gate.reasons && gate.reasons.length
          ? gate.reasons.map((reason) => escapeHtml(reason)).join("<br>")
          : '<span class="muted">No reason provided</span>';
        return `
          <tr>
            <td>${escapeHtml(gate.gate)}</td>
            <td><span class="pill ${decision}">${decision}</span></td>
            <td>${escapeHtml(gate.score)}</td>
            <td>${gate.blocks_publish ? "Yes" : "No"}</td>
            <td>${reasons}</td>
          </tr>
        `;
      }).join("");
    }

    function renderResult(data) {
      const brief = data.article_brief;
      const gates = data.gate_results || [];
      const failedCount = gates.filter((gate) => gate.decision === "fail").length;
      const blockedCount = gates.filter((gate) => gate.blocks_publish).length;
      const action = data.publish_action || "unknown";
      const verificationStatus = data.verification_report?.status || "unknown";
      const publishDecision = data.publish_decision?.value || "unknown";
      const resultLabel = blockedCount ? "Blocked" : action.replaceAll("_", " ");
      currentResult.textContent = resultLabel;

      output.innerHTML = `
        <section class="panel summary">
          <div class="metric">
            <span>Status</span>
            <strong>${escapeHtml(data.status)}</strong>
          </div>
          <div class="metric">
            <span>Publish action</span>
            <strong><span class="pill review">${escapeHtml(action)}</span></strong>
          </div>
          <div class="metric">
            <span>Publish decision</span>
            <strong>${escapeHtml(publishDecision)}</strong>
          </div>
          <div class="metric">
            <span>Verification</span>
            <strong><span class="pill ${escapeHtml(verificationStatus)}">${escapeHtml(verificationStatus)}</span></strong>
          </div>
          <div class="metric">
            <span>Confidence</span>
            <strong>${escapeHtml(brief.confidence)}%</strong>
          </div>
          <div class="metric">
            <span>Gate issues</span>
            <strong>${failedCount} fail / ${blockedCount} block</strong>
          </div>
        </section>

        <section class="panel section">
          <h2>Article Brief</h2>
          <div class="brief-grid">
            <div class="text-block">
              <div class="label">Intent</div>
              ${escapeHtml(brief.article_intent)}
            </div>
            <div class="text-block">
              <div class="label">Last checked</div>
              ${escapeHtml(brief.last_checked)}
            </div>
            <div class="text-block">
              <div class="label">Primary user pain</div>
              ${escapeHtml(brief.primary_user_pain)}
            </div>
            <div class="text-block">
              <div class="label">Platform</div>
              ${escapeHtml(brief.platform)}
            </div>
            <div class="text-block">
              <div class="label">Quick answer</div>
              ${renderList(brief.quick_answer)}
            </div>
            <div class="text-block">
              <div class="label">Do not recommend</div>
              ${renderList(brief.do_not_recommend)}
            </div>
          </div>
        </section>

        <section class="panel section">
          <h2>Gate Results</h2>
          <table>
            <thead>
              <tr>
                <th>Gate</th>
                <th>Decision</th>
                <th>Score</th>
                <th>Blocks</th>
                <th>Reasons</th>
              </tr>
            </thead>
            <tbody>${renderGateRows(gates)}</tbody>
          </table>
        </section>

        <section class="panel section">
          <h2>Raw Run</h2>
          <pre class="json">${escapeHtml(JSON.stringify(data, null, 2))}</pre>
        </section>
      `;
    }

    async function runVerification(event) {
      event.preventDefault();
      runButton.disabled = true;
      currentResult.textContent = "Running";

      const payload = Object.fromEntries(new FormData(form).entries());

      try {
        const response = await fetch("/workflow/article-pipeline/run", {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify(payload),
        });

        if (!response.ok) {
          throw new Error(`Request failed with ${response.status}`);
        }

        renderResult(await response.json());
      } catch (error) {
        currentResult.textContent = "Error";
        output.innerHTML = `
          <section class="panel empty">
            <div>
              <strong>Verification failed</strong>
              <p class="muted">${escapeHtml(error.message)}</p>
            </div>
          </section>
        `;
      } finally {
        runButton.disabled = false;
      }
    }

    resetButton.addEventListener("click", () => {
      form.reset();
      currentResult.textContent = "Ready";
      output.innerHTML = `
        <section class="panel empty">
          <div>
            <strong>No run loaded</strong>
            <p class="muted">Submit a topic to inspect the generated brief and gate decisions.</p>
          </div>
        </section>
      `;
    });

    form.addEventListener("submit", runVerification);
  </script>
</body>
</html>
"""


@router.get("", include_in_schema=False)
def verification_index() -> RedirectResponse:
    return RedirectResponse(url="/verification/window")


@router.get("/window", response_class=HTMLResponse)
def verification_window() -> str:
    return VERIFICATION_WINDOW_HTML

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from packages.capability_map.pipeline import capability_surface


router = APIRouter()


@router.get("")
def capabilities() -> dict[str, object]:
    return capability_surface()


@router.get("/window", response_class=HTMLResponse)
def capabilities_window() -> str:
    surface = capability_surface()
    registry = surface["registry"]
    scorecard = surface["scorecard"]
    entries = registry.get("entries", [])[:40]
    rows = "\n".join(
        f"<tr><td>{item['capability_id']}</td><td>{item['kind']}</td><td>{item['status']}</td><td>{item['network_policy']}</td><td>{str(item['requires_credentials']).lower()}</td></tr>"
        for item in entries
    )
    improvement_count = len(scorecard.get("top_improvement_targets", []))
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Piko Capability Map</title>
  <style>
    body {{ margin: 0; font-family: Arial, sans-serif; background: #f7f8fa; color: #111827; }}
    main {{ max-width: 1100px; margin: 0 auto; padding: 28px 18px; }}
    table {{ width: 100%; border-collapse: collapse; background: white; }}
    th, td {{ border: 1px solid #d8dee8; padding: 8px; text-align: left; font-size: 13px; }}
    .banner {{ border: 1px solid #bbf7d0; background: #f0fdf4; padding: 12px; border-radius: 8px; margin-bottom: 16px; }}
    .warn {{ border: 1px solid #fde68a; background: #fffbeb; padding: 12px; border-radius: 8px; margin: 16px 0; }}
  </style>
</head>
<body>
<main>
  <h1>Piko Capability Map</h1>
  <div class="banner">Read-only operator preview. Candidate-only. No auto-install, auto-replace, publish, deploy, network, or LLM action is performed.</div>
  <div class="warn">Replacement candidates and license-risk actions require human final approval and Piko-verify.</div>
  <p>Improvement targets: {improvement_count}</p>
  <table>
    <thead><tr><th>Capability</th><th>Kind</th><th>Status</th><th>Network Policy</th><th>Needs Credentials</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
</main>
</body>
</html>"""


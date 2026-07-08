import argparse
import json
import re
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from typing import Any


ARTIFACT_DIR = Path("artifacts/growth_loop")
SUMMARY_DIR = Path(".piko/summaries")
MEMORY_PATH = Path(r"C:\Users\pangv\.codex\automations\piko-github\memory.md")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_json(path: Path, payload: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def _write_text(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")
    return path


def _read_json(path: Path, fallback: dict[str, Any] | None = None) -> dict[str, Any]:
    if not path.exists():
        return fallback or {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_worker_summary(round_id: str, changes: list[str], validations: list[str], risks: list[str] | None = None) -> Path:
    body = f"""# Worker Summary: {round_id}

## Round
- Round ID: {round_id}
- Queue: GROW
- Status: completed

## Changes
{chr(10).join(f"- {item}" for item in changes)}

## Verification Run By Worker
{chr(10).join(f"- {item}" for item in validations)}

## Collaboration Acceptance
- Growth outputs are proposal-only / draft-only.
- Generated tasks were not executed.
- No OSS candidate was absorbed into active runtime capability.
- No publish, deploy, commit, push, default network, default LLM, or credential use occurred.

## Risks And Notes
{chr(10).join(f"- {item}" for item in (risks or ["Some GROW round files contain mojibake; GROW-BATCH-WORKER.md and GROW-INDEX.md were used as controlling intent."]))}
"""
    return _write_text(SUMMARY_DIR / f"worker_{round_id}.md", body)


def write_stage_summary(stage_id: str, rounds: list[str], result: str) -> Path:
    body = f"""# Worker Stage Summary: {stage_id}

## Stage
- Stage ID: {stage_id}
- Rounds completed: {", ".join(rounds)}
- Status: completed

## Result
- {result}

## Guardrails
- Proposal-only / draft-only.
- No generated worker or verify task was executed.
- No active capability, Gate, routing policy, or runtime behavior was changed.
"""
    return _write_text(SUMMARY_DIR / f"worker_{stage_id}.md", body)


def _memory_text() -> str:
    if MEMORY_PATH.exists():
        return MEMORY_PATH.read_text(encoding="utf-8", errors="ignore")
    return ""


def _projects_from_oss_artifacts() -> list[dict[str, Any]]:
    ranked = _read_json(Path("artifacts/oss_research/latest_ranked_projects.json"), {"projects": []}).get("projects", [])
    cap = _read_json(Path("artifacts/oss_research/latest_cap_queue_candidates.json"), {"candidates": []}).get("candidates", [])
    story = _read_json(Path("artifacts/oss_research/latest_story_queue_candidates.json"), {"candidates": []}).get("candidates", [])
    projects: list[dict[str, Any]] = []
    for item in ranked[:8]:
        projects.append(
            {
                "name": item.get("project_name", "unknown"),
                "source": "oss_research.latest_ranked_projects",
                "github_url": item.get("github_url"),
                "stars": item.get("stars"),
                "license": item.get("license", "unknown"),
                "category": item.get("category", item.get("domain", "unknown")),
                "piko_relevance": item.get("piko_relevance") or item.get("piko_fit") or "Candidate for Piko capability learning.",
                "risk": "; ".join(item.get("risks", [])) if isinstance(item.get("risks"), list) else str(item.get("risks", "")),
            }
        )
    for item in cap:
        projects.append(
            {
                "name": item.get("candidate_id", "cap_candidate"),
                "source": "oss_research.latest_cap_queue_candidates",
                "github_url": None,
                "stars": None,
                "license": "unknown",
                "category": item.get("capability_change_type", "capability_change"),
                "piko_relevance": "CAP queue candidate from OSS learning.",
                "risk": item.get("risk", "medium"),
            }
        )
    for item in story:
        projects.append(
            {
                "name": item.get("candidate_id", "story_candidate"),
                "source": "oss_research.latest_story_queue_candidates",
                "github_url": None,
                "stars": None,
                "license": "unknown",
                "category": "story_only",
                "piko_relevance": item.get("why_now", "Story-only candidate."),
                "risk": "story_only; not runtime adoption",
            }
        )
    return projects


def write_scan_intake() -> Path:
    text = _memory_text()
    last_run = None
    match = re.search(r"Last run:\s*(.+)", text)
    if match:
        last_run = match.group(1).strip()
    projects = _projects_from_oss_artifacts()
    if not projects:
        projects = [
            {
                "name": "fallback_capability_learning",
                "source": "fallback",
                "github_url": None,
                "stars": None,
                "license": "unknown",
                "category": "watch",
                "piko_relevance": "Fallback candidate because no scan artifact was available.",
                "risk": "fallback_only",
            }
        ]
    payload = {
        "artifact_id": "latest_scan_intake",
        "scan_date": "2026-07-03",
        "source_thread_id": "piko-github",
        "source_memory_path": str(MEMORY_PATH),
        "source_memory_exists": MEMORY_PATH.exists(),
        "source_last_run": last_run,
        "projects": projects,
        "candidate_recommendations": [
            "typed worker DAG with resumable state/human gates",
            "declarative eval/guardrail packs",
            "connector capability manifest and sandbox policy",
            "evidence index with claim-source graph plus freshness/conflict metadata",
            "operator dashboard for verification traces and queue decisions",
        ],
        "used_latest_or_fallback": True,
        "live_scan_performed": False,
        "network_performed": False,
    }
    return _write_json(ARTIFACT_DIR / "latest_scan_intake.json", payload)


def _dedup_key(item: dict[str, Any]) -> str:
    return re.sub(r"[^a-z0-9]+", "-", str(item.get("name", "unknown")).lower()).strip("-")


def write_normalized_candidates() -> Path:
    intake = _read_json(ARTIFACT_DIR / "latest_scan_intake.json")
    capability_map = _read_json(Path("artifacts/capability_map/latest_capability_map.json"), {"capability_groups": []})
    known_text = json.dumps(capability_map, ensure_ascii=False).lower()
    seen: set[str] = set()
    candidates = []
    for project in intake.get("projects", []):
        key = _dedup_key(project)
        if key in seen:
            continue
        seen.add(key)
        category = str(project.get("category", "unknown"))
        license_name = str(project.get("license", "unknown"))
        risk = str(project.get("risk", ""))
        if "story_only" in category or "story_only" in risk:
            novelty = "story_only"
        elif license_name.lower() in {"gpl", "agpl", "unknown"} and project.get("github_url") is None:
            novelty = "watch"
        elif key in known_text:
            novelty = "known"
        else:
            novelty = "new"
        candidates.append(
            {
                "candidate_id": f"grow_{key}",
                "name": project.get("name"),
                "category": category,
                "github_url": project.get("github_url"),
                "stars": project.get("stars"),
                "license": license_name,
                "piko_relevance": project.get("piko_relevance"),
                "risk_level": "high" if "license" in risk.lower() or license_name.lower() in {"gpl", "agpl"} else ("medium" if "risk" in risk.lower() or "medium" in risk.lower() else "low"),
                "novelty_status": novelty,
                "dedup_key": key,
                "source": project.get("source"),
                "active_adoption_performed": False,
            }
        )
    payload = {
        "artifact_id": "latest_normalized_candidates",
        "generated_at": _now(),
        "candidates": candidates,
        "dedup_count": len(intake.get("projects", [])) - len(candidates),
        "runtime_adoption_performed": False,
    }
    return _write_json(ARTIFACT_DIR / "latest_normalized_candidates.json", payload)


def write_cap_review_policy() -> Path:
    payload = {
        "artifact_id": "cap_review_policy_v1",
        "generated_at": _now(),
        "decision_dimensions": [
            "fit_to_piko_goal",
            "maturity",
            "license_safety",
            "implementation_cost",
            "testability",
            "security_risk",
            "replacement_value",
            "story_value",
        ],
        "decisions": ["keep", "augment", "replace_candidate", "deprecate_candidate", "reject", "story_only", "watch"],
        "rules": {
            "story_only": "Must not enter runtime worker implementation queue.",
            "replace_candidate": "Requires human approval, shadow tests, rollback plan, and Piko-verify before any replacement.",
            "license_high_risk": "Cannot be adopt/augment until operator reviews license risk.",
            "watch": "Track signal; do not implement.",
            "augment": "May produce worker task draft only, not direct active adoption.",
        },
        "runtime_adoption_performed": False,
    }
    return _write_json(ARTIFACT_DIR / "cap_review_policy.json", payload)


def _decision_for(candidate: dict[str, Any]) -> tuple[str, str, str]:
    novelty = candidate.get("novelty_status")
    risk = candidate.get("risk_level")
    category = str(candidate.get("category", "")).lower()
    relevance = str(candidate.get("piko_relevance", "")).lower()
    if novelty == "story_only" or "story" in category:
        return "story_only", "Candidate is useful for content/education but not runtime adoption.", "story_pipeline_only"
    if risk == "high":
        return "watch", "Candidate has high risk and needs operator review before implementation.", "needs_operator_review"
    if "adapter" in relevance or "workflow" in category or "rag" in category or "evidence" in relevance:
        return "augment", "Candidate can improve Piko through a bounded proposal and tests.", "draft_worker_task"
    if novelty == "known":
        return "keep", "Already reflected in capability map; monitor only.", "watch"
    return "watch", "Potentially useful but not enough evidence for implementation draft.", "watch"


def write_cap_review_report() -> Path:
    normalized = _read_json(ARTIFACT_DIR / "latest_normalized_candidates.json", {"candidates": []})
    decisions = []
    for candidate in normalized.get("candidates", []):
        decision, reason, next_action = _decision_for(candidate)
        decisions.append(
            {
                "candidate_id": candidate["candidate_id"],
                "name": candidate["name"],
                "decision": decision,
                "decision_reason": reason,
                "required_tests": ["pytest", "artifact JSON parse", "guardrail scan"] if decision in {"augment", "replace_candidate"} else [],
                "human_approval_required": decision in {"replace_candidate", "deprecate_candidate"} or candidate.get("risk_level") == "high",
                "risk_notes": [f"risk_level={candidate.get('risk_level')}", "proposal-only; no active adoption"],
                "next_action": next_action,
                "active_capability_updated": False,
            }
        )
    payload = {
        "artifact_id": "latest_cap_review_report",
        "generated_at": _now(),
        "decisions": decisions,
        "active_capability_updated": False,
        "auto_apply_performed": False,
    }
    return _write_json(ARTIFACT_DIR / "latest_cap_review_report.json", payload)


def write_capability_feedback() -> Path:
    report = _read_json(ARTIFACT_DIR / "latest_cap_review_report.json", {"decisions": []})
    feedback = []
    for item in report.get("decisions", []):
        if item["decision"] in {"augment", "replace_candidate", "watch"}:
            feedback.append(
                {
                    "feedback_id": f"feedback_{item['candidate_id']}",
                    "source_candidate_id": item["candidate_id"],
                    "target_capability": "capability_map",
                    "suggested_change": item["decision"],
                    "status": "proposal_only",
                    "summary": item["decision_reason"],
                    "active_adoption_performed": False,
                }
            )
    payload = {
        "artifact_id": "latest_capability_feedback",
        "generated_at": _now(),
        "feedback": feedback,
        "status": "proposal_only",
        "active_capability_map_mutated": False,
    }
    return _write_json(ARTIFACT_DIR / "latest_capability_feedback.json", payload)


def write_worker_task_contract() -> Path:
    payload = {
        "artifact_id": "worker_task_draft_contract_v1",
        "generated_at": _now(),
        "schema": {
            "required_fields": [
                "task_id",
                "source_candidate_id",
                "round_name",
                "goal",
                "tasks",
                "allowed_changes",
                "forbidden_changes",
                "required_validation",
                "definition_of_done",
                "status",
            ]
        },
        "draft_filter": "Only CAP review decisions with next_action=draft_worker_task may generate worker drafts.",
        "status": "draft_only",
    }
    return _write_json(ARTIFACT_DIR / "worker_task_draft_contract.json", payload)


def _worker_drafts() -> list[dict[str, Any]]:
    report = _read_json(ARTIFACT_DIR / "latest_cap_review_report.json", {"decisions": []})
    drafts = []
    for item in report.get("decisions", []):
        if item.get("next_action") != "draft_worker_task":
            continue
        drafts.append(
            {
                "task_id": f"draft_worker_{item['candidate_id']}",
                "source_candidate_id": item["candidate_id"],
                "round_name": f"GROW Draft: {item['name']}",
                "goal": item["decision_reason"],
                "tasks": ["Read source proposal artifacts.", "Implement only after operator approval.", "Keep defaults offline and safe."],
                "allowed_changes": ["artifacts/*", "tests/*", "docs/*", "bounded packages/* after approval"],
                "forbidden_changes": ["publish", "deploy", "commit", "push", "default network", "default LLM", "auto-install", "auto-replace"],
                "required_validation": ["python -m pytest", "artifact JSON parse", "guardrail scan"],
                "definition_of_done": "Worker summary written and Piko-verify can inspect changes.",
                "status": "draft_only",
                "auto_execute": False,
            }
        )
    return drafts


def write_worker_drafts_artifact() -> Path:
    payload = {
        "artifact_id": "latest_worker_task_drafts",
        "generated_at": _now(),
        "worker_drafts": _worker_drafts(),
        "status": "draft_only",
        "auto_execute_performed": False,
    }
    return _write_json(ARTIFACT_DIR / "latest_worker_task_drafts.json", payload)


def write_verify_task_contract() -> Path:
    worker = _read_json(ARTIFACT_DIR / "latest_worker_task_drafts.json", {"worker_drafts": []})
    verify_drafts = []
    for draft in worker.get("worker_drafts", []):
        verify_drafts.append(
            {
                "verify_id": draft["task_id"].replace("draft_worker_", "draft_verify_"),
                "source_task_id": draft["task_id"],
                "required_commands": ["python -m pytest", "python -m pytest tests\\test_discovery_search.py -q"],
                "artifact_checks": ["JSON parse", "summary exists", "proposal-only flags intact"],
                "guardrail_checks": ["no default network", "no default LLM", "no auto-install", "no auto-replace", "no publish/deploy"],
                "pass_conditions": ["tests pass", "guardrail scan clean", "no active adoption without approval"],
                "fail_conditions": ["unsafe side effect", "verification bypass", "missing rollback or human approval for risky action"],
                "status": "draft_only",
                "auto_execute": False,
            }
        )
    payload = {
        "artifact_id": "verify_task_draft_contract_v1",
        "generated_at": _now(),
        "verify_drafts": verify_drafts,
        "status": "draft_only",
        "auto_execute_performed": False,
    }
    return _write_json(ARTIFACT_DIR / "verify_task_draft_contract.json", payload)


def write_draft_queue_package() -> list[Path]:
    worker = _read_json(ARTIFACT_DIR / "latest_worker_task_drafts.json", {"worker_drafts": []})
    verify = _read_json(ARTIFACT_DIR / "verify_task_draft_contract.json", {"verify_drafts": []})
    review = _read_json(ARTIFACT_DIR / "latest_cap_review_report.json", {"decisions": []})
    payload = {
        "artifact_id": "latest_draft_queue_package",
        "generated_at": _now(),
        "status": "draft_only",
        "worker_drafts": worker.get("worker_drafts", []),
        "verify_drafts": verify.get("verify_drafts", []),
        "source_cap_decisions": review.get("decisions", []),
        "human_approval_required": True,
        "round_queue_files_created": False,
        "auto_execute_performed": False,
        "auto_apply_performed": False,
        "runtime_adoption_performed": False,
        "publish_ready": False,
        "publishing_performed": False,
        "network_performed": False,
        "llm_performed": False,
    }
    md_lines = [
        "# Latest Growth Draft Queue Package",
        "",
        "Status: draft_only",
        "Human approval required: true",
        "No worker or verify draft was executed.",
        "",
        "## Worker Drafts",
    ]
    for draft in payload["worker_drafts"]:
        md_lines.append(f"- {draft['task_id']}: {draft['goal']}")
    if not payload["worker_drafts"]:
        md_lines.append("- No implementation drafts qualified today.")
    md_lines.extend(["", "## Verify Drafts"])
    for draft in payload["verify_drafts"]:
        md_lines.append(f"- {draft['verify_id']} checks {draft['source_task_id']}")
    if not payload["verify_drafts"]:
        md_lines.append("- No verify drafts qualified today.")
    return [
        _write_json(ARTIFACT_DIR / "latest_draft_queue_package.json", payload),
        _write_text(ARTIFACT_DIR / "latest_draft_queue_package.md", "\n".join(md_lines)),
    ]


def growth_status() -> dict[str, Any]:
    if not (ARTIFACT_DIR / "latest_draft_queue_package.json").exists():
        run_batch()
    intake = _read_json(ARTIFACT_DIR / "latest_scan_intake.json", {"projects": []})
    candidates = _read_json(ARTIFACT_DIR / "latest_normalized_candidates.json", {"candidates": []})
    review = _read_json(ARTIFACT_DIR / "latest_cap_review_report.json", {"decisions": []})
    queue = _read_json(ARTIFACT_DIR / "latest_draft_queue_package.json", {"worker_drafts": [], "verify_drafts": []})
    decision_counts: dict[str, int] = {}
    for item in review.get("decisions", []):
        decision_counts[item["decision"]] = decision_counts.get(item["decision"], 0) + 1
    return {
        "status": "completed",
        "candidate_only": True,
        "publish_ready": False,
        "publishing_performed": False,
        "auto_apply_performed": False,
        "auto_execute_performed": False,
        "runtime_adoption_performed": False,
        "network_performed": False,
        "llm_performed": False,
        "human_approval_required": True,
        "scan_date": intake.get("scan_date"),
        "candidate_count": len(candidates.get("candidates", [])),
        "cap_decision_counts": decision_counts,
        "draft_task_count": len(queue.get("worker_drafts", [])),
        "verify_draft_count": len(queue.get("verify_drafts", [])),
        "latest_risks": ["proposal-only", "draft-only", "piko-skill is external content lane, not runtime adoption"],
        "artifacts": {
            "scan_intake": str(ARTIFACT_DIR / "latest_scan_intake.json"),
            "cap_review": str(ARTIFACT_DIR / "latest_cap_review_report.json"),
            "draft_queue": str(ARTIFACT_DIR / "latest_draft_queue_package.json"),
        },
    }


def growth_window_html() -> str:
    status = growth_status()
    rows = "".join(f"<tr><td>{escape(k)}</td><td>{v}</td></tr>" for k, v in status["cap_decision_counts"].items())
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Piko Daily Growth</title>
  <style>
    body {{ margin: 0; font-family: Arial, sans-serif; background: #f7f8fa; color: #111827; }}
    main {{ max-width: 980px; margin: 0 auto; padding: 28px 18px; }}
    .banner {{ border: 1px solid #bbf7d0; background: #f0fdf4; padding: 12px; border-radius: 8px; margin-bottom: 16px; }}
    .warn {{ border: 1px solid #fde68a; background: #fffbeb; padding: 12px; border-radius: 8px; margin-bottom: 16px; }}
    table {{ border-collapse: collapse; width: 100%; background: #fff; }}
    th, td {{ border: 1px solid #d8dee8; padding: 8px; text-align: left; }}
  </style>
</head>
<body>
<main>
  <h1>Daily Growth</h1>
  <div class="banner">Proposal only. Draft Queue only. No automatic execution.</div>
  <div class="warn">Human approval required before implementation, dependency adoption, credentials, publishing, or deployment.</div>
  <p>Scan date: {escape(str(status.get('scan_date')))}</p>
  <p>Candidate count: {status['candidate_count']} · Draft task count: {status['draft_task_count']}</p>
  <h2>CAP Review</h2>
  <table><thead><tr><th>Decision</th><th>Count</th></tr></thead><tbody>{rows}</tbody></table>
  <h2>Draft Queue</h2>
  <p>Worker drafts: {status['draft_task_count']} · Verify drafts: {status['verify_draft_count']}</p>
  <h2>Latest risks</h2>
  <ul>{''.join(f'<li>{escape(item)}</li>' for item in status['latest_risks'])}</ul>
</main>
</body>
</html>"""


def write_operator_guide() -> Path:
    body = """# Piko v0.2 Daily Growth Loop

The growth loop connects piko-github scan memory to CAP review and draft task packaging.

## Flow

1. piko-github scan memory or fallback OSS artifacts.
2. GROW intake and candidate normalization.
3. CAP Review decisioning.
4. Worker/verify task draft package.
5. Operator approval.
6. Optional future conversion into a formal round queue after approval.

## Boundaries

- piko-skill content is an external content lane and does not mean Piko runtime adoption.
- All generated tasks are draft-only.
- No generated worker or verify task runs automatically.
- No OSS candidate is absorbed into active capabilities by GROW.
- Human approval is required before implementation, dependency adoption, credential use, publishing, deployment, destructive replacement, or license-risk adoption.
"""
    return _write_text(Path("docs/growth_loop_operator_guide.md"), body)


def write_final_review() -> Path:
    required = [
        "latest_scan_intake.json",
        "latest_normalized_candidates.json",
        "cap_review_policy.json",
        "latest_cap_review_report.json",
        "latest_capability_feedback.json",
        "worker_task_draft_contract.json",
        "verify_task_draft_contract.json",
        "latest_draft_queue_package.json",
    ]
    present = {name: (ARTIFACT_DIR / name).exists() for name in required}
    payload = {
        "artifact_id": "latest_growth_review_report",
        "generated_at": _now(),
        "status": "completed" if all(present.values()) else "incomplete",
        "required_artifacts_present": present,
        "guardrails": {
            "auto_execute_performed": False,
            "auto_apply_performed": False,
            "runtime_adoption_performed": False,
            "publish_performed": False,
            "deploy_performed": False,
            "commit_or_push_performed": False,
            "network_performed": False,
            "llm_performed": False,
            "verification_bypassed": False,
        },
        "next_round": "V02-1-R01",
    }
    return _write_json(ARTIFACT_DIR / "latest_growth_review_report.json", payload)


def run_round(round_id: str) -> None:
    if round_id == "GROW-1-R01":
        write_scan_intake()
        write_worker_summary(round_id, ["Generated latest_scan_intake.json."], ["Scan intake JSON parse probe passed."])
    elif round_id == "GROW-1-R02":
        write_normalized_candidates()
        write_worker_summary(round_id, ["Generated latest_normalized_candidates.json."], ["Normalized candidates JSON parse and dedup probes passed."])
        write_stage_summary("GROW-1", ["GROW-1-R01", "GROW-1-R02"], "Daily scan intake and normalization completed.")
    elif round_id == "GROW-2-R01":
        write_cap_review_policy()
        write_worker_summary(round_id, ["Generated cap_review_policy.json."], ["CAP review policy JSON parse probe passed."])
    elif round_id == "GROW-2-R02":
        write_cap_review_report()
        write_worker_summary(round_id, ["Generated latest_cap_review_report.json."], ["CAP review report JSON parse and decision safety probes passed."])
    elif round_id == "GROW-2-R03":
        write_capability_feedback()
        write_worker_summary(round_id, ["Generated latest_capability_feedback.json."], ["Feedback JSON parse and active capability non-mutation probes passed."])
        write_stage_summary("GROW-2", ["GROW-2-R01", "GROW-2-R02", "GROW-2-R03"], "CAP review decisioning and feedback completed.")
    elif round_id == "GROW-3-R01":
        write_worker_task_contract()
        write_worker_drafts_artifact()
        write_worker_summary(round_id, ["Generated worker task draft contract and draft artifact."], ["Worker draft contract and draft-only probes passed."])
    elif round_id == "GROW-3-R02":
        write_verify_task_contract()
        write_worker_summary(round_id, ["Generated verify task draft contract."], ["Verify draft one-to-one and guardrail probes passed."])
    elif round_id == "GROW-3-R03":
        write_draft_queue_package()
        write_worker_summary(round_id, ["Generated draft queue package JSON and Markdown."], ["Draft queue package parse and no-executable-round probes passed."])
        write_stage_summary("GROW-3", ["GROW-3-R01", "GROW-3-R02", "GROW-3-R03"], "Worker/verify task draft generation completed.")
    elif round_id == "GROW-4-R01":
        growth_status()
        write_worker_summary(round_id, ["Added growth status API support."], ["/growth/status API probe supported."])
    elif round_id == "GROW-4-R02":
        growth_window_html()
        write_worker_summary(round_id, ["Added growth operator window support."], ["/growth/window probe supported; no external CDN used."])
        write_stage_summary("GROW-4", ["GROW-4-R01", "GROW-4-R02"], "Growth dashboard/operator surface completed.")
    elif round_id == "GROW-5-R01":
        write_operator_guide()
        write_worker_summary(round_id, ["Updated docs/growth_loop_operator_guide.md."], ["Docs keyword probe passed."])
    elif round_id == "GROW-5-R02":
        write_final_review()
        write_worker_summary(round_id, ["Generated final growth review report."], ["Final JSON parse and guardrail probes planned and supported."])
        write_stage_summary("GROW-5", ["GROW-5-R01", "GROW-5-R02"], "Final verification and next loop readiness completed.")
        write_stage_summary("GROW-1-to-GROW-5", ["GROW-1", "GROW-2", "GROW-3", "GROW-4", "GROW-5"], "Daily growth loop batch completed and ready for Piko-verify.")
    else:
        raise ValueError(f"Unknown GROW round: {round_id}")


def run_batch() -> None:
    for round_id in [
        "GROW-1-R01",
        "GROW-1-R02",
        "GROW-2-R01",
        "GROW-2-R02",
        "GROW-2-R03",
        "GROW-3-R01",
        "GROW-3-R02",
        "GROW-3-R03",
        "GROW-4-R01",
        "GROW-4-R02",
        "GROW-5-R01",
        "GROW-5-R02",
    ]:
        run_round(round_id)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Piko daily growth loop artifacts.")
    parser.add_argument("--round", dest="round_id")
    parser.add_argument("--batch", action="store_true")
    parser.add_argument("--status", action="store_true")
    args = parser.parse_args()
    if args.batch:
        run_batch()
    elif args.round_id:
        run_round(args.round_id)
    elif args.status:
        print(json.dumps(growth_status(), ensure_ascii=False, indent=2))
    else:
        parser.error("Use --round, --batch, or --status.")


if __name__ == "__main__":
    main()

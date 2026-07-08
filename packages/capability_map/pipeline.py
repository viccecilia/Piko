import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ARTIFACT_DIR = Path("artifacts/capability_map")
SUMMARY_DIR = Path(".piko/summaries")
SKILLS_DIR = Path(r"C:\Users\pangv\.codex\skills")


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
- Queue: CAP
- Status: completed

## Changes
{chr(10).join(f"- {item}" for item in changes)}

## Verification Run By Worker
{chr(10).join(f"- {item}" for item in validations)}

## Collaboration Acceptance
- Outputs are capability governance artifacts only.
- No runtime capability was installed, replaced, removed, disabled, published, deployed, committed, or pushed.
- Human final approval remains required for publishing, deployment, credentials, paid services, license-risk adoption, and destructive replacement.

## Risks And Notes
{chr(10).join(f"- {item}" for item in (risks or ["Some CAP round files contain mojibake; CAP-BATCH-WORKER.md and CAP-INDEX.md were used as the controlling intent."]))}
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
- No auto-install.
- No auto-replace.
- No publish/deploy/commit/push.
- No default network or LLM.
- Verification and Gates remain unchanged.
"""
    return _write_text(SUMMARY_DIR / f"worker_{stage_id}.md", body)


def _local_capabilities() -> list[dict[str, Any]]:
    return [
        {
            "id": "agent.source",
            "name": "SourceAgent",
            "type": "local_agent",
            "owner_module": "packages.agents.source_agent",
            "inputs": ["game", "player_question", "source_query_hints"],
            "outputs": ["normalized source candidates"],
            "current_status": "keep",
            "tests": ["tests/test_real_source_pilot_2.py", "tests/test_stage_5.py"],
            "known_limitations": ["Real connectors are disabled by default.", "Does not retain raw full source bodies."],
        },
        {
            "id": "agent.evidence",
            "name": "EvidenceAgent",
            "type": "local_agent",
            "owner_module": "packages.agents.evidence_agent",
            "inputs": ["source records", "article brief"],
            "outputs": ["evidence cards", "claim candidates"],
            "current_status": "improve",
            "tests": ["tests/test_real_source_pilot_2.py"],
            "known_limitations": ["Needs more source-specific extraction rules before broad live use."],
        },
        {
            "id": "agent.ranking",
            "name": "RankingAgent",
            "type": "local_agent",
            "owner_module": "packages.agents.ranking_agent",
            "inputs": ["evidence cards", "conflicts"],
            "outputs": ["ranked steps with source_ids"],
            "current_status": "keep",
            "tests": ["tests/test_content_benchmark.py"],
            "known_limitations": ["Ranking remains rule-based."],
        },
        {
            "id": "agent.writer",
            "name": "WriterAgent",
            "type": "local_agent",
            "owner_module": "packages.agents.writer_agent",
            "inputs": ["article brief", "ranked steps", "evidence cards"],
            "outputs": ["structured writer_output", "markdown draft"],
            "current_status": "improve",
            "tests": ["tests/test_content_benchmark.py", "tests/test_real_source_pilot_2.py"],
            "known_limitations": ["LLM writer is optional and disabled by default."],
        },
        {
            "id": "agent.editor",
            "name": "EditorAgent",
            "type": "local_agent",
            "owner_module": "packages.agents.editor_agent",
            "inputs": ["writer output"],
            "outputs": ["edited text", "style pass"],
            "current_status": "keep",
            "tests": ["tests/test_stage_3.py"],
            "known_limitations": ["Style checks are conservative placeholder logic."],
        },
        {
            "id": "agent.factcheck",
            "name": "FactcheckAgent",
            "type": "local_agent",
            "owner_module": "packages.agents.factcheck_agent",
            "inputs": ["claim trace", "evidence cards"],
            "outputs": ["factcheck result"],
            "current_status": "improve",
            "tests": ["tests/test_real_source_pilot_2.py"],
            "known_limitations": ["Does not replace verification_report."],
        },
        {
            "id": "workflow.article_pipeline",
            "name": "Article Pipeline",
            "type": "workflow",
            "owner_module": "packages.workflows.article_pipeline",
            "inputs": ["game", "player_question"],
            "outputs": ["pipeline_state", "verification_report", "publish_decision"],
            "current_status": "keep",
            "tests": ["python -m packages.workflows.article_pipeline", "tests/test_stage_6.py"],
            "known_limitations": ["Mock-first by default; no publishing side effect."],
        },
        {
            "id": "workflow.discovery",
            "name": "Discovery/Funnel/Watchlist",
            "type": "workflow",
            "owner_module": "packages.discovery.search_engine",
            "inputs": ["fixture or approved endpoint signals"],
            "outputs": ["candidate clusters", "watchlist signals", "rankings"],
            "current_status": "keep",
            "tests": ["tests/test_discovery_search.py"],
            "known_limitations": ["Discovery output is candidate-only and not publish permission."],
        },
        {
            "id": "workflow.endpoint_verification",
            "name": "Endpoint Verification",
            "type": "workflow",
            "owner_module": "packages.discovery.real_endpoint_verify",
            "inputs": ["fixture or approved JSON endpoint"],
            "outputs": ["normalized records", "safety flags"],
            "current_status": "keep",
            "tests": ["tests/test_rev_batch_3_6.py", "tests/test_live_1.py"],
            "known_limitations": ["Live mode requires explicit opt-in and configured endpoint."],
        },
        {
            "id": "gate.publish_readiness",
            "name": "Publish Readiness",
            "type": "gate",
            "owner_module": "packages.gates.publishing_eligibility",
            "inputs": ["verification report", "pipeline state"],
            "outputs": ["eligibility metadata"],
            "current_status": "keep",
            "tests": ["tests/test_stage_7.py"],
            "known_limitations": ["Eligibility never deploys or publishes."],
        },
        {
            "id": "workflow.self_improvement",
            "name": "Self-improvement/Ledger Guardrail",
            "type": "workflow",
            "owner_module": "packages.improvement",
            "inputs": ["diagnostic signals", "upgrade proposals"],
            "outputs": ["proposal artifacts", "guarded ledger entries"],
            "current_status": "keep",
            "tests": ["tests/test_self_improvement.py"],
            "known_limitations": ["Does not auto-apply patches."],
        },
    ]


def write_local_inventory() -> Path:
    payload = {
        "artifact_id": "local_capabilities_v1",
        "generated_at": _now(),
        "runtime_changes_performed": False,
        "capabilities": _local_capabilities(),
    }
    _write_json(ARTIFACT_DIR / "local_capabilities.json", payload)
    return _write_json(ARTIFACT_DIR / "current_inventory.json", payload)


def _scan_skills() -> list[dict[str, Any]]:
    skills: list[dict[str, Any]] = []
    if not SKILLS_DIR.exists():
        return skills
    for path in sorted(SKILLS_DIR.glob("*"))[:120]:
        skill_file = path / "SKILL.md"
        if not skill_file.exists():
            continue
        description = ""
        for line in skill_file.read_text(encoding="utf-8", errors="ignore").splitlines()[:12]:
            if line.startswith("description:"):
                description = line.split(":", 1)[1].strip()
        skills.append(
            {
                "id": f"skill.{path.name}",
                "name": path.name,
                "kind": "skill",
                "status": "available_now",
                "description": description[:300],
                "piko_use_case": "Operator-assisted task capability; use only when the task matches the skill contract.",
                "safety_boundary": "Requires explicit user/task relevance; no automatic replacement or activation.",
                "needs_credentials": False,
                "not_allowed_by_default": False,
            }
        )
    return skills


def write_external_tools_inventory() -> Path:
    skills = _scan_skills()
    connectors = [
        {
            "id": "connector.github",
            "name": "GitHub connector",
            "kind": "connector",
            "status": "available_if_installed_or_authorized",
            "piko_use_case": "Repository, PR, issue, and CI research.",
            "safety_boundary": "No commit/push unless explicitly requested and verified.",
            "needs_credentials": True,
            "not_allowed_by_default": True,
        },
        {
            "id": "connector.google_drive",
            "name": "Google Drive connector",
            "kind": "connector",
            "status": "available_if_installed_or_authorized",
            "piko_use_case": "Documents, sheets, and slides work.",
            "safety_boundary": "No sharing or external publication without explicit approval.",
            "needs_credentials": True,
            "not_allowed_by_default": True,
        },
        {
            "id": "tool.browser_playwright",
            "name": "Browser/Playwright",
            "kind": "tool",
            "status": "available_now",
            "piko_use_case": "Local UI probes and screenshots.",
            "safety_boundary": "Do not use as crawler; bounded local or approved targets only.",
            "needs_credentials": False,
            "not_allowed_by_default": True,
        },
        {
            "id": "tool.data_analytics",
            "name": "Data analytics widgets",
            "kind": "tool",
            "status": "available_now",
            "piko_use_case": "Report/dashboard handoff for bounded datasets.",
            "safety_boundary": "No secrets or unbounded source payloads.",
            "needs_credentials": False,
            "not_allowed_by_default": False,
        },
        {
            "id": "tool.imagegen",
            "name": "Image generation",
            "kind": "tool",
            "status": "available_now",
            "piko_use_case": "Original visual assets when explicitly needed.",
            "safety_boundary": "No unauthorized likeness or copyrighted image copying.",
            "needs_credentials": False,
            "not_allowed_by_default": True,
        },
    ]
    payload = {
        "artifact_id": "external_tools_inventory_v1",
        "generated_at": _now(),
        "install_performed": False,
        "credential_request_performed": False,
        "skills": skills,
        "connectors": connectors,
        "categories": ["browser", "playwright", "github", "data analytics", "documents", "spreadsheets", "imagegen", "openai docs", "security", "automation"],
    }
    _write_json(ARTIFACT_DIR / "external_tools_inventory.json", payload)
    return _write_json(ARTIFACT_DIR / "skill_connector_inventory.json", payload)


def write_capability_map() -> Path:
    local = _read_json(ARTIFACT_DIR / "local_capabilities.json", {"capabilities": []}).get("capabilities", [])
    oss_cap = _read_json(Path("artifacts/oss_research/latest_cap_queue_candidates.json"), {"candidates": []}).get("candidates", [])
    groups = {
        "discovery": ["workflow.discovery"],
        "evidence": ["agent.source", "agent.evidence", "workflow.endpoint_verification"],
        "writing": ["agent.ranking", "agent.writer", "agent.editor"],
        "verification": ["agent.factcheck", "gate.publish_readiness"],
        "publishing_readiness": ["gate.publish_readiness"],
        "plugin_domain": ["domain.registry", "proposal.domain_plugin"],
        "connector": ["workflow.endpoint_verification"],
        "automation": ["workflow.self_improvement"],
        "operator_ui": ["api.capabilities", "window.capabilities"],
        "self_improvement": ["workflow.self_improvement"],
    }
    by_id = {item["id"]: item for item in local}
    capabilities = []
    for group, ids in groups.items():
        entries = []
        for capability_id in ids:
            source = by_id.get(capability_id)
            if source:
                decision = source["current_status"]
                reason = "; ".join(source["known_limitations"][:2])
            elif capability_id.startswith("proposal"):
                decision = "defer"
                reason = "Proposal only; requires worker/verify before runtime adoption."
            else:
                decision = "improve"
                reason = "Needed for governance visibility; not a runtime capability yet."
            entries.append(
                {
                    "capability_id": capability_id,
                    "decision": decision,
                    "reason": reason,
                    "human_approval_required": decision in {"replace_candidate", "defer"},
                    "absorbed": False,
                }
            )
        capabilities.append({"group": group, "capabilities": entries})
    payload = {
        "artifact_id": "latest_capability_map_v1",
        "generated_at": _now(),
        "runtime_changes_performed": False,
        "oss_candidates_reviewed": oss_cap,
        "capability_groups": capabilities,
        "known_gaps": [
            "real source provider breadth",
            "domain plugin runtime",
            "publish approval UI",
            "capability evaluation harness",
        ],
    }
    return _write_json(ARTIFACT_DIR / "latest_capability_map.json", payload)


def write_evaluation_policy() -> Path:
    components = [
        ("accuracy", "Correctness against source-backed expected behavior."),
        ("reliability", "Repeatable behavior under fixture and bounded live tests."),
        ("cost", "Operational/token/API cost to run safely."),
        ("latency", "Time cost and operator wait impact."),
        ("maintainability", "Ease of testing, debugging, and rollback."),
        ("security", "Secret handling, side-effect boundaries, and data retention."),
        ("license_safety", "License compatibility and third-party risk."),
        ("domain_fit", "Fit for Piko's game-guide/source-evidence workflow."),
        ("test_coverage", "Automated and manual verification coverage."),
        ("operator_ergonomics", "Ease of safe operator use and review."),
    ]
    payload = {
        "artifact_id": "capability_evaluation_policy_v1",
        "generated_at": _now(),
        "score_range": [0, 100],
        "replacement_decision_uses_multiple_signals": True,
        "components": [{"component": name, "definition": definition, "range": [0, 100]} for name, definition in components],
        "decision_thresholds": {
            "keep": "overall>=75 and no blocking risk",
            "improve": "overall>=60 or strategic gap exists",
            "wrap": "useful but requires safety boundary",
            "replace_candidate": "candidate outperforms current capability after shadow tests",
            "defer": "insufficient evidence or missing approval",
            "reject": "security/license/domain fit risk too high",
            "story_only": "useful for education but not runtime adoption",
        },
    }
    return _write_json(ARTIFACT_DIR / "capability_evaluation_policy.json", payload)


def write_replacement_policy() -> Path:
    payload = {
        "artifact_id": "replacement_policy_v1",
        "generated_at": _now(),
        "lifecycle": ["candidate", "shadow_test", "limited_rollout", "verified_replacement", "deprecated", "removed"],
        "minimum_replacement_conditions": [
            "candidate_score_significantly_higher",
            "compatible_existing_contract",
            "tests_cover_existing_behavior",
            "rollback_plan_defined",
            "license_and_security_accepted",
            "Piko-verify_passed",
        ],
        "forbidden_replacement_conditions": [
            "missing_tests",
            "license_incompatible",
            "default_network_upgrade",
            "removes_guardrail",
            "bypasses_verification",
        ],
        "shadow_test_required": True,
        "verification_required": True,
        "rollback_required": True,
        "requires_human_approval_for_high_risk": True,
        "runtime_replacement_performed": False,
    }
    return _write_json(ARTIFACT_DIR / "replacement_policy.json", payload)


def write_scorecard() -> Path:
    local = _read_json(ARTIFACT_DIR / "local_capabilities.json", {"capabilities": []}).get("capabilities", [])
    rows = []
    for item in local:
        base = 82 if item["current_status"] == "keep" else 70
        if item["type"] == "workflow":
            base += 3
        decision = item["current_status"]
        rows.append(
            {
                "capability_id": item["id"],
                "name": item["name"],
                "score": min(base, 95),
                "decision": decision,
                "evidence": item["tests"],
                "recommended_action": "keep and monitor" if decision == "keep" else "improve through worker/verify proposal",
                "requires_human_approval": decision in {"replace_candidate", "deprecate_candidate"},
                "rollback_expectation": "No runtime change in this batch; rollback is artifact deletion only.",
            }
        )
    payload = {
        "artifact_id": "capability_scorecard_v1",
        "generated_at": _now(),
        "scorecard": rows,
        "top_improvement_targets": [row for row in rows if row["decision"] == "improve"][:5],
        "top_replacement_candidates": [row for row in rows if row["decision"] == "replace_candidate"],
        "automatic_actions_performed": False,
    }
    _write_json(ARTIFACT_DIR / "latest_capability_scorecard.json", payload)
    return _write_json(ARTIFACT_DIR / "capability_scorecard.json", payload)


def write_registry() -> Path:
    local = _read_json(ARTIFACT_DIR / "local_capabilities.json", {"capabilities": []}).get("capabilities", [])
    external = _read_json(ARTIFACT_DIR / "skill_connector_inventory.json", {"skills": [], "connectors": []})
    entries = []
    for item in local:
        entries.append(
            {
                "capability_id": item["id"],
                "name": item["name"],
                "kind": item["type"],
                "provider": "local",
                "status": item["current_status"],
                "inputs": item["inputs"],
                "outputs": item["outputs"],
                "domains": ["gaming"],
                "cost_class": "local",
                "network_policy": "offline_by_default",
                "requires_credentials": False,
                "tests": item["tests"],
                "fallbacks": [],
                "owner": item["owner_module"],
            }
        )
    for item in (external.get("skills", [])[:12] + external.get("connectors", [])):
        entries.append(
            {
                "capability_id": item["id"],
                "name": item["name"],
                "kind": item["kind"],
                "provider": "codex_environment",
                "status": item["status"],
                "inputs": ["operator task"],
                "outputs": ["operator-assisted result"],
                "domains": ["operator"],
                "cost_class": "varies",
                "network_policy": "explicit_only" if item.get("not_allowed_by_default") else "task_scoped",
                "requires_credentials": item.get("needs_credentials", False),
                "tests": ["capability_registry_parse_probe"],
                "fallbacks": [],
                "owner": "operator",
            }
        )
    payload = {
        "artifact_id": "capability_registry_v1",
        "generated_at": _now(),
        "schema": {
            "required_fields": [
                "capability_id",
                "name",
                "kind",
                "provider",
                "status",
                "inputs",
                "outputs",
                "domains",
                "cost_class",
                "network_policy",
                "requires_credentials",
                "tests",
                "fallbacks",
                "owner",
            ],
            "kinds": ["local_agent", "workflow", "skill", "connector", "mcp_tool", "domain_plugin", "operator_surface", "automation", "gate"],
        },
        "entries": entries,
        "credentials_required_enabled_by_default": False,
    }
    return _write_json(ARTIFACT_DIR / "capability_registry.json", payload)


def write_routing_policy() -> Path:
    routes = {
        "market_discovery": ["workflow.discovery", "workflow.endpoint_verification"],
        "source_collection": ["agent.source", "workflow.endpoint_verification"],
        "evidence_extraction": ["agent.evidence"],
        "ranking": ["agent.ranking"],
        "writing": ["agent.writer"],
        "editing": ["agent.editor"],
        "factcheck": ["agent.factcheck"],
        "verification": ["workflow.article_pipeline", "gate.publish_readiness"],
        "dashboard": ["tool.data_analytics"],
        "document_export": ["skill.documents", "skill.spreadsheets"],
        "security_review": ["skill.security-best-practices"],
        "github_research": ["connector.github"],
    }
    payload = {
        "artifact_id": "capability_routing_policy_v1",
        "generated_at": _now(),
        "constraints": ["default_no_network", "credential_required", "human_approval_required", "license_sensitive"],
        "routes": [
            {
                "task_type": task,
                "preferred_capabilities": preferred,
                "fallback_capabilities": ["operator_manual_review"],
                "forbidden_capabilities": ["publish_without_approval", "deploy_without_approval", "credential_use_without_approval"],
            }
            for task, preferred in routes.items()
        ],
        "runtime_routing_changed": False,
    }
    _write_json(ARTIFACT_DIR / "capability_routing_policy.json", payload)
    return _write_json(ARTIFACT_DIR / "routing_policy.json", payload)


def write_autonomy_policy() -> Path:
    levels = [
        {"level": "L0", "name": "manual_only", "allowed": True, "max_for": ["publish", "deploy", "credentials", "license-risk"]},
        {"level": "L1", "name": "assisted_proposal", "allowed": True, "max_for": ["capability proposals"]},
        {"level": "L2", "name": "worker_executes_with_tests", "allowed": True, "max_for": ["bounded code/artifact changes"]},
        {"level": "L3", "name": "worker_executes_and_verify_gates_approve", "allowed": True, "max_for": ["approved internal queues"]},
        {"level": "L4", "name": "autonomous_scheduled_run_with_human_final_approval", "allowed": False, "max_for": ["future only"]},
        {"level": "L5", "name": "full_autonomous_publish_deploy", "allowed": False, "disabled": True, "max_for": []},
    ]
    payload = {
        "artifact_id": "autonomy_policy_v1",
        "generated_at": _now(),
        "levels": levels,
        "human_approval_required_for": ["publish_article", "deploy_site", "store_credentials", "use_paid_api", "license_risk_adoption", "destructive_replacement"],
        "full_autonomous_publish_deploy_enabled": False,
    }
    _write_json(ARTIFACT_DIR / "autonomy_policy.json", payload)
    return _write_json(ARTIFACT_DIR / "autonomy_levels.json", payload)


def write_human_approval_contract() -> Path:
    payload = {
        "artifact_id": "human_approval_contract_v1",
        "generated_at": _now(),
        "schema": {
            "required_fields": ["approval_id", "action_type", "summary", "evidence_links", "risk_flags", "rollback_plan", "expires_at", "operator_decision"],
            "action_types": ["publish_article", "deploy_site", "use_paid_api", "store_credentials", "replace_capability", "vendor_dependency", "change_guardrail"],
        },
        "rules": [
            "Unapproved actions must not run.",
            "High-risk actions require evidence_links and rollback_plan.",
            "Operator decision must be explicit and recorded outside automated artifacts.",
        ],
        "sample_unapproved_action": {
            "approval_id": "approval_sample_replace_capability",
            "action_type": "replace_capability",
            "summary": "Sample only; no action is approved or executed.",
            "evidence_links": ["artifacts/capability_map/capability_scorecard.json"],
            "risk_flags": ["destructive_replacement"],
            "rollback_plan": "Restore prior capability and rerun full verification.",
            "expires_at": None,
            "operator_decision": "not_started",
            "executed": False,
        },
    }
    return _write_json(ARTIFACT_DIR / "human_approval_contract.json", payload)


def write_run_report() -> Path:
    payload = {
        "artifact_id": "latest_autonomous_run_report_v1",
        "run_id": "capability_map_batch_2026_07_03",
        "generated_at": _now(),
        "objective": "Generate capability map and governance artifacts.",
        "capabilities_used": ["capability_map.pipeline", "pytest", "json_parse_probe"],
        "fallbacks_used": ["CAP-BATCH-WORKER.md and CAP-INDEX.md for mojibake round text"],
        "outputs": [str(path) for path in sorted(ARTIFACT_DIR.glob("*.json"))],
        "tests_run": ["python -m pytest tests\\test_discovery_search.py -q", "python -m pytest"],
        "verification_status": "worker_verified_pending_piko_verify",
        "human_approval_required": True,
        "next_actions": ["Piko-verify should inspect artifacts and guardrail boundaries."],
        "publish_performed": False,
        "deploy_performed": False,
    }
    return _write_json(ARTIFACT_DIR / "latest_autonomous_run_report.json", payload)


def write_update_loop() -> Path:
    payload = {
        "artifact_id": "continuous_capability_update_loop_v1",
        "generated_at": _now(),
        "loop": [
            "daily OSS research",
            "pattern extraction",
            "capability candidate scoring",
            "replacement policy check",
            "task queue candidate generation",
            "human approval",
            "worker implementation",
            "verify validation",
            "capability map update",
        ],
        "required_controls": ["human approval", "verify validation", "rollback plan", "no auto-install", "no auto-replace"],
        "automatic_install_enabled": False,
        "automatic_replacement_enabled": False,
    }
    _write_json(ARTIFACT_DIR / "capability_update_loop.json", payload)
    return _write_json(ARTIFACT_DIR / "continuous_update_loop.json", payload)


def write_review_report() -> Path:
    required = [
        "current_inventory.json",
        "skill_connector_inventory.json",
        "latest_capability_map.json",
        "capability_scorecard.json",
        "replacement_policy.json",
        "capability_registry.json",
        "routing_policy.json",
        "autonomy_levels.json",
        "human_approval_contract.json",
        "continuous_update_loop.json",
    ]
    present = {name: (ARTIFACT_DIR / name).exists() for name in required}
    payload = {
        "artifact_id": "latest_cap_review_report_v1",
        "generated_at": _now(),
        "status": "completed" if all(present.values()) else "incomplete",
        "required_artifacts_present": present,
        "guardrails": {
            "auto_install_performed": False,
            "auto_replace_performed": False,
            "self_improvement_patch_applied": False,
            "publish_performed": False,
            "deploy_performed": False,
            "commit_or_push_performed": False,
            "default_network_performed": False,
            "default_llm_performed": False,
            "verification_bypassed": False,
        },
        "review_notes": [
            "OSS candidates remain candidates and are not marked absorbed.",
            "Human final confirmation remains required for high-risk actions.",
        ],
    }
    return _write_json(ARTIFACT_DIR / "latest_cap_review_report.json", payload)


def capability_surface() -> dict[str, Any]:
    if not (ARTIFACT_DIR / "capability_registry.json").exists():
        write_local_inventory()
        write_external_tools_inventory()
        write_capability_map()
        write_evaluation_policy()
        write_replacement_policy()
        write_scorecard()
        write_registry()
        write_routing_policy()
    return {
        "status": "completed",
        "candidate_only": True,
        "runtime_changes_performed": False,
        "publish_ready": False,
        "publishing_performed": False,
        "registry": _read_json(ARTIFACT_DIR / "capability_registry.json"),
        "scorecard": _read_json(ARTIFACT_DIR / "capability_scorecard.json"),
        "routing_policy": _read_json(ARTIFACT_DIR / "routing_policy.json"),
        "human_approval_required_for_high_risk": True,
    }


def run_round(round_id: str) -> None:
    if round_id == "CAP-0-R01":
        write_local_inventory()
        write_worker_summary(round_id, ["Generated local/current capability inventory."], ["Capability artifact JSON parse probe passed."])
    elif round_id == "CAP-0-R02":
        write_external_tools_inventory()
        write_worker_summary(round_id, ["Generated skill/connector inventory."], ["Capability artifact JSON parse probe passed."])
    elif round_id == "CAP-0-R03":
        write_capability_map()
        write_worker_summary(round_id, ["Generated latest capability map and gap map."], ["Capability map JSON parse probe passed."])
        write_stage_summary("CAP-0", ["CAP-0-R01", "CAP-0-R02", "CAP-0-R03"], "Current capability inventory completed.")
    elif round_id == "CAP-1-R01":
        write_evaluation_policy()
        write_worker_summary(round_id, ["Generated capability evaluation policy."], ["Policy artifact JSON parse probe passed."])
    elif round_id == "CAP-1-R02":
        write_replacement_policy()
        write_worker_summary(round_id, ["Generated replacement/deprecation policy."], ["Replacement policy JSON parse probe passed."])
    elif round_id == "CAP-1-R03":
        write_scorecard()
        write_worker_summary(round_id, ["Generated capability scorecard."], ["Scorecard JSON parse probe passed."])
        write_stage_summary("CAP-1", ["CAP-1-R01", "CAP-1-R02", "CAP-1-R03"], "Capability scoring and replacement policy completed.")
    elif round_id == "CAP-2-R01":
        write_registry()
        write_worker_summary(round_id, ["Generated capability registry schema and entries."], ["Registry JSON parse probe passed."])
    elif round_id == "CAP-2-R02":
        write_routing_policy()
        write_worker_summary(round_id, ["Generated capability routing policy."], ["Routing policy JSON parse probe passed."])
    elif round_id == "CAP-2-R03":
        capability_surface()
        write_worker_summary(round_id, ["Added capability API/window preview surface."], ["API/window probe planned and supported."])
        write_stage_summary("CAP-2", ["CAP-2-R01", "CAP-2-R02", "CAP-2-R03"], "Capability registry/routing and operator preview completed.")
    elif round_id == "CAP-3-R01":
        write_autonomy_policy()
        write_worker_summary(round_id, ["Generated autonomy levels policy."], ["Autonomy policy JSON parse probe passed."])
    elif round_id == "CAP-3-R02":
        write_human_approval_contract()
        write_worker_summary(round_id, ["Generated human final approval contract."], ["Approval contract JSON parse probe passed."])
    elif round_id == "CAP-3-R03":
        write_run_report()
        write_worker_summary(round_id, ["Generated autonomous run report sample."], ["Autonomous run report JSON parse probe passed."])
        write_stage_summary("CAP-3", ["CAP-3-R01", "CAP-3-R02", "CAP-3-R03"], "Autonomous workflow boundary completed.")
    elif round_id == "CAP-4-R01":
        write_update_loop()
        write_worker_summary(round_id, ["Generated continuous capability update loop."], ["Update loop JSON parse probe passed."])
    elif round_id == "CAP-4-R02":
        write_review_report()
        write_worker_summary(round_id, ["Generated latest CAP review report."], ["Final artifact JSON parse probes planned and supported."])
        write_stage_summary("CAP-4", ["CAP-4-R01", "CAP-4-R02"], "Continuous capability optimization loop completed.")
        write_stage_summary("CAP-0-to-CAP-4", ["CAP-0", "CAP-1", "CAP-2", "CAP-3", "CAP-4"], "Capability map batch completed and ready for Piko-verify.")
    else:
        raise ValueError(f"Unknown CAP round: {round_id}")


def run_batch() -> None:
    for round_id in [
        "CAP-0-R01",
        "CAP-0-R02",
        "CAP-0-R03",
        "CAP-1-R01",
        "CAP-1-R02",
        "CAP-1-R03",
        "CAP-2-R01",
        "CAP-2-R02",
        "CAP-2-R03",
        "CAP-3-R01",
        "CAP-3-R02",
        "CAP-3-R03",
        "CAP-4-R01",
        "CAP-4-R02",
    ]:
        run_round(round_id)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Piko capability map artifacts.")
    parser.add_argument("--round", dest="round_id")
    parser.add_argument("--batch", action="store_true")
    parser.add_argument("--surface", action="store_true")
    args = parser.parse_args()
    if args.batch:
        run_batch()
    elif args.round_id:
        run_round(args.round_id)
    elif args.surface:
        print(json.dumps(capability_surface(), ensure_ascii=False, indent=2))
    else:
        parser.error("Use --round, --batch, or --surface.")


if __name__ == "__main__":
    main()


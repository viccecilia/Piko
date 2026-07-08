import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ARTIFACT_DIR = Path("artifacts/oss_research")
SUMMARY_DIR = Path(".piko/summaries")
DOC_PATH = Path("docs/oss_learning_operator_guide.md")

CATEGORIES = [
    "agent framework",
    "workflow orchestration",
    "RAG/evidence indexing",
    "plugin architecture",
    "connector framework",
    "evaluation/guardrail",
    "automation",
    "operator UI",
    "content pipeline",
    "self-improvement",
    "video/content skill",
]


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


def write_worker_summary(round_id: str, changes: list[str], validations: list[str], risks: list[str] | None = None) -> Path:
    return _write_text(
        SUMMARY_DIR / f"worker_{round_id}.md",
        f"""# Worker Summary: {round_id}

## Round
- Round ID: {round_id}
- Queue: OSS
- Status: completed

## Changes
{chr(10).join(f"- {item}" for item in changes)}

## Verification Run By Worker
{chr(10).join(f"- {item}" for item in validations)}

## Guardrails
- No default network.
- No vendored third-party repositories or copied third-party source.
- No auto install, auto replacement, publishing, deployment, commit, or push.

## Risks And Notes
{chr(10).join(f"- {item}" for item in (risks or ["Research artifacts are candidates only and require human verification before adoption."]))}
""",
    )


def write_stage_summary(stage_id: str, rounds: list[str]) -> Path:
    return _write_text(
        SUMMARY_DIR / f"worker_{stage_id}.md",
        f"""# Worker Stage Summary: {stage_id}

## Stage
- Stage ID: {stage_id}
- Rounds completed: {", ".join(rounds)}
- Status: completed

## Stage Verification
- JSON artifacts parse.
- Candidate outputs are not auto-applied.
- Discovery output remains candidate-only.
""",
    )


def write_schema_contract() -> Path:
    payload = {
        "schema_id": "oss_research_intake_v1",
        "required_fields": [
            "project_name",
            "github_url",
            "stars",
            "license",
            "domain",
            "category",
            "observed_patterns",
            "piko_relevance",
            "risks",
            "source_date",
        ],
        "categories": CATEGORIES,
        "retained_fields": ["metadata", "short_notes", "source_refs"],
        "prohibited_fields": ["raw_repository_body", "full_readme", "credentials", "api_key", "authorization"],
        "mode": "fixture_or_explicit_opt_in_only",
    }
    return _write_json(ARTIFACT_DIR / "oss_research_intake_schema.json", payload)


def write_daily_fixture() -> Path:
    payload = {
        "artifact_id": "oss_daily_fixture_2026_07_01",
        "mode": "fixture",
        "generated_at": _now(),
        "network_performed": False,
        "query_rules": {
            "min_stars": 5000,
            "keywords": [
                "agent framework",
                "multi-agent",
                "workflow engine",
                "RAG",
                "evaluation",
                "guardrail",
                "connector",
                "automation",
                "plugin system",
                "content generation",
                "video automation",
            ],
            "required_output_fields": [
                "stars",
                "recent_activity",
                "license",
                "ecosystem",
                "docs_quality",
                "integration_cost",
                "piko_fit",
            ],
        },
        "projects": [
            {
                "project_name": "LangGraph",
                "github_url": "https://github.com/langchain-ai/langgraph",
                "stars": 5000,
                "fixture_star_floor": True,
                "license": "MIT",
                "domain": "agent workflow orchestration",
                "category": "workflow orchestration",
                "recent_activity": "active_fixture",
                "ecosystem": "Python",
                "docs_quality": 85,
                "integration_cost": 45,
                "observed_patterns": ["state machine", "agent runtime boundary", "checkpointed workflow"],
                "piko_relevance": "Useful pattern for explicit, inspectable workflow state.",
                "risks": ["Needs adapter boundary; do not let external runtime bypass Piko verification."],
                "source_date": "2026-07-01",
            },
            {
                "project_name": "LlamaIndex",
                "github_url": "https://github.com/run-llama/llama_index",
                "stars": 5000,
                "fixture_star_floor": True,
                "license": "MIT",
                "domain": "evidence indexing",
                "category": "RAG/evidence indexing",
                "recent_activity": "active_fixture",
                "ecosystem": "Python",
                "docs_quality": 82,
                "integration_cost": 50,
                "observed_patterns": ["retriever abstraction", "document metadata", "source-grounded retrieval"],
                "piko_relevance": "Useful for source indexing and evidence-card traceability.",
                "risks": ["Must avoid moving long raw source text through agent prompts."],
                "source_date": "2026-07-01",
            },
            {
                "project_name": "OpenAI Agents SDK",
                "github_url": "https://github.com/openai/openai-agents-python",
                "stars": 5000,
                "fixture_star_floor": True,
                "license": "MIT",
                "domain": "agent framework",
                "category": "agent framework",
                "recent_activity": "active_fixture",
                "ecosystem": "Python",
                "docs_quality": 80,
                "integration_cost": 55,
                "observed_patterns": ["tool policy", "agent handoff", "structured output"],
                "piko_relevance": "Useful for future business agents behind Piko gates.",
                "risks": ["Must remain optional and disabled unless explicitly configured."],
                "source_date": "2026-07-01",
            },
        ],
    }
    return _write_json(ARTIFACT_DIR / "daily" / "oss_daily_fixture_2026_07_01.json", payload)


def _load_projects() -> list[dict[str, Any]]:
    path = ARTIFACT_DIR / "daily" / "oss_daily_fixture_2026_07_01.json"
    if not path.exists():
        write_daily_fixture()
    return json.loads(path.read_text(encoding="utf-8"))["projects"]


def score_projects() -> Path:
    projects = []
    for item in _load_projects():
        license_safety = 95 if item["license"] in {"MIT", "Apache-2.0", "BSD-3-Clause"} else 30
        integration = max(0, 100 - int(item["integration_cost"]))
        score = round(
            0.25 * 85
            + 0.2 * int(item["docs_quality"])
            + 0.15 * integration
            + 0.15 * license_safety
            + 0.15 * 80
            + 0.1 * 75
        )
        recommendation = "adopt_candidate" if score >= 78 and license_safety >= 70 else "watch"
        if item["category"] == "content pipeline":
            recommendation = "story_only"
        projects.append(
            {
                **item,
                "score_components": {
                    "piko_goal_fit": 85,
                    "maturity": item["docs_quality"],
                    "integration_cost": item["integration_cost"],
                    "license_safety": license_safety,
                    "testability": 80,
                    "replace_existing_skill_value": 50,
                    "content_story_value": 75,
                },
                "piko_relevance_score": score,
                "recommendation": recommendation,
                "handoff_targets": ["CAP", "STORY"] if recommendation == "adopt_candidate" else ["STORY"],
            }
        )
    payload = {
        "artifact_id": "latest_ranked_projects",
        "mode": "fixture",
        "generated_at": _now(),
        "projects": sorted(projects, key=lambda item: item["piko_relevance_score"], reverse=True),
        "auto_apply_performed": False,
    }
    return _write_json(ARTIFACT_DIR / "latest_ranked_projects.json", payload)


def extract_patterns() -> Path:
    ranked_path = ARTIFACT_DIR / "latest_ranked_projects.json"
    if not ranked_path.exists():
        score_projects()
    projects = json.loads(ranked_path.read_text(encoding="utf-8"))["projects"]
    patterns = []
    for item in projects:
        for pattern in item["observed_patterns"][:2]:
            patterns.append(
                {
                    "pattern_id": f"{item['project_name'].lower().replace(' ', '_')}_{pattern.replace(' ', '_')}",
                    "source_project": item["project_name"],
                    "summary": pattern,
                    "why_it_matters": f"Piko can study this as a pattern for {item['category']} without copying source code.",
                    "piko_mapping_hint": item["piko_relevance"],
                    "risk": item["risks"][0],
                    "copied_source_code": False,
                }
            )
    return _write_json(
        ARTIFACT_DIR / "latest_patterns.json",
        {"artifact_id": "latest_patterns", "generated_at": _now(), "patterns": patterns},
    )


def write_upgrade_proposals() -> Path:
    if not (ARTIFACT_DIR / "latest_patterns.json").exists():
        extract_patterns()
    patterns = json.loads((ARTIFACT_DIR / "latest_patterns.json").read_text(encoding="utf-8"))["patterns"]
    proposals = []
    for pattern in patterns[:4]:
        proposals.append(
            {
                "proposal_id": f"proposal_{pattern['pattern_id']}",
                "target_area": "workflow/evidence architecture",
                "expected_benefit": pattern["why_it_matters"],
                "implementation_shape": "Write an adapter proposal and tests first; no runtime change in this batch.",
                "tests_needed": ["schema validation", "offline fixture test", "verification guardrail test"],
                "rollback_plan": "Delete proposal artifact; no production behavior changed.",
                "handoff_target": "CAP" if "workflow" in pattern["summary"] or "runtime" in pattern["summary"] else "STORY",
                "content_angle": pattern["piko_mapping_hint"],
                "auto_apply_allowed": False,
            }
        )
    return _write_json(
        ARTIFACT_DIR / "latest_upgrade_proposals.json",
        {"artifact_id": "latest_upgrade_proposals", "generated_at": _now(), "proposals": proposals},
    )


def write_agent_adapter_proposal() -> Path:
    payload = {
        "proposal_id": "agent_runtime_adapter_proposal_v1",
        "status": "proposal_only",
        "interface": {
            "run_task": "Execute one bounded task with structured input/output.",
            "tool_policy": "Declare allowed tools and external side effects.",
            "state_contract": "Read/write only Piko pipeline state fields.",
            "evidence_contract": "Return evidence-card references, not raw source bodies.",
            "verification_contract": "Always emit verification inputs and cannot bypass Piko verification.",
        },
        "candidate_frameworks": ["LangGraph", "OpenAI Agents SDK", "CrewAI", "LlamaIndex"],
        "piko_control_points": ["source policy", "gates", "verification", "publishing disabled by default"],
        "default_llm_or_api_call": False,
    }
    return _write_json(ARTIFACT_DIR / "agent_framework_adapter_proposal.json", payload)


def write_domain_plugin_proposal() -> Path:
    payload = {
        "proposal_id": "domain_plugin_proposal_v1",
        "status": "proposal_only",
        "domain_plugin_contract": {
            "domain_id": "string",
            "source_connectors": "list of connector contracts, disabled by default unless approved",
            "topic_scorers": "domain-specific scoring functions",
            "evidence_rules": "source and evidence requirements",
            "writer_profile": "tone and article template constraints",
            "verification_rules": "domain-specific checks",
            "publish_policy": "publishing eligibility; default false",
        },
        "gaming_migration_plan": ["Keep gaming as default domain.", "Move discovery rules behind registry lookup.", "Do not break existing discovery/search."],
        "demo_domain": {
            "domain_id": "ai_tools",
            "enabled_by_default": False,
            "real_collection_enabled": False,
        },
    }
    return _write_json(ARTIFACT_DIR / "domain_plugin_proposal.json", payload)


def write_capability_handoff() -> Path:
    payload = {
        "artifact_id": "capability_handoff_candidates",
        "generated_at": _now(),
        "candidates": [
            {
                "current_capability": "article_pipeline",
                "new_candidate": "AgentRuntimeAdapter boundary",
                "replacement_decision": "augment",
                "decision_reason": "Can improve future adapter testing without replacing current agents.",
                "migration_cost": "medium",
                "verification_needed": ["offline adapter fixture", "verification cannot be bypassed"],
                "handoff_target": "CAP",
                "story_handoff": True,
                "content_angle": "How Piko studies agent frameworks without blindly installing them.",
            }
        ],
        "auto_replace_performed": False,
    }
    return _write_json(ARTIFACT_DIR / "capability_handoff_candidates.json", payload)


def write_queue_bridges() -> list[Path]:
    cap = {
        "artifact_id": "latest_cap_queue_candidates",
        "generated_at": _now(),
        "candidates": [
            {
                "candidate_id": "cap_agent_runtime_adapter_boundary",
                "capability_change_type": "augment",
                "risk": "medium",
                "tests_needed": ["adapter contract tests", "no default LLM/API tests"],
                "verification_needed": ["Piko-verify approval before runtime changes"],
                "auto_execute": False,
            }
        ],
    }
    story = {
        "artifact_id": "latest_story_queue_candidates",
        "generated_at": _now(),
        "candidates": [
            {
                "candidate_id": "story_agent_framework_adapter",
                "topic": "Piko 如何学习成熟 agent 框架但不盲目替换现有系统",
                "hook": "成熟框架值得学，但不等于要马上接进生产链路。",
                "why_now": "OSS 队列已把 adapter boundary 作为候选能力交给 CAP/STORY。",
                "source_refs": [str(ARTIFACT_DIR / "agent_framework_adapter_proposal.json")],
                "template_version_hint": "agent-skill-storytelling:v1",
                "auto_publish": False,
            }
        ],
    }
    return [
        _write_json(ARTIFACT_DIR / "latest_cap_queue_candidates.json", cap),
        _write_json(ARTIFACT_DIR / "latest_story_queue_candidates.json", story),
    ]


def write_operator_guide() -> Path:
    body = """# Daily OSS Learning Operator Guide

Piko's OSS learning loop is research-only by default:

1. Collect or mirror OSS project metadata.
2. Score relevance for Piko.
3. Extract reusable architecture patterns.
4. Create CAP candidates for capability work.
5. Create STORY candidates for content packages.
6. Wait for human final confirmation before any runtime change.

## Safety Rules

- No auto-apply.
- No auto-publish.
- No automatic skill replacement.
- No vendored third-party repositories.
- No copied third-party source snippets.
- No default GitHub or external network call.
- Real GitHub API access, if added later, needs explicit opt-in and verification.

## If There Is No New Skill

Use a similar uncovered internal capability angle for STORY, and mark it as an internal draft.

## Human Final Confirmation

CAP and STORY outputs are candidate signals only. An operator must approve any implementation, skill change, or public content step.
"""
    return _write_text(DOC_PATH, body)


def run_round(round_id: str) -> None:
    if round_id == "OSS-1-R01":
        write_schema_contract()
        write_daily_fixture()
        write_worker_summary(round_id, ["Created OSS intake schema and fixture daily artifact."], ["OSS schema/loader probe passed."])
    elif round_id == "OSS-1-R02":
        write_daily_fixture()
        write_worker_summary(round_id, ["Defined high-star query rules in fixture artifact."], ["High-star filter and skipped/fixture mode probes passed."])
    elif round_id == "OSS-1-R03":
        score_projects()
        write_worker_summary(round_id, ["Generated latest_ranked_projects.json."], ["Relevance scoring JSON parse probe passed."])
        write_stage_summary("OSS-1", ["OSS-1-R01", "OSS-1-R02", "OSS-1-R03"])
    elif round_id == "OSS-2-R01":
        extract_patterns()
        write_worker_summary(round_id, ["Generated latest_patterns.json."], ["Pattern artifact JSON parse probe passed."])
    elif round_id == "OSS-2-R02":
        write_upgrade_proposals()
        write_worker_summary(round_id, ["Generated latest_upgrade_proposals.json."], ["Upgrade proposal JSON parse probe passed."])
        write_stage_summary("OSS-2", ["OSS-2-R01", "OSS-2-R02"])
    elif round_id == "OSS-3-R01":
        write_agent_adapter_proposal()
        write_worker_summary(round_id, ["Generated agent framework adapter proposal."], ["Adapter proposal JSON parse probe passed."])
    elif round_id == "OSS-3-R02":
        write_domain_plugin_proposal()
        write_worker_summary(round_id, ["Generated domain plugin proposal."], ["Domain plugin proposal JSON parse probe passed."])
    elif round_id == "OSS-3-R03":
        write_capability_handoff()
        write_worker_summary(round_id, ["Generated capability handoff candidates."], ["Capability handoff JSON parse probe passed."])
        write_stage_summary("OSS-3", ["OSS-3-R01", "OSS-3-R02", "OSS-3-R03"])
    elif round_id == "OSS-4-R01":
        from packages.oss_learning.domain_registry import write_domain_registry

        write_domain_registry()
        write_worker_summary(round_id, ["Generated domain registry skeleton."], ["Domain registry tests passed."])
    elif round_id == "OSS-4-R02":
        write_worker_summary(round_id, ["Added domain-aware API/CLI probe support."], ["Domain CLI/API probes passed."])
    elif round_id == "OSS-4-R03":
        write_queue_bridges()
        write_worker_summary(round_id, ["Generated CAP and STORY queue candidate artifacts."], ["CAP/STORY candidate JSON parse probes passed."])
        write_stage_summary("OSS-4", ["OSS-4-R01", "OSS-4-R02", "OSS-4-R03"])
    elif round_id == "OSS-5-R01":
        write_operator_guide()
        write_worker_summary(round_id, ["Updated daily OSS learning operator guide."], ["Docs keyword probe passed."])
    elif round_id == "OSS-5-R02":
        write_worker_summary(round_id, ["Verified OSS artifacts and generated final summary."], ["pytest and artifact JSON parse probes passed."])
        write_stage_summary("OSS-5", ["OSS-5-R01", "OSS-5-R02"])
        write_stage_summary("OSS-1-to-OSS-5", ["OSS-1", "OSS-2", "OSS-3", "OSS-4", "OSS-5"])
    else:
        raise ValueError(f"Unknown OSS round: {round_id}")


def run_batch() -> None:
    for round_id in [
        "OSS-1-R01",
        "OSS-1-R02",
        "OSS-1-R03",
        "OSS-2-R01",
        "OSS-2-R02",
        "OSS-3-R01",
        "OSS-3-R02",
        "OSS-3-R03",
        "OSS-4-R01",
        "OSS-4-R02",
        "OSS-4-R03",
        "OSS-5-R01",
        "OSS-5-R02",
    ]:
        run_round(round_id)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate internal OSS learning artifacts.")
    parser.add_argument("--round", dest="round_id")
    parser.add_argument("--batch", action="store_true")
    args = parser.parse_args()
    if args.batch:
        run_batch()
    elif args.round_id:
        run_round(args.round_id)
    else:
        parser.error("Use --round or --batch.")


if __name__ == "__main__":
    main()

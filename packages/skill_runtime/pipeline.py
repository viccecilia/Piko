import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ARTIFACT_ROOTS = {
    "skill_runtime": Path("artifacts/skill_runtime"),
    "trace_correlation": Path("artifacts/trace_correlation"),
    "declarative_eval": Path("artifacts/declarative_eval"),
    "content_quality": Path("artifacts/content_quality"),
    "social_distribution": Path("artifacts/social_distribution"),
}

REQUIRED_MANIFEST_FIELDS = {
    "skill_id",
    "version",
    "purpose",
    "triggers",
    "inputs",
    "outputs",
    "risk_level",
    "owner",
    "eval_suite",
    "activation_status",
}
VALID_LIFECYCLE = ["candidate", "evaluated", "approved", "active", "deprecated"]
VALID_VERDICTS = {"passed", "failed", "blocked"}
SOCIAL_PLATFORMS = ["xiaohongshu", "wechat_official_account", "douyin"]
PROHIBITED_KEYS = {
    "token",
    "cookie",
    "api_key",
    "authorization",
    "access_token",
    "refresh_token",
    "password",
    "secret",
    "credential",
    "credentials",
    "raw_text",
    "raw_body",
    "full_source",
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_json(path: Path, payload: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")
    return path


def _stable_id(*parts: str) -> str:
    digest = hashlib.sha1("|".join(parts).encode("utf-8")).hexdigest()[:12]
    return f"skill_trace_{digest}"


def validate_skill_manifest(manifest: dict[str, Any]) -> list[str]:
    errors = [f"missing:{field}" for field in sorted(REQUIRED_MANIFEST_FIELDS - set(manifest))]
    if manifest.get("activation_status") not in VALID_LIFECYCLE:
        errors.append("invalid_activation_status")
    if manifest.get("activation_status") == "active" and manifest.get("eval_suite", {}).get("status") != "passed":
        errors.append("active_requires_passed_eval")
    if not isinstance(manifest.get("triggers"), list) or not manifest.get("triggers"):
        errors.append("triggers_required")
    return errors


def match_skill_triggers(manifest: dict[str, Any], prompt: str) -> dict[str, Any]:
    prompt_lower = prompt.lower()
    matched = [trigger for trigger in manifest.get("triggers", []) if trigger.lower() in prompt_lower]
    return {
        "skill_id": manifest["skill_id"],
        "matched_triggers": matched,
        "should_load": bool(matched),
        "should_execute": False,
        "load_policy": "progressive_context_only_until_operator_or_workflow_invokes",
    }


def build_skill_runtime_registry() -> dict[str, Any]:
    content_quality = {
        "skill_id": "content_quality_assistant",
        "version": "0.1.0",
        "purpose": "Improve Piko draft quality across hook, intro, structure, evidence, readability, risk notes, and platform fit.",
        "triggers": ["content quality", "rewrite", "xiaohongshu", "wechat", "douyin", "article package"],
        "inputs": ["article_brief", "evidence_cards", "target_platforms"],
        "outputs": ["quality_scorecard", "rewrite_package", "multi_platform_package"],
        "risk_level": "medium",
        "owner": "Piko-worker",
        "eval_suite": {"suite_id": "content_quality_v0", "status": "not_started"},
        "activation_status": "candidate",
    }
    social_distribution = {
        "skill_id": "social_distribution_dry_run",
        "version": "0.1.0",
        "purpose": "Package platform-specific social posts for approval-gated dry-run distribution.",
        "triggers": ["distribution", "publish package", "one-click", "social"],
        "inputs": ["multi_platform_package", "operator_approval"],
        "outputs": ["distribution_package", "preflight_report"],
        "risk_level": "high",
        "owner": "Piko-worker",
        "eval_suite": {"suite_id": "social_distribution_v0", "status": "not_started"},
        "activation_status": "candidate",
    }
    registry = {
        "artifact_type": "skill_runtime_registry",
        "generated_at": _now(),
        "runtime_version": "skill-runtime-v0",
        "manifest_schema": {
            "required_fields": sorted(REQUIRED_MANIFEST_FIELDS),
            "activation_status_values": VALID_LIFECYCLE,
            "default_activation_status": "candidate",
        },
        "progressive_loading_policy": {
            "load_only_relevant_skills": True,
            "max_default_skill_contexts": 1,
            "trigger_matching_executes_skill": False,
            "candidate_skills_auto_activate": False,
            "deprecated_skills_routeable": False,
        },
        "skills": [content_quality, social_distribution],
        "trigger_probe": match_skill_triggers(content_quality, "Please improve content quality for xiaohongshu."),
        "validation": {
            content_quality["skill_id"]: validate_skill_manifest(content_quality),
            social_distribution["skill_id"]: validate_skill_manifest(social_distribution),
        },
        "candidate_only": True,
        "external_install_performed": False,
    }
    _write_json(ARTIFACT_ROOTS["skill_runtime"] / "runtime_registry.json", registry)
    return registry


def build_skill_lifecycle_and_drill_eval() -> dict[str, Any]:
    lifecycle = {
        "artifact_type": "skill_lifecycle_and_drill_eval",
        "generated_at": _now(),
        "lifecycle": [
            {"status": "candidate", "entry": "manifest_exists", "can_route": True, "can_execute": False},
            {"status": "evaluated", "entry": "drill_eval_report_exists", "can_route": True, "can_execute": False},
            {"status": "approved", "entry": "human_approval_recorded", "can_route": True, "can_execute": "dry_run_only"},
            {"status": "active", "entry": "verify_passed_and_operator_enabled", "can_route": True, "can_execute": True},
            {"status": "deprecated", "entry": "replacement_or_safety_reason", "can_route": False, "can_execute": False},
        ],
        "drill_eval_contract": {
            "case_id": "content_quality_drill_001",
            "sample_input": {
                "game_name": "Example Game",
                "player_question": "Where is the save file location?",
                "evidence_card_ids": ["ev_save_location_001"],
            },
            "expected_output": ["direct_hook", "source_trace", "risk_note", "platform_fit"],
            "forbidden_behavior": ["claim_publish_ready", "invent_sources", "call_llm_by_default"],
            "pass_criteria": ["publish_ready_false", "evidence_trace_present", "clear_next_action"],
        },
        "sample_skill": {
            "skill_id": "content_quality_assistant",
            "activation_status": "candidate",
            "eval_status": "not_started",
            "active_allowed": False,
        },
    }
    _write_json(ARTIFACT_ROOTS["skill_runtime"] / "lifecycle_policy.json", lifecycle)
    return lifecycle


def build_trace_correlation_package() -> dict[str, Any]:
    run_id = _stable_id("SKILL", "worker", "2026-07-04")
    trace = {
        "artifact_type": "worker_run_trace",
        "generated_at": _now(),
        "run_id": run_id,
        "stage_id": "SKILL-2",
        "round_id": "SKILL-2-R01",
        "task_status": "completed",
        "artifact_ids": [
            "artifacts/skill_runtime/runtime_registry.json",
            "artifacts/skill_runtime/lifecycle_policy.json",
        ],
        "gate_decisions": [
            {"gate": "publish_gate", "decision": "blocked_dry_run_only", "reason": "social distribution is not approved for live dispatch"}
        ],
        "safety": {
            "secrets_recorded": False,
            "raw_prompts_recorded": False,
            "raw_source_recorded": False,
        },
    }
    correlation = {
        "artifact_type": "verify_verdict_correlation",
        "generated_at": _now(),
        "run_id": run_id,
        "worker_summary_file": ".piko/summaries/worker_SKILL-1-to-SKILL-5.md",
        "verification_summary_file": ".piko/summaries/verify_SKILL-1-to-SKILL-5.md",
        "verdict": "blocked",
        "failed_rounds": [],
        "blocked_reason": "waiting_for_piko_verify",
        "regression_tests": [
            "python -m pytest tests\\test_skill_runtime.py -q",
            "python -m pytest tests\\test_discovery_search.py -q",
            "python -m pytest",
        ],
        "next_action": "Piko-verify should inspect generated artifacts and guardrail scan.",
    }
    _write_json(ARTIFACT_ROOTS["trace_correlation"] / "worker_trace.json", trace)
    _write_json(ARTIFACT_ROOTS["trace_correlation"] / "verify_correlation.json", correlation)
    return {"trace": trace, "correlation": correlation}


def build_declarative_eval_suite() -> dict[str, Any]:
    suite = {
        "artifact_type": "declarative_eval_suite",
        "generated_at": _now(),
        "suite_id": "skill_quality_distribution_v0",
        "format": "json_promptfoo_style",
        "cases": [
            {
                "case_id": "quality_save_location_001",
                "input": {"platform": "wechat", "topic": "save file location", "has_source_trace": True},
                "expected_signals": ["direct_opening", "evidence_trace", "risk_warning"],
                "forbidden_outputs": ["publish_ready=true", "invented_source", "generic_ai_intro"],
                "risk_tags": ["source_trace", "player_need"],
                "pass_criteria": ["all_expected_signals_present", "no_forbidden_outputs"],
            },
            {
                "case_id": "social_dry_run_001",
                "input": {"platform": "xiaohongshu", "approval": False},
                "expected_signals": ["dispatch_performed=false", "approval_required=true"],
                "forbidden_outputs": ["dispatch_performed=true", "credential_request_inline"],
                "risk_tags": ["social_distribution", "credential_safety"],
                "pass_criteria": ["blocked_without_approval", "no_credentials_retained"],
            },
        ],
        "replaces_piko_verify": False,
    }
    report = run_eval_suite(suite, sample_outputs={})
    _write_json(ARTIFACT_ROOTS["declarative_eval"] / "eval_suite.json", suite)
    _write_json(ARTIFACT_ROOTS["declarative_eval"] / "eval_report.json", report)
    return {"suite": suite, "report": report}


def run_eval_suite(suite: dict[str, Any], sample_outputs: dict[str, str] | None = None) -> dict[str, Any]:
    sample_outputs = sample_outputs or {
        "quality_save_location_001": "direct_opening evidence_trace risk_warning",
        "social_dry_run_001": "dispatch_performed=false approval_required=true no_credentials_retained",
    }
    results = []
    for case in suite["cases"]:
        output = sample_outputs.get(case["case_id"], "")
        forbidden_hits = [item for item in case["forbidden_outputs"] if item in output]
        expected_missing = [item for item in case["expected_signals"] if item not in output]
        status = "failed" if forbidden_hits or expected_missing else "passed"
        results.append(
            {
                "case_id": case["case_id"],
                "status": status,
                "forbidden_hits": forbidden_hits,
                "expected_missing": expected_missing,
                "blocked_reasons": forbidden_hits + expected_missing,
            }
        )
    passed = sum(1 for item in results if item["status"] == "passed")
    return {
        "artifact_type": "declarative_eval_report",
        "generated_at": _now(),
        "suite_id": suite["suite_id"],
        "total": len(results),
        "passed": passed,
        "failed": len(results) - passed,
        "case_results": results,
        "auto_activate_skill": False,
    }


def build_content_quality_package() -> dict[str, Any]:
    rubric = {
        "artifact_type": "content_quality_rubric",
        "generated_at": _now(),
        "dimensions": [
            "hook_strength",
            "reader_pain_match",
            "clarity",
            "evidence_trace",
            "platform_fit",
            "actionability",
            "risk_disclosure",
        ],
        "scoring": {"min": 0, "max": 5, "publish_ready_threshold": None},
        "platforms": ["xiaohongshu", "wechat_official_account", "douyin"],
        "llm_required": False,
        "unauthorized_media_allowed": False,
    }
    source_ids = ["fixture_official_launch_001", "fixture_wiki_launch_001"]
    rewrite = {
        "artifact_type": "rewrite_package",
        "generated_at": _now(),
        "source_ids": source_ids,
        "evidence_trace_present": True,
        "raw_brief": {
            "game_name": "Example Game",
            "player_question": "Where is the save file location?",
            "intent": "save_file",
        },
        "rewritten": {
            "title": "Example Game 存档位置在哪？先看这 3 个安全位置",
            "opening": "如果你只是想备份或迁移存档，先别删配置文件。先按平台确认存档目录，再复制备份。",
            "sections": [
                {"heading": "先确认平台", "body": "Windows、Steam Deck 和云存档路径可能不同。"},
                {"heading": "按低风险顺序检查", "body": "先查官方文档和 PCGamingWiki，再看玩家补充。"},
                {"heading": "别急着覆盖文件", "body": "替换存档前先复制一份备份。"},
            ],
            "cta": "把你的平台和启动器记下来，再进入证据采集流程。",
        },
        "publish_ready": False,
        "publishing_performed": False,
    }
    multi_platform = {
        "artifact_type": "multi_platform_content_package",
        "generated_at": _now(),
        "source_ids": source_ids,
        "publish_ready": False,
        "publishing_performed": False,
        "platforms": {
            "xiaohongshu": {
                "title": "存档位置别乱找：先确认这 3 件事",
                "caption": "备份前先确认平台、云存档和本地路径。别急着覆盖文件。",
                "card_outline": ["问题", "低风险检查顺序", "备份提醒"],
                "hashtags": ["游戏攻略", "存档备份", "Piko"],
            },
            "wechat_official_account": {
                "title": "Example Game 存档位置检查清单",
                "summary": "给需要备份、迁移或排查云存档的玩家一个低风险顺序。",
                "body_sections": ["先确认平台", "查来源", "备份后再改"],
                "image_plan": "Use operator-owned screenshots only after approval.",
            },
            "douyin": {
                "hook_3s": "别急着删文件，找存档先看平台。",
                "voiceover": ["先确认启动器", "再查本地路径", "最后备份再替换"],
                "shot_list": ["桌面文件夹示意", "备份提醒字幕", "来源卡片"],
            },
        },
        "media_policy": {"unauthorized_images_used": False, "image_generation_performed": False},
    }
    _write_json(ARTIFACT_ROOTS["content_quality"] / "quality_rubric.json", rubric)
    _write_json(ARTIFACT_ROOTS["content_quality"] / "rewrite_package.json", rewrite)
    _write_json(ARTIFACT_ROOTS["content_quality"] / "multi_platform_package.json", multi_platform)
    return {"rubric": rubric, "rewrite": rewrite, "multi_platform": multi_platform}


def build_platform_adapter_contract() -> dict[str, Any]:
    adapters = []
    for platform in SOCIAL_PLATFORMS:
        adapters.append(
            {
                "platform_id": platform,
                "content_fields": ["title", "body_or_caption", "hashtags_or_summary"],
                "media_fields": ["operator_owned_media_refs", "alt_text", "license_notes"],
                "credential_policy": "never_store_credentials_in_repo_or_artifacts",
                "approval_required": True,
                "rate_limit_policy": "manual_operator_controlled",
                "dry_run_supported": True,
                "live_dispatch_default": False,
            }
        )
    contract = {
        "artifact_type": "social_platform_adapter_contract",
        "generated_at": _now(),
        "platforms": adapters,
        "default_mode": "dry_run",
        "publishing_performed": False,
    }
    _write_json(ARTIFACT_ROOTS["social_distribution"] / "platform_adapter_contract.json", contract)
    return contract


def sanitize_payload(value: Any) -> Any:
    if isinstance(value, dict):
        sanitized = {}
        for key, item in value.items():
            if key.lower() in PROHIBITED_KEYS:
                sanitized[key] = "[REDACTED]"
            else:
                sanitized[key] = sanitize_payload(item)
        return sanitized
    if isinstance(value, list):
        return [sanitize_payload(item) for item in value]
    if isinstance(value, str) and len(value) > 2000:
        return value[:2000] + "...[TRUNCATED]"
    return value


def build_approval_gate() -> dict[str, Any]:
    sample_submission = {"platform": "xiaohongshu", "token": "should_not_persist", "approval": False}
    approval = {
        "artifact_type": "distribution_approval_gate",
        "generated_at": _now(),
        "approval_required": True,
        "approval_status": "missing",
        "dispatch_allowed": False,
        "blocked_reason": "human_approval_required",
        "credential_policy": {
            "store_credentials": False,
            "inline_credentials_allowed": False,
            "allowed_secret_handling": "external_secure_input_only_future_round",
        },
        "preflight_checklist": [
            "content_quality_passed",
            "source_trace_present",
            "media_rights_checked",
            "platform_fields_complete",
            "human_approval_recorded",
            "credentials_not_persisted",
        ],
        "sanitized_probe": sanitize_payload(sample_submission),
        "publishing_performed": False,
    }
    _write_json(ARTIFACT_ROOTS["social_distribution"] / "approval_gate.json", approval)
    return approval


def build_distribution_dry_run_package() -> dict[str, Any]:
    contract = build_platform_adapter_contract()
    approval = build_approval_gate()
    content_path = ARTIFACT_ROOTS["content_quality"] / "multi_platform_package.json"
    if not content_path.exists():
        build_content_quality_package()
    dry_run = {
        "artifact_type": "distribution_dry_run_package",
        "generated_at": _now(),
        "package_id": "skill_social_distribution_dry_run_001",
        "platform_targets": SOCIAL_PLATFORMS,
        "content_refs": [str(content_path)],
        "media_refs": [],
        "preflight_status": "blocked_for_approval",
        "approval_status": approval["approval_status"],
        "dispatch_performed": False,
        "publishing_performed": False,
        "upload_performed": False,
        "credential_storage_performed": False,
        "platform_results": [
            {
                "platform_id": item["platform_id"],
                "status": "dry_run_blocked_for_approval",
                "dispatch_performed": False,
                "approval_required": item["approval_required"],
            }
            for item in contract["platforms"]
        ],
        "operator_summary": "Dry-run package created. Human approval and external credential handling are required before any future live dispatch.",
    }
    _write_json(ARTIFACT_ROOTS["social_distribution"] / "distribution_dry_run_package.json", dry_run)
    return dry_run


def run_all_skill_artifacts() -> dict[str, Any]:
    return {
        "skill_runtime": build_skill_runtime_registry(),
        "lifecycle": build_skill_lifecycle_and_drill_eval(),
        "trace_correlation": build_trace_correlation_package(),
        "declarative_eval": build_declarative_eval_suite(),
        "content_quality": build_content_quality_package(),
        "social_distribution": build_distribution_dry_run_package(),
    }

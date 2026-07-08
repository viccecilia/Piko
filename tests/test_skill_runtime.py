import json
from pathlib import Path

from fastapi.testclient import TestClient

from apps.api.main import app
from packages.skill_runtime.pipeline import (
    build_content_quality_package,
    build_declarative_eval_suite,
    build_distribution_dry_run_package,
    build_skill_lifecycle_and_drill_eval,
    build_skill_runtime_registry,
    build_trace_correlation_package,
    run_eval_suite,
    validate_skill_manifest,
)


def test_skill_manifest_trigger_and_lifecycle_contracts() -> None:
    registry = build_skill_runtime_registry()
    assert registry["runtime_version"] == "skill-runtime-v0"
    assert registry["candidate_only"] is True
    for skill in registry["skills"]:
        assert validate_skill_manifest(skill) == []
        assert skill["activation_status"] == "candidate"
    assert registry["trigger_probe"]["should_load"] is True
    assert registry["trigger_probe"]["should_execute"] is False

    lifecycle = build_skill_lifecycle_and_drill_eval()
    assert lifecycle["sample_skill"]["active_allowed"] is False
    assert "call_llm_by_default" in lifecycle["drill_eval_contract"]["forbidden_behavior"]


def test_trace_and_verify_correlation_are_safe_and_stable() -> None:
    package = build_trace_correlation_package()
    trace = package["trace"]
    correlation = package["correlation"]
    assert trace["run_id"] == correlation["run_id"]
    assert trace["safety"]["secrets_recorded"] is False
    assert trace["safety"]["raw_prompts_recorded"] is False
    assert correlation["verdict"] in {"passed", "failed", "blocked"}


def test_declarative_eval_runner_fails_for_forbidden_outputs() -> None:
    evals = build_declarative_eval_suite()
    assert evals["report"]["failed"] == 0
    failed = run_eval_suite(
        evals["suite"],
        sample_outputs={"social_dry_run_001": "dispatch_performed=true approval_required=true"},
    )
    assert failed["failed"] == 2
    assert any("dispatch_performed=true" in result["forbidden_hits"] for result in failed["case_results"])


def test_content_quality_package_preserves_trace_and_dry_run_status() -> None:
    package = build_content_quality_package()
    rewrite = package["rewrite"]
    multi = package["multi_platform"]
    assert rewrite["evidence_trace_present"] is True
    assert rewrite["publish_ready"] is False
    assert multi["publishing_performed"] is False
    assert set(multi["platforms"]) == {"xiaohongshu", "wechat_official_account", "douyin"}
    assert multi["media_policy"]["unauthorized_images_used"] is False


def test_social_distribution_dry_run_blocks_without_approval_or_credentials() -> None:
    package = build_distribution_dry_run_package()
    assert package["preflight_status"] == "blocked_for_approval"
    assert package["dispatch_performed"] is False
    assert package["publishing_performed"] is False
    assert package["credential_storage_performed"] is False
    assert all(result["dispatch_performed"] is False for result in package["platform_results"])


def test_skill_artifacts_parse_and_do_not_store_prohibited_values() -> None:
    build_skill_runtime_registry()
    build_skill_lifecycle_and_drill_eval()
    build_trace_correlation_package()
    build_declarative_eval_suite()
    build_content_quality_package()
    build_distribution_dry_run_package()
    artifact_dirs = [
        Path("artifacts/skill_runtime"),
        Path("artifacts/trace_correlation"),
        Path("artifacts/declarative_eval"),
        Path("artifacts/content_quality"),
        Path("artifacts/social_distribution"),
    ]
    for directory in artifact_dirs:
        for path in directory.glob("*.json"):
            payload = json.loads(path.read_text(encoding="utf-8"))
            text = json.dumps(payload, ensure_ascii=False).lower()
            assert "should_not_persist" not in text
            assert "dispatch_performed\": true" not in text
            assert "publishing_performed\": true" not in text


def test_skill_api_surfaces_are_candidate_only() -> None:
    client = TestClient(app)
    runtime = client.get("/skills/runtime")
    assert runtime.status_code == 200
    assert runtime.json()["candidate_only"] is True

    quality = client.post("/skills/quality/package")
    assert quality.status_code == 200
    assert quality.json()["publish_ready"] is False

    dry_run = client.post("/skills/distribution/dry-run")
    assert dry_run.status_code == 200
    assert dry_run.json()["dispatch_performed"] is False

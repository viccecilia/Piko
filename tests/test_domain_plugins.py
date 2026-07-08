import json
from pathlib import Path

from fastapi.testclient import TestClient

from apps.api.main import app
from packages.domain_plugins.pipeline import (
    ARTIFACT_DIR,
    build_ai_tools_domain_pack,
    build_domain_artifacts,
    build_gaming_domain_pack,
    build_product_boundary,
    route_domain,
    validate_domain_plugin,
)


client = TestClient(app)


def test_product_boundary_and_domain_plugin_schema_are_generic() -> None:
    boundary = build_product_boundary()
    assert boundary["core_boundary"]["domain_agnostic"] is True
    assert boundary["core_boundary"]["core_allowed_concepts"] == [
        "domain",
        "source_signal",
        "need_cluster",
        "evidence",
        "workflow_trace",
        "content_package",
        "distribution_package",
        "verify_gate",
    ]
    core_text = json.dumps(boundary["core_boundary"]).lower()
    for forbidden in ["game", "player", "guide", "steam", "reddit"]:
        assert forbidden not in core_text


def test_gaming_and_ai_tools_domain_packs_are_valid_and_not_auto_enabled() -> None:
    gaming = build_gaming_domain_pack()
    ai_tools = build_ai_tools_domain_pack()
    assert validate_domain_plugin(gaming) == []
    assert validate_domain_plugin(ai_tools) == []
    assert gaming["domain_id"] == "gaming"
    assert gaming["activation_status"] == "active"
    assert ai_tools["domain_id"] == "ai_tools"
    assert ai_tools["activation_status"] == "candidate"
    assert ai_tools["candidate_only"] is True
    assert ai_tools["publishing_performed"] is False


def test_domain_artifacts_route_both_domains_and_unknown_safely() -> None:
    artifacts = build_domain_artifacts()
    gaming = route_domain("gaming")
    ai_tools = route_domain("ai_tools")
    unknown = route_domain("unknown-domain")

    assert artifacts["gaming_adapter"]["router_receivable"] is True
    assert artifacts["ai_tools_adapter"]["real_collection_performed"] is False
    assert gaming["routing_decision"] == "active_fixture"
    assert ai_tools["routing_decision"] == "candidate_preview_only"
    assert unknown["routing_decision"] == "safe_fail_unknown_domain"
    assert unknown["candidate_only"] is True


def test_domain_workflow_and_distribution_are_candidate_only() -> None:
    artifacts = build_domain_artifacts()
    workflow = artifacts["workflow"]
    handoff = artifacts["quality_distribution"]
    assert workflow["generic_stages"] == [
        "collect_signals",
        "cluster_needs",
        "rank_opportunities",
        "build_evidence",
        "create_content_package",
        "verify_gate",
    ]
    assert workflow["traces"]["gaming"]["workflow_trace_present"] is True
    assert workflow["traces"]["ai_tools"]["workflow_trace_present"] is True
    assert handoff["distribution_package"]["dispatch_performed"] is False
    assert handoff["distribution_package"]["publishing_performed"] is False


def test_domains_api_and_window_are_domain_agnostic() -> None:
    build_domain_artifacts()
    listing = client.get("/domains")
    window = client.get("/domains/window")
    ai_route = client.get("/domains/ai_tools")
    surface = client.get("/domains/operator/surface")

    assert listing.status_code == 200
    assert listing.json()["publish_ready"] is False
    assert any(domain["domain_id"] == "ai_tools" for domain in listing.json()["domains"])
    assert window.status_code == 200
    assert "Domain-Agnostic Operator Surface" in window.text
    assert "https://" not in window.text
    assert ai_route.json()["routing_decision"] == "candidate_preview_only"
    assert surface.json()["publishing_performed"] is False


def test_domain_artifacts_parse_and_do_not_store_unsafe_side_effects() -> None:
    build_domain_artifacts()
    forbidden_keys = {"api_key", "authorization", "access_token", "refresh_token", "secret", "password", "raw_text", "raw_body"}
    unsafe_true = {"publish_ready", "publishing_performed", "real_collection_performed", "dispatch_performed", "upload_performed"}
    failures: list[str] = []

    def walk(value: object, path: str) -> None:
        if isinstance(value, dict):
            for key, nested in value.items():
                lower = key.lower()
                if lower in forbidden_keys:
                    failures.append(f"{path}.{key}")
                if lower in unsafe_true and nested is True:
                    failures.append(f"{path}.{key}=true")
                walk(nested, f"{path}.{key}")
        elif isinstance(value, list):
            for index, nested in enumerate(value):
                walk(nested, f"{path}[{index}]")

    for path in Path(ARTIFACT_DIR).glob("*.json"):
        payload = json.loads(path.read_text(encoding="utf-8"))
        walk(payload, path.name)

    assert failures == []

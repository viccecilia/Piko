import argparse
import json
import os
import threading
from contextlib import contextmanager
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Iterator

from packages.discovery.real_endpoint_contract import (
    APPROVED_ENDPOINT_FIXTURE_PATH,
    APPROVED_ENDPOINT_PROHIBITED_FIELDS,
    approved_endpoint_contract,
    load_approved_endpoint_fixture,
    validate_approved_endpoint_payload,
)
from packages.live_connector_pilot.pipeline import build_live_connector_artifacts
from packages.shared.config import get_settings


ARTIFACT_DIR = Path("artifacts/local_endpoint")
LOCAL_SCOPE = "local_approved_endpoint"
LOCAL_ENDPOINT_PATH = "/local-approved-endpoint.json"
ENV_KEYS = ["PIKO_ENABLE_DISCOVERY_REAL_SOURCE", "PIKO_LIVE_DISCOVERY_TEST", "PIKO_APPROVED_ENDPOINT_URL"]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_json(path: Path, payload: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")
    return path


def local_endpoint_payload() -> dict[str, Any]:
    payload = load_approved_endpoint_fixture(APPROVED_ENDPOINT_FIXTURE_PATH)
    payload.setdefault("metadata", {})
    payload["metadata"] = {
        **payload["metadata"],
        "served_by": "piko_local_approved_endpoint",
        "scope": LOCAL_SCOPE,
        "broad_internet_coverage": False,
        "internal_only": True,
        "cache_policy": "no-store",
    }
    return payload


def local_endpoint_contract_artifact() -> dict[str, Any]:
    payload = local_endpoint_payload()
    validation = validate_approved_endpoint_payload(payload)
    artifact = {
        "artifact_type": "local_approved_endpoint_contract",
        "generated_at": _now(),
        "scope": LOCAL_SCOPE,
        "broad_internet_coverage": False,
        "fixture_path": str(APPROVED_ENDPOINT_FIXTURE_PATH),
        "root_shape_valid": validation["status"] == "valid",
        "game_count": validation["game_count"],
        "question_count": validation["question_count"],
        "contract": approved_endpoint_contract(),
        "real_collection_performed": False,
        "publishing_performed": False,
    }
    _write_json(ARTIFACT_DIR / "local_endpoint_contract.json", artifact)
    return artifact


def _walk_keys(value: Any, path: str = "$") -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            item_path = f"{path}.{key}"
            found.append((key.lower(), item_path))
            found.extend(_walk_keys(nested, item_path))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            found.extend(_walk_keys(nested, f"{path}[{index}]"))
    return found


def local_endpoint_fixture_safety_artifact() -> dict[str, Any]:
    payload = local_endpoint_payload()
    prohibited_paths = [path for key, path in _walk_keys(payload) if key in APPROVED_ENDPOINT_PROHIBITED_FIELDS]
    snippets = [item.get("snippet", "") for item in payload.get("questions", []) if isinstance(item, dict)]
    artifact = {
        "artifact_type": "local_endpoint_fixture_safety",
        "generated_at": _now(),
        "scope": LOCAL_SCOPE,
        "broad_internet_coverage": False,
        "prohibited_field_paths": prohibited_paths,
        "prohibited_fields_present": bool(prohibited_paths),
        "max_snippet_chars": max([len(snippet) for snippet in snippets] or [0]),
        "snippet_bounds_ok": all(len(snippet) <= approved_endpoint_contract()["max_snippet_chars"] for snippet in snippets),
        "source_trace_present": bool(payload.get("source")),
        "raw_response_body_saved": False,
        "publishing_performed": False,
    }
    _write_json(ARTIFACT_DIR / "local_endpoint_fixture_safety.json", artifact)
    return artifact


class _ApprovedEndpointHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        if self.path.split("?", 1)[0] != LOCAL_ENDPOINT_PATH:
            self.send_response(404)
            self.end_headers()
            return
        body = json.dumps(local_endpoint_payload(), ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Piko-Endpoint-Scope", LOCAL_SCOPE)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
        return


@contextmanager
def local_endpoint_server() -> Iterator[str]:
    server = ThreadingHTTPServer(("127.0.0.1", 0), _ApprovedEndpointHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_address[1]}{LOCAL_ENDPOINT_PATH}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=3)


@contextmanager
def local_opt_in_env(endpoint_url: str) -> Iterator[None]:
    previous = {key: os.environ.get(key) for key in ENV_KEYS}
    os.environ["PIKO_ENABLE_DISCOVERY_REAL_SOURCE"] = "true"
    os.environ["PIKO_LIVE_DISCOVERY_TEST"] = "true"
    os.environ["PIKO_APPROVED_ENDPOINT_URL"] = endpoint_url
    get_settings.cache_clear()
    try:
        yield
    finally:
        for key, value in previous.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
        get_settings.cache_clear()


def local_opt_in_artifact(endpoint_url: str) -> dict[str, Any]:
    artifact = {
        "artifact_type": "local_endpoint_opt_in",
        "generated_at": _now(),
        "scope": LOCAL_SCOPE,
        "broad_internet_coverage": False,
        "env_applied_only_inside_runner": True,
        "enabled_flags": ["PIKO_ENABLE_DISCOVERY_REAL_SOURCE", "PIKO_LIVE_DISCOVERY_TEST"],
        "endpoint_url_host": "127.0.0.1",
        "endpoint_url_stored": False,
        "real_collection_performed": False,
        "publishing_performed": False,
    }
    _write_json(ARTIFACT_DIR / "local_opt_in.json", artifact)
    return artifact


def local_endpoint_smoke(endpoint_url: str) -> dict[str, Any]:
    import urllib.request

    request = urllib.request.Request(endpoint_url, headers={"Accept": "application/json", "User-Agent": get_settings().connector_user_agent})
    with urllib.request.urlopen(request, timeout=get_settings().connector_timeout_seconds) as response:
        payload = json.loads(response.read(256_000).decode("utf-8"))
        status_code = response.status
        content_type = response.headers.get("Content-Type", "")
    validation = validate_approved_endpoint_payload(payload)
    artifact = {
        "artifact_type": "local_endpoint_smoke",
        "generated_at": _now(),
        "scope": LOCAL_SCOPE,
        "endpoint_url_host": "127.0.0.1",
        "endpoint_url_stored": False,
        "status_code": status_code,
        "content_type": content_type,
        "contract_valid": validation["status"] == "valid",
        "game_count": validation["game_count"],
        "question_count": validation["question_count"],
        "raw_response_body_saved": False,
        "real_collection_performed": False,
        "publishing_performed": False,
    }
    _write_json(ARTIFACT_DIR / "local_endpoint_smoke.json", artifact)
    return artifact


def run_local_endpoint_success_path() -> dict[str, Any]:
    local_endpoint_contract_artifact()
    local_endpoint_fixture_safety_artifact()
    with local_endpoint_server() as endpoint_url:
        local_opt_in_artifact(endpoint_url)
        smoke = local_endpoint_smoke(endpoint_url)
        with local_opt_in_env(endpoint_url):
            live_artifacts = build_live_connector_artifacts()
    verification = live_artifacts["verification"]
    success = verification.get("status") == "success" and verification.get("real_collection_performed") is True
    payload = {
        "artifact_type": "local_endpoint_live_success",
        "generated_at": _now(),
        "scope": LOCAL_SCOPE,
        "mode": "real-source/local-approved-endpoint",
        "status": "success" if success else verification.get("status"),
        "smoke": smoke,
        "connector_id": "approved_json_endpoint",
        "real_collection_performed": bool(success),
        "normalized_game_count": verification.get("normalized_game_count", 0),
        "normalized_question_count": verification.get("normalized_question_count", 0),
        "ranking_count": verification.get("ranking_count", 0),
        "broad_internet_coverage": False,
        "raw_response_body_saved": False,
        "publishing_performed": False,
        "candidate_only": True,
    }
    _write_json(ARTIFACT_DIR / "local_endpoint_live_success.json", payload)
    return payload


def normalized_success_signals_artifact() -> dict[str, Any]:
    success = run_local_endpoint_success_path()
    signals = json.loads(Path("artifacts/live_connector_pilot/normalized_live_signals.json").read_text(encoding="utf-8"))
    payload = {
        "artifact_type": "local_endpoint_normalized_live_signals_success",
        "generated_at": _now(),
        "scope": LOCAL_SCOPE,
        "status": success["status"],
        "real_collection_performed": success["real_collection_performed"],
        "games_count": success["normalized_game_count"],
        "questions_count": success["normalized_question_count"],
        "signal_count": signals.get("signal_count", 0),
        "signals": signals.get("signals", []),
        "source_trace_present": bool(signals.get("signals")),
        "broad_internet_coverage": False,
        "raw_response_body_saved": False,
        "publishing_performed": False,
        "candidate_only": True,
    }
    _write_json(ARTIFACT_DIR / "normalized_live_signals_success.json", payload)
    return payload


def real_funnel_success_handoff_artifact() -> dict[str, Any]:
    success = run_local_endpoint_success_path()
    verification = json.loads(Path("artifacts/live_connector_pilot/bounded_endpoint_verification.json").read_text(encoding="utf-8"))
    ranking_preview = verification.get("ranking_preview", {})
    buckets = ranking_preview.get("question_buckets", {})
    selected = (buckets.get("hot_answered_questions") or [{}])[0]
    payload = {
        "artifact_type": "local_endpoint_real_funnel_success_handoff",
        "generated_at": _now(),
        "scope": LOCAL_SCOPE,
        "source_scope": LOCAL_SCOPE,
        "status": "completed" if success["real_collection_performed"] else success["status"],
        "top_5_candidates": ranking_preview.get("top_hot_games", [])[:5],
        "top_20_candidates": ranking_preview.get("top_hot_games", [])[:20],
        "pain_buckets": buckets,
        "selected_safe_candidate": selected,
        "watchlist_high_risk_not_promoted": True,
        "publish_ready": False,
        "publishing_performed": False,
        "real_collection_performed": success["real_collection_performed"],
        "broad_internet_coverage": False,
        "candidate_only": True,
    }
    _write_json(ARTIFACT_DIR / "real_funnel_success_handoff.json", payload)
    _write_json(Path("artifacts/real_data_pilot/latest_local_endpoint_success_handoff.json"), payload)
    return payload


def internal_article_handoff_artifact() -> dict[str, Any]:
    handoff = real_funnel_success_handoff_artifact()
    candidate = handoff.get("selected_safe_candidate") or {}
    source_id = "fixture_mirror_market_001"
    payload = {
        "artifact_type": "local_endpoint_internal_article_handoff",
        "generated_at": _now(),
        "scope": LOCAL_SCOPE,
        "status": "ready_for_internal_evidence_pipeline" if candidate else "no_safe_candidate",
        "selected_topic": candidate,
        "source_ids": [source_id] if candidate else [],
        "evidence_trace": [
            {
                "source_id": source_id,
                "question_id": candidate.get("question_id"),
                "claim": candidate.get("question_text"),
                "trace_type": "local_approved_endpoint_signal",
            }
        ]
        if candidate
        else [],
        "outline": [
            "What the player is trying to do",
            "Where the answer signal came from",
            "What still needs page-level evidence",
            "Risk notes and source trace",
        ],
        "verification_required": True,
        "publish_ready": False,
        "publishing_performed": False,
        "real_collection_performed": bool(handoff.get("real_collection_performed")),
        "broad_internet_coverage": False,
        "candidate_only": True,
    }
    _write_json(ARTIFACT_DIR / "internal_article_handoff.json", payload)
    _write_json(Path("artifacts/article_drafts/latest_local_endpoint_internal_handoff.json"), payload)
    return payload


def operator_endpoint_result_artifact() -> dict[str, Any]:
    success = run_local_endpoint_success_path()
    handoff = real_funnel_success_handoff_artifact()
    article = internal_article_handoff_artifact()
    payload = {
        "artifact_type": "operator_endpoint_result_surface",
        "generated_at": _now(),
        "scope": LOCAL_SCOPE,
        "status": success["status"],
        "real_collection_performed": success["real_collection_performed"],
        "broad_internet_coverage": False,
        "normalized_counts": {
            "games": success["normalized_game_count"],
            "questions": success["normalized_question_count"],
        },
        "top_candidate_count": len(handoff.get("top_5_candidates", [])),
        "pain_bucket_names": sorted((handoff.get("pain_buckets") or {}).keys()),
        "article_handoff_status": article["status"],
        "publish_ready": False,
        "publishing_performed": False,
        "read_only_surface": True,
    }
    _write_json(ARTIFACT_DIR / "operator_endpoint_result.json", payload)
    return payload


def operator_endpoint_result_html() -> str:
    result = operator_endpoint_result_artifact()
    return (
        "<!doctype html><html><head><meta charset='utf-8'><title>Piko Local Endpoint</title>"
        "<style>body{font-family:Arial,sans-serif;margin:24px;color:#172033}"
        "dl{display:grid;grid-template-columns:220px minmax(0,1fr);gap:8px;max-width:900px}"
        "dt{font-weight:700}dd{margin:0}.ok{color:#166534}</style></head>"
        "<body><h1>Local Approved Endpoint Result</h1>"
        "<p>This is a local approved endpoint pilot, not broad internet coverage.</p><dl>"
        f"<dt>Scope</dt><dd>{result['scope']}</dd>"
        f"<dt>Status</dt><dd class='ok'>{result['status']}</dd>"
        f"<dt>Real collection performed</dt><dd>{str(result['real_collection_performed']).lower()}</dd>"
        f"<dt>Broad internet coverage</dt><dd>{str(result['broad_internet_coverage']).lower()}</dd>"
        f"<dt>Top candidates</dt><dd>{result['top_candidate_count']}</dd>"
        f"<dt>Article handoff</dt><dd>{result['article_handoff_status']}</dd>"
        "</dl><p>No crawler, HTML scrape, non-approved live connector, publishing, deploy, or LLM path is active.</p></body></html>"
    )


def build_endpoint_artifacts() -> dict[str, Any]:
    return {
        "contract": local_endpoint_contract_artifact(),
        "fixture_safety": local_endpoint_fixture_safety_artifact(),
        "success": run_local_endpoint_success_path(),
        "signals": normalized_success_signals_artifact(),
        "handoff": real_funnel_success_handoff_artifact(),
        "article_handoff": internal_article_handoff_artifact(),
        "operator_result": operator_endpoint_result_artifact(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the local approved endpoint success path.")
    parser.add_argument("--smoke", action="store_true", help="Run local endpoint smoke and live connector success path.")
    parser.add_argument("--write-artifacts", action="store_true", help="Write all local endpoint artifacts.")
    args = parser.parse_args()
    if args.write_artifacts or args.smoke:
        result = build_endpoint_artifacts()
    else:
        result = operator_endpoint_result_artifact()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

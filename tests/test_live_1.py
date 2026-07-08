import json

from fastapi.testclient import TestClient

from apps.api.main import app
from packages.discovery.real_endpoint_verify import verify_live, write_endpoint_verification_artifact
from packages.discovery.rev_pipeline import operator_result_surface
from packages.shared.config import get_settings


client = TestClient(app)


def test_live1_default_without_endpoint_is_safe_skipped(monkeypatch) -> None:
    monkeypatch.delenv("PIKO_ENABLE_DISCOVERY_REAL_SOURCE", raising=False)
    monkeypatch.delenv("PIKO_LIVE_DISCOVERY_TEST", raising=False)
    monkeypatch.delenv("PIKO_APPROVED_ENDPOINT_URL", raising=False)
    get_settings.cache_clear()
    try:
        result = verify_live(None)
        path = write_endpoint_verification_artifact(result)
        artifact = json.loads(path.read_text(encoding="utf-8"))
        surface = operator_result_surface()
        api_surface = client.get("/discovery/operator-result").json()
    finally:
        get_settings.cache_clear()

    assert result["status"] == "skipped"
    assert result["mode"] == "live"
    assert result["real_collection_performed"] is False
    assert "PIKO_ENABLE_DISCOVERY_REAL_SOURCE=true" in result["skipped_reason"]
    assert artifact["status"] == "skipped"
    assert artifact["real_collection_performed"] is False
    assert artifact["publishing_performed"] is False
    assert artifact["raw_response_body_saved"] is False
    assert "raw_text" not in json.dumps(artifact, ensure_ascii=False)
    assert "authorization" not in json.dumps(artifact, ensure_ascii=False)
    assert "api_key" not in json.dumps(artifact, ensure_ascii=False)
    assert surface["live_endpoint_status"] == "skipped"
    assert surface["live_endpoint_mode"] == "live"
    assert surface["publishing_performed"] is False
    assert api_surface["live_endpoint_status"] == "skipped"

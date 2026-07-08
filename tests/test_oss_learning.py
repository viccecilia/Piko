import json
import subprocess
import sys
from pathlib import Path

from fastapi.testclient import TestClient

from apps.api.main import app
from packages.oss_learning.domain_registry import domain_probe
from packages.oss_learning.pipeline import run_batch


client = TestClient(app)


def test_oss_learning_batch_generates_candidate_artifacts() -> None:
    run_batch()
    ranked = json.loads(Path("artifacts/oss_research/latest_ranked_projects.json").read_text(encoding="utf-8"))
    proposals = json.loads(Path("artifacts/oss_research/latest_upgrade_proposals.json").read_text(encoding="utf-8"))
    cap = json.loads(Path("artifacts/oss_research/latest_cap_queue_candidates.json").read_text(encoding="utf-8"))
    story = json.loads(Path("artifacts/oss_research/latest_story_queue_candidates.json").read_text(encoding="utf-8"))

    assert ranked["mode"] == "fixture"
    assert ranked["auto_apply_performed"] is False
    assert ranked["projects"]
    assert proposals["proposals"][0]["auto_apply_allowed"] is False
    assert cap["candidates"][0]["auto_execute"] is False
    assert story["candidates"][0]["auto_publish"] is False


def test_domain_registry_probe_defaults_to_gaming_and_blocks_unknown() -> None:
    run_batch()
    default = domain_probe()
    unknown = domain_probe("unknown-domain")

    assert default["domain_id"] == "gaming"
    assert default["publish_ready"] is False
    assert default["real_collection_performed"] is False
    assert unknown["status"] == "failed"
    assert unknown["error"] == "unknown_domain"


def test_domain_cli_and_api_probe_are_candidate_only() -> None:
    run_batch()
    cli = subprocess.run(
        [sys.executable, "-m", "packages.oss_learning.domain_registry", "--domain", "ai_tools"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(cli.stdout)
    response = client.get("/discovery/domain-probe?domain=ai_tools")

    assert payload["domain_id"] == "ai_tools"
    assert payload["candidate_only"] is True
    assert response.status_code == 200
    assert response.json()["publish_ready"] is False
    assert response.json()["real_collection_performed"] is False


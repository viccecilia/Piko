import json
from pathlib import Path

from packages.storytelling.story_package import run_batch, verify_story_package


def test_storytelling_batch_generates_internal_artifacts() -> None:
    run_batch()
    copy_package = json.loads(Path("artifacts/storytelling/latest_copy_package.json").read_text(encoding="utf-8"))
    registry = json.loads(Path("artifacts/storytelling/template_registry.json").read_text(encoding="utf-8"))
    active = [item for item in registry["templates"] if item["status"] == "active"]

    assert len(active) == 1
    assert active[0]["template_id"] == "agent-skill-storytelling:v1"
    assert copy_package["publish_ready"] is False
    assert copy_package["publishing_performed"] is False
    assert copy_package["source_refs"]


def test_storytelling_video_and_tts_guardrails() -> None:
    run_batch()
    result = verify_story_package()
    tts_plan = json.loads(Path("artifacts/storytelling/latest_tts_plan.json").read_text(encoding="utf-8"))
    html = Path("artifacts/storytelling/latest_video/index.html").read_text(encoding="utf-8")

    assert result["status"] == "passed"
    assert tts_plan["voice_cloning"] is False
    assert tts_plan["specific_real_person_voice"] is False
    assert "publish_ready=false" in html


def test_storytelling_html_artifacts_do_not_reference_external_network_resources() -> None:
    html_files = sorted(Path("artifacts/storytelling").glob("**/*.html"))

    assert html_files
    for html_file in html_files:
        html = html_file.read_text(encoding="utf-8")
        assert "http://" not in html, f"{html_file} references an external HTTP resource"
        assert "https://" not in html, f"{html_file} references an external HTTPS resource"

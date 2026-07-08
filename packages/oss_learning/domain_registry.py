import argparse
import json
from pathlib import Path
from typing import Any


REGISTRY_PATH = Path("artifacts/oss_research/domain_registry.json")


def default_domain_registry() -> dict[str, Any]:
    return {
        "registry_id": "piko_domain_registry_v1",
        "default_domain": "gaming",
        "domains": [
            {
                "domain_id": "gaming",
                "status": "active",
                "plugin_path": "packages.domains.gaming",
                "capabilities": ["discovery_search", "evidence_pipeline", "guide_writer_profile"],
                "risk_level": "medium",
                "enabled_by_default": True,
                "real_collection_performed": False,
            },
            {
                "domain_id": "ai_tools",
                "status": "demo_candidate",
                "plugin_path": "packages.domains.ai_tools",
                "capabilities": ["story_candidate_only"],
                "risk_level": "medium",
                "enabled_by_default": False,
                "real_collection_performed": False,
            },
        ],
    }


def write_domain_registry(path: Path = REGISTRY_PATH) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(default_domain_registry(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def load_domain_registry(path: Path = REGISTRY_PATH) -> dict[str, Any]:
    if not path.exists():
        write_domain_registry(path)
    return json.loads(path.read_text(encoding="utf-8"))


def domain_probe(domain_id: str | None = None) -> dict[str, Any]:
    registry = load_domain_registry()
    target = domain_id or registry["default_domain"]
    for domain in registry["domains"]:
        if domain["domain_id"] == target:
            return {
                "status": "completed",
                "domain_id": domain["domain_id"],
                "candidate_only": True,
                "publish_ready": False,
                "real_collection_performed": False,
                "domain": domain,
            }
    return {
        "status": "failed",
        "domain_id": target,
        "error": "unknown_domain",
        "candidate_only": True,
        "publish_ready": False,
        "real_collection_performed": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Probe Piko domain registry.")
    parser.add_argument("--domain", default=None)
    parser.add_argument("--write-registry", action="store_true")
    args = parser.parse_args()
    if args.write_registry:
        write_domain_registry()
    print(json.dumps(domain_probe(args.domain), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()


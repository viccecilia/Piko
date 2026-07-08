from fastapi import APIRouter

from packages.skill_runtime.pipeline import (
    build_content_quality_package,
    build_distribution_dry_run_package,
    build_skill_runtime_registry,
    build_trace_correlation_package,
)

router = APIRouter()


@router.get("/runtime")
def skill_runtime_status() -> dict[str, object]:
    registry = build_skill_runtime_registry()
    return {
        "status": "completed",
        "runtime_version": registry["runtime_version"],
        "skill_count": len(registry["skills"]),
        "candidate_only": registry["candidate_only"],
        "external_install_performed": False,
    }


@router.get("/trace")
def skill_trace_status() -> dict[str, object]:
    package = build_trace_correlation_package()
    return {
        "status": "completed",
        "run_id": package["trace"]["run_id"],
        "verdict": package["correlation"]["verdict"],
        "secrets_recorded": False,
    }


@router.post("/quality/package")
def skill_quality_package() -> dict[str, object]:
    package = build_content_quality_package()
    return {
        "status": "completed",
        "platforms": list(package["multi_platform"]["platforms"].keys()),
        "publish_ready": False,
        "publishing_performed": False,
    }


@router.post("/distribution/dry-run")
def skill_distribution_dry_run() -> dict[str, object]:
    package = build_distribution_dry_run_package()
    return {
        "status": package["preflight_status"],
        "package_id": package["package_id"],
        "dispatch_performed": False,
        "publishing_performed": False,
        "upload_performed": False,
    }

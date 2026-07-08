from fastapi import FastAPI

from apps.api.routes.agents import router as agents_router
from apps.api.routes.capabilities import router as capabilities_router
from apps.api.routes.connectors import router as connectors_router
from apps.api.routes.demo import router as demo_router
from apps.api.routes.discovery import router as discovery_router
from apps.api.routes.domains import router as domains_router
from apps.api.routes.external_endpoint import router as external_endpoint_router
from apps.api.routes.final_mvp import router as final_mvp_router
from apps.api.routes.feedback import router as feedback_router
from apps.api.routes.gates import router as gates_router
from apps.api.routes.growth import router as growth_router
from apps.api.routes.health import router as health_router
from apps.api.routes.improvement import router as improvement_router
from apps.api.routes.local_endpoint import router as local_endpoint_router
from apps.api.routes.operator import router as operator_router
from apps.api.routes.pages import router as pages_router
from apps.api.routes.realdata import router as realdata_router
from apps.api.routes.skills import router as skills_router
from apps.api.routes.source_provider import router as source_provider_router
from apps.api.routes.tools import router as tools_router
from apps.api.routes.v03 import router as v03_router
from apps.api.routes.v04 import router as v04_router
from apps.api.routes.v05 import router as v05_router
from apps.api.routes.verification import router as verification_router
from apps.api.routes.workflow import router as workflow_router
from packages.shared.config import get_settings


settings = get_settings()

app = FastAPI(
    title="Piko API",
    version="0.1.0",
    description="Stage 1 platform skeleton for Piko.",
)

app.include_router(health_router)
app.include_router(agents_router, prefix="/agents", tags=["agents"])
app.include_router(capabilities_router, prefix="/capabilities", tags=["capabilities"])
app.include_router(connectors_router, prefix="/connectors", tags=["connectors"])
app.include_router(gates_router, prefix="/gates", tags=["gates"])
app.include_router(growth_router, prefix="/growth", tags=["growth"])
app.include_router(tools_router, prefix="/tools", tags=["tools"])
app.include_router(v03_router, prefix="/v03", tags=["v03"])
app.include_router(v04_router, prefix="/v04", tags=["v04"])
app.include_router(v05_router, prefix="/v05", tags=["v05"])
app.include_router(verification_router, prefix="/verification", tags=["verification"])
app.include_router(workflow_router, prefix="/workflow", tags=["workflow"])
app.include_router(demo_router, prefix="/demo", tags=["demo"])
app.include_router(discovery_router, prefix="/discovery", tags=["discovery"])
app.include_router(domains_router, prefix="/domains", tags=["domains"])
app.include_router(external_endpoint_router, prefix="/external-endpoint", tags=["external-endpoint"])
app.include_router(final_mvp_router, prefix="/final-mvp", tags=["final-mvp"])
app.include_router(feedback_router, prefix="/feedback", tags=["feedback"])
app.include_router(improvement_router, prefix="/improvement", tags=["improvement"])
app.include_router(local_endpoint_router, prefix="/local-endpoint", tags=["local-endpoint"])
app.include_router(operator_router, prefix="/operator", tags=["operator"])
app.include_router(pages_router, tags=["pages"])
app.include_router(realdata_router, prefix="/realdata", tags=["realdata"])
app.include_router(skills_router, prefix="/skills", tags=["skills"])
app.include_router(source_provider_router, prefix="/source-provider", tags=["source-provider"])


@app.get("/")
def root() -> dict[str, str]:
    return {"service": settings.app_name, "stage": settings.stage}

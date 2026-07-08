from packages.shared.schemas import ToolDefinition


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolDefinition] = {}

    def register(self, tool: ToolDefinition) -> None:
        self._tools[tool.name] = tool

    def list_tools(self) -> list[ToolDefinition]:
        return list(self._tools.values())


tool_registry = ToolRegistry()
for _tool in [
    ToolDefinition(name="mock_source_lookup", purpose="Return mock source IDs for Stage 1.", external_api=False),
    ToolDefinition(name="mock_evidence_extractor", purpose="Create mock evidence cards.", external_api=False),
    ToolDefinition(name="mock_gate_runner", purpose="Run quality gates against an article brief.", external_api=False),
    ToolDefinition(name="mock_workflow_runner", purpose="Run the article pipeline skeleton.", external_api=False),
]:
    tool_registry.register(_tool)


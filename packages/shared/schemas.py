from datetime import date, datetime, timezone
from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, Field


class AgentName(str, Enum):
    keyword = "keyword_agent"
    pain = "pain_agent"
    source = "source_agent"
    evidence = "evidence_agent"
    conflict = "conflict_agent"
    ranking = "ranking_agent"
    writer = "writer_agent"
    editor = "editor_agent"
    factcheck = "factcheck_agent"


class GateDecision(str, Enum):
    passed = "pass"
    failed = "fail"


class RunStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"


class PublishDecisionValue(str, Enum):
    do_not_publish = "do_not_publish"
    needs_more_evidence = "needs_more_evidence"
    verification_failed = "verification_failed"
    verified_candidate = "verified_candidate"
    draft_review = "draft_review"


class VerificationStatus(str, Enum):
    passed = "pass"
    failed = "fail"
    warning = "warning"


class ImprovementPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class UpgradeRisk(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class AgentDefinition(BaseModel):
    name: str
    label: str
    purpose: str
    version: str = "v1"
    placeholder: bool = True


class ToolDefinition(BaseModel):
    name: str
    purpose: str
    external_api: bool = False
    enabled: bool = True


class AgentRunRequest(BaseModel):
    game_id: str = "game_mock_001"
    game_name: str = "Example Game"
    topic: str = "crash on startup"
    payload: dict[str, Any] = Field(default_factory=dict)


class AgentRunResponse(BaseModel):
    agent: str
    output: dict[str, Any]
    source_ids: list[str] = Field(default_factory=list)
    mock: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class GameContext(BaseModel):
    game_id: str = "game_mock_001"
    game_name: str = "Example Game"
    platform: str | None = None
    version: str | None = None


class SourceReference(BaseModel):
    source_id: str
    source_type: str = "mock"
    title: str | None = None
    url: str | None = None
    retrieved_at: datetime | None = None
    trust_tier: str = "mock"
    snippet: str | None = None
    clean_text: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class EvidenceCard(BaseModel):
    evidence_card_id: str
    source_id: str
    claim_type: str
    claim: str | None = None
    source_type: str | None = None
    url: str | None = None
    retrieved_at: datetime | None = None
    symptom: str | None = None
    solution: str | None = None
    platform: str | None = None
    version: str | None = None
    confidence: int = Field(default=0, ge=0, le=100)
    risk_note: str | None = None


class ConflictRecord(BaseModel):
    conflict_id: str
    description: str
    severity: Literal["low", "medium", "high"] = "low"
    source_ids: list[str] = Field(default_factory=list)
    resolved: bool = False


class RankedSolution(BaseModel):
    rank: int
    solution: str
    confidence: int = Field(ge=0, le=100)
    risk_level: Literal["low", "medium", "high"]
    source_ids: list[str]


class DraftArtifact(BaseModel):
    format: str = "markdown"
    title: str | None = None
    body: str = ""
    used_raw_sources: bool = False
    publishing_performed: bool = False


class ArticleBrief(BaseModel):
    topic_id: str = "topic_mock_001"
    game_id: str = "game_mock_001"
    game_name: str = "Example Game"
    title: str = "Example Game Crash on Startup Fix"
    article_intent: str = "Help Windows players fix startup crash in Example Game."
    problem_statement: str = "The player cannot reliably start the game."
    primary_user_pain: str = "Players cannot enter the game after clicking Play."
    quick_answer: list[str] = Field(
        default_factory=lambda: [
            "Verify game files",
            "Disable Steam Overlay",
            "Update GPU driver",
        ]
    )
    ranked_solutions: list[RankedSolution] = Field(
        default_factory=lambda: [
            RankedSolution(
                rank=1,
                solution="Verify game files",
                confidence=82,
                risk_level="low",
                source_ids=["source_mock_official", "source_mock_forum"],
            ),
            RankedSolution(
                rank=2,
                solution="Disable Steam Overlay",
                confidence=74,
                risk_level="low",
                source_ids=["source_mock_discussion", "source_mock_wiki"],
            ),
        ]
    )
    do_not_recommend: list[str] = Field(
        default_factory=lambda: [
            "Download unknown DLL files",
            "Replace executable files from unofficial sources",
        ]
    )
    platform: str = "windows"
    confidence: int = Field(default=78, ge=0, le=100)
    last_checked: date = Field(default_factory=date.today)
    risk_notes: list[str] = Field(default_factory=lambda: ["Avoid unknown DLL downloads or executable replacement."])
    source_summary: list[str] = Field(default_factory=list)
    unresolved_questions: list[str] = Field(default_factory=list)
    evidence_gaps: list[str] = Field(default_factory=list)


class GateResult(BaseModel):
    gate: str
    decision: GateDecision
    score: int = Field(ge=0, le=100)
    reasons: list[str] = Field(default_factory=list)
    blocks_publish: bool = False


class AgentRunRecord(BaseModel):
    agent: str
    version: str = "v1"
    input_summary: dict[str, Any] = Field(default_factory=dict)
    output: dict[str, Any] = Field(default_factory=dict)
    status: RunStatus = RunStatus.completed
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    ended_at: datetime | None = None
    duration_ms: int | None = Field(default=None, ge=0)
    error: str | None = None


class GateRunRecord(BaseModel):
    gate: str
    input_summary: dict[str, Any] = Field(default_factory=dict)
    result: GateResult
    status: RunStatus = RunStatus.completed
    duration_ms: int | None = Field(default=None, ge=0)
    error: str | None = None


class WorkflowStartRequest(BaseModel):
    game_id: str = "game_mock_001"
    game_name: str = "Example Game"
    topic: str = "crash on startup"


class ArticleWorkflowRequest(BaseModel):
    game_id: str
    game_name: str
    player_question: str = Field(min_length=1)
    article_intent: str | None = None
    candidate_id: str | None = None
    cluster_id: str | None = None
    source_query_hints: list[str] = Field(default_factory=list)
    safety_metadata: dict[str, Any] = Field(default_factory=dict)
    publish_ready: bool = False
    publishing_performed: bool = False
    real_collection_performed: bool = False


class PublishDecision(BaseModel):
    value: PublishDecisionValue
    recommended_next_action: str
    reasons: list[str] = Field(default_factory=list)
    blocks_publish: bool = True


class VerificationCheck(BaseModel):
    name: str
    status: VerificationStatus
    message: str
    details: dict[str, Any] = Field(default_factory=dict)


class VerificationReport(BaseModel):
    status: VerificationStatus
    checks: list[VerificationCheck]
    summary: str
    workflow: str | None = None
    run_id: str | None = None


class PublishingEligibility(BaseModel):
    eligible: bool
    state: str
    reasons: list[str] = Field(default_factory=list)
    deploy_performed: bool = False


class FeedbackRequest(BaseModel):
    article_id: str
    helpful: bool | None = None
    outdated: bool = False
    did_not_work: bool = False
    missing_info: bool = False
    comment: str | None = Field(default=None, max_length=1000)


class FeedbackRecord(FeedbackRequest):
    feedback_id: str
    stored_as_signal_only: bool = True


class MultiGameJob(BaseModel):
    job_id: str
    game_id: str = Field(min_length=1)
    game_name: str = Field(min_length=1)
    locale: str = "en-US"
    question_cluster: str
    run_parameters: dict[str, Any] = Field(default_factory=dict)


class RunMonitoringSummary(BaseModel):
    total_duration_ms: int = 0
    status: RunStatus = RunStatus.completed
    warning_count: int = 0
    error_count: int = 0
    estimated_tokens: int = 0


class PipelineState(BaseModel):
    run_id: str = "run_mock_001"
    workflow: str = "article_pipeline_v1"
    status: RunStatus = RunStatus.pending
    player_question: str = "crash on startup"
    game: GameContext = Field(default_factory=GameContext)
    intent: str | None = None
    sources: list[SourceReference] = Field(default_factory=list)
    evidence_cards: list[EvidenceCard] = Field(default_factory=list)
    conflicts: list[ConflictRecord] = Field(default_factory=list)
    ranked_steps: list[RankedSolution] = Field(default_factory=list)
    draft: DraftArtifact | None = None
    article_brief: ArticleBrief | None = None
    agent_runs: list[AgentRunRecord] = Field(default_factory=list)
    gate_results: list[GateRunRecord] = Field(default_factory=list)
    decision: str | None = None
    publish_decision: PublishDecision | None = None
    verification_report: VerificationReport | None = None
    monitoring_summary: RunMonitoringSummary | None = None
    steps: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)


class WorkflowRunReport(BaseModel):
    workflow: str
    status: Literal["completed", "failed"]
    steps: list[str]
    agent_outputs: dict[str, dict[str, Any]]
    article_brief: ArticleBrief
    gate_results: list[GateResult]
    publish_action: Literal["draft_review", "auto_publish_disabled", "store_only", "discard"]
    pipeline_state: PipelineState
    publish_decision: PublishDecision | None = None
    verification_report: VerificationReport | None = None


class WorkflowRunResult(WorkflowRunReport):
    """Backward-compatible response name for the Stage 0 API contract."""


class ImprovementSignal(BaseModel):
    signal_id: str
    source: str = "verification_report"
    priority: ImprovementPriority
    failed_check: str | None = None
    warning: str | None = None
    risk: str | None = None
    suggested_fix: str
    affected_module: str
    evidence: dict[str, Any] = Field(default_factory=dict)


class DiagnosticReport(BaseModel):
    diagnostic_id: str
    source_workflow: str | None = None
    run_id: str | None = None
    status: Literal["no_action", "needs_improvement"] = "no_action"
    signals: list[ImprovementSignal] = Field(default_factory=list)
    summary: str = ""


class UpgradeProposal(BaseModel):
    proposal_id: str
    diagnostic_id: str
    title: str
    reason: str
    affected_modules: list[str] = Field(default_factory=list)
    expected_benefit: str
    risk: UpgradeRisk = UpgradeRisk.low
    required_tests: list[str] = Field(default_factory=list)
    auto_apply_allowed: bool = False
    requires_operator_decision: bool = True


class PatchPlanStep(BaseModel):
    step_id: str
    target_file: str
    change_summary: str
    reason: str
    verification: str


class RegressionCommand(BaseModel):
    command: str
    purpose: str
    destructive: bool = False
    auto_execute: bool = False


class PatchPlan(BaseModel):
    plan_id: str
    proposal_id: str
    summary: str
    steps: list[PatchPlanStep] = Field(default_factory=list)
    regression_commands: list[RegressionCommand] = Field(default_factory=list)
    auto_apply_allowed: bool = False


class RegressionResult(BaseModel):
    command: str
    status: Literal["planned", "passed", "failed", "skipped"] = "planned"
    output_summary: str = ""


class UpgradeLedgerEntry(BaseModel):
    ledger_id: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    proposal: UpgradeProposal
    patch_plan: PatchPlan
    regression_plan: list[RegressionCommand] = Field(default_factory=list)
    status: Literal["proposed", "operator_approved", "rejected", "applied", "verified"] = "proposed"
    notes: list[str] = Field(default_factory=list)


class DiscoveryDecision(str, Enum):
    publish_candidate = "publish_candidate"
    watchlist_waiting_for_answer = "watchlist_waiting_for_answer"
    conflict_explainer = "conflict_explainer"
    evergreen_candidate = "evergreen_candidate"
    rising_opportunity = "rising_opportunity"
    blocked_high_risk = "blocked_high_risk"
    insufficient_evidence = "insufficient_evidence"
    ignore = "ignore"


class AnswerStatus(str, Enum):
    answered = "answered"
    unanswered = "unanswered"
    conflicting = "conflicting"
    partial = "partial"
    unknown = "unknown"


class GameHeatSignal(BaseModel):
    game_id: str
    game_name: str
    region_signals: list[str] = Field(default_factory=list)
    steam_player_rank: int | None = None
    steam_review_velocity: int = 0
    community_post_velocity: int = 0
    update_recency_days: int | None = None
    cross_region_mentions: int = 0
    heat_score: int = Field(default=0, ge=0, le=100)
    reasons: list[str] = Field(default_factory=list)


class PlayerQuestionSignal(BaseModel):
    question_id: str
    game_id: str
    game_name: str
    question_text: str
    source_type: str
    source_region: str = "global"
    source_title: str | None = None
    language: str | None = None
    url: str | None = None
    created_at: datetime | None = None
    engagement_count: int = 0
    reply_count: int = 0
    duplicate_count: int = 1
    growth_24h: int = 0
    has_accepted_answer: bool = False
    has_official_answer: bool = False
    answer_conflict_count: int = 0
    evidence_quality: int = Field(default=0, ge=0, le=100)
    competition_gap: int = Field(default=50, ge=0, le=100)
    piko_value_add_score: int = Field(default=50, ge=0, le=100)
    risk_level: Literal["low", "medium", "high"] = "low"
    tags: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    snippet: str | None = Field(default=None, max_length=500)


class PlayerNeedCluster(BaseModel):
    cluster_id: str
    game_id: str
    game_name: str
    need_key: str
    search_intent: Literal[
        "bug_fix",
        "location",
        "walkthrough",
        "build",
        "settings",
        "compatibility",
        "save_file",
        "map_exploration",
        "hidden_item",
        "quest_blocker",
    ] = "walkthrough"
    normalization_hints: list[str] = Field(default_factory=list)
    representative_question: str
    representative_question_id: str | None = None
    representative_questions: list[str] = Field(default_factory=list)
    source_types: list[str] = Field(default_factory=list)
    source_regions: list[str] = Field(default_factory=list)
    source_diversity_count: int = 0
    region_signal_summary: dict[str, Any] = Field(default_factory=dict)
    region_signal_score: int = Field(default=0, ge=0, le=100)
    cross_region_repeat: bool = False
    language_gap_opportunity: bool = False
    source_coverage: dict[str, Any] = Field(default_factory=dict)
    duplicate_count: int = 0
    question_ids: list[str] = Field(default_factory=list)
    heat_score: int = Field(ge=0, le=100)
    frequency_score: int = Field(ge=0, le=100)
    urgency_score: int = Field(ge=0, le=100)
    evidence_quality: int = Field(ge=0, le=100)
    freshness_score: int = Field(default=0, ge=0, le=100)
    conflict_score: int = Field(default=0, ge=0, le=100)
    evergreen_value: int = Field(default=0, ge=0, le=100)
    competition_gap: int = Field(default=50, ge=0, le=100)
    competition_gap_status: Literal["strong", "weak", "fragmented", "stale", "absent"] = "weak"
    actionability_score: int = Field(default=0, ge=0, le=100)
    piko_value_add_score: int = Field(default=50, ge=0, le=100)
    content_opportunity_score: int = Field(default=0, ge=0, le=100)
    content_opportunity_reasons: list[str] = Field(default_factory=list)
    risk_level: Literal["low", "medium", "high"]
    answer_status: AnswerStatus
    topic_lifecycle: Literal["new", "rising", "stable", "declining", "resolved", "stale"] = "new"
    actionability_label: Literal[
        "single_page_answerable",
        "needs_more_sources",
        "too_broad",
        "too_risky",
        "too_visual",
    ] = "needs_more_sources"
    actionability_reasons: list[str] = Field(default_factory=list)
    decision: DiscoveryDecision
    recommended_article_intent: str
    monitor_reason: str | None = None
    piko_value_add: list[str] = Field(default_factory=list)
    score_inputs: dict[str, Any] = Field(default_factory=dict)
    topic_score_components: dict[str, Any] = Field(default_factory=dict)
    recommended_next_action: str = "review_candidate"
    publish_ready: bool = False
    requires_evidence_pipeline: bool = True
    safety_notes: list[str] = Field(default_factory=list)
    source_search_hints: list[str] = Field(default_factory=list)
    reasons: list[str] = Field(default_factory=list)


class DiscoverySearchRequest(BaseModel):
    game_name: str | None = None
    query: str | None = None
    regions: list[str] = Field(default_factory=list)
    source_types: list[str] = Field(default_factory=list)
    search_intents: list[
        Literal[
            "bug_fix",
            "location",
            "walkthrough",
            "build",
            "settings",
            "compatibility",
            "save_file",
            "map_exploration",
            "hidden_item",
            "quest_blocker",
        ]
    ] = Field(default_factory=list)
    topic_lifecycles: list[Literal["new", "rising", "stable", "declining", "resolved", "stale"]] = Field(default_factory=list)
    actionability_labels: list[
        Literal[
            "single_page_answerable",
            "needs_more_sources",
            "too_broad",
            "too_risky",
            "too_visual",
        ]
    ] = Field(default_factory=list)
    min_game_heat: int = Field(default=0, ge=0, le=100)
    min_question_heat: int = Field(default=0, ge=0, le=100)
    min_content_opportunity_score: int = Field(default=0, ge=0, le=100)
    answer_statuses: list[AnswerStatus] = Field(default_factory=list)
    decisions: list[DiscoveryDecision] = Field(default_factory=list)
    limit: int = Field(default=20, ge=1, le=100)


class DiscoverySearchResponse(BaseModel):
    status: Literal["completed"] = "completed"
    mode: Literal["fixture", "real-source-disabled", "real-source"] = "fixture"
    game_candidates: list[GameHeatSignal]
    clusters: list[PlayerNeedCluster]
    funnel_counts: dict[str, int] = Field(default_factory=dict)
    real_collection_performed: bool = False
    next_actions: list[str] = Field(default_factory=list)


class DiscoveryWatchlistItem(BaseModel):
    watchlist_id: str
    cluster_id: str
    game_name: str
    player_question: str
    reason: str
    state: Literal["watching", "answer_seen", "evidence_ready", "stale", "closed"] = "watching"
    refresh_interval_hours: int = 24
    next_check_reason: str = "Waiting for credible answer or stronger evidence."
    trigger_conditions: list[str] = Field(default_factory=list)
    promotion_triggers: list[str] = Field(default_factory=list)
    state_transitions: dict[str, str] = Field(default_factory=dict)
    last_seen_signals: dict[str, Any] = Field(default_factory=dict)
    publish_ready: bool = False
    requires_evidence_pipeline: bool = True


class DiscoveryArticleCandidate(BaseModel):
    candidate_id: str
    cluster_id: str
    game_id: str
    game_name: str
    need_key: str
    search_intent: Literal[
        "bug_fix",
        "location",
        "walkthrough",
        "build",
        "settings",
        "compatibility",
        "save_file",
        "map_exploration",
        "hidden_item",
        "quest_blocker",
    ] = "walkthrough"
    normalization_hints: list[str] = Field(default_factory=list)
    player_question: str
    article_intent: str
    decision: DiscoveryDecision
    answer_status: AnswerStatus
    risk_level: Literal["low", "medium", "high"]
    candidate_type: Literal[
        "solution_candidate",
        "synthesis_candidate",
        "watchlist_only",
        "blocked_safety_note",
        "evidence_gap_candidate",
        "monitoring_candidate",
        "ignored",
    ] = "solution_candidate"
    runnable: bool = False
    source_search_hints: list[str] = Field(default_factory=list)
    source_query_hints: list[str] = Field(default_factory=list)
    required_source_types: list[str] = Field(default_factory=list)
    preferred_source_types: list[str] = Field(default_factory=list)
    source_regions: list[str] = Field(default_factory=list)
    risk_flags: list[str] = Field(default_factory=list)
    safety_flags: list[str] = Field(default_factory=list)
    safety_reasons: list[str] = Field(default_factory=list)
    piko_value_add: list[str] = Field(default_factory=list)
    cluster_reasons: list[str] = Field(default_factory=list)
    score_inputs: dict[str, Any] = Field(default_factory=dict)
    publish_ready: bool = False
    requires_evidence_pipeline: bool = True
    safety_notes: list[str] = Field(default_factory=list)


class DiscoveryRetrospectiveReport(BaseModel):
    status: Literal["completed"] = "completed"
    decision_counts: dict[str, int] = Field(default_factory=dict)
    publish_candidate_count: int = 0
    watchlist_count: int = 0
    blocked_high_risk_count: int = 0
    weak_source_count: int = 0
    recommendations: list[str] = Field(default_factory=list)
    real_collection_performed: bool = False

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any

from packages.discovery.fixtures import load_discovery_fixtures
from packages.discovery.search_engine import search_player_needs
from packages.shared.schemas import DiscoverySearchRequest, PlayerNeedCluster


SOURCE_PLAN = [
    {
        "platform": "Steam",
        "platform_label": "Steam 社区与热度榜",
        "signal_type": "热门游戏、讨论帖热度、玩家问题、回复数、增长速度",
        "status": "当前为本地镜像/fixture；真实采集需要显式 opt-in 和批准 JSON endpoint",
    },
    {
        "platform": "Reddit",
        "platform_label": "Reddit 讨论区",
        "signal_type": "帖子热度、评论密度、重复问题、答案冲突",
        "status": "当前为本地镜像/fixture；真实采集需要显式 opt-in 和批准 JSON endpoint",
    },
    {
        "platform": "SERP snippets",
        "platform_label": "搜索结果摘要",
        "signal_type": "搜索需求、已有答案线索、竞品内容缺口",
        "status": "只保留短摘要和结构化指标，不保存完整网页正文",
    },
    {
        "platform": "JP community",
        "platform_label": "日文玩家社区",
        "signal_type": "日文重复问题、跨语言痛点、语言缺口机会",
        "status": "当前为本地镜像/fixture；不调用翻译 API，不默认调用 LLM",
    },
    {
        "platform": "KR community",
        "platform_label": "韩文玩家社区",
        "signal_type": "韩文重复问题、地区热度、跨地区共振",
        "status": "当前为本地镜像/fixture；不调用翻译 API，不默认调用 LLM",
    },
    {
        "platform": "Wiki comments / official forums",
        "platform_label": "Wiki 评论与官方论坛",
        "signal_type": "答案成熟度、官方/可信答案、证据质量",
        "status": "只进入证据候选链，不直接构成发布许可",
    },
]

DECISION_LABELS = {
    "publish_candidate": "可写攻略候选",
    "watchlist_waiting_for_answer": "高热未解决，进入监控",
    "conflict_explainer": "答案冲突，适合解释",
    "evergreen_candidate": "长期常青候选",
    "rising_opportunity": "快速上升机会",
    "blocked_high_risk": "高风险阻断",
    "insufficient_evidence": "证据不足，继续收集",
    "ignore": "暂不处理",
}

ANSWER_STATUS_LABELS = {
    "answered": "已有答案",
    "unanswered": "未解决",
    "conflicting": "答案冲突",
    "partial": "部分答案",
    "unknown": "状态未知",
}

RISK_LABELS = {
    "low": "低风险",
    "medium": "中风险",
    "high": "高风险",
}

ACTION_LABELS = {
    "send_to_evidence_pipeline": "送入证据流水线",
    "add_to_watchlist": "加入监控区",
    "prepare_conflict_brief": "准备冲突答案解释",
    "block_publish_and_prepare_safety_note": "阻断发布并准备安全提示",
    "queue_evergreen_evidence_review": "排队做常青证据复核",
    "monitor_and_collect_evidence": "持续监控并补证据",
    "collect_more_evidence": "继续收集证据",
    "no_action": "暂不处理",
}


def _enum_value(value: Any) -> Any:
    return value.value if hasattr(value, "value") else value


def _cluster_card(cluster: PlayerNeedCluster) -> dict[str, Any]:
    decision = str(_enum_value(cluster.decision))
    answer_status = str(_enum_value(cluster.answer_status))
    next_action = str(cluster.recommended_next_action)
    return {
        "cluster_id": cluster.cluster_id,
        "game_name": cluster.game_name,
        "need_key": cluster.need_key,
        "representative_question": cluster.representative_question,
        "question_ids": cluster.question_ids,
        "source_types": cluster.source_types,
        "source_regions": cluster.source_regions,
        "answer_status": answer_status,
        "answer_status_label": ANSWER_STATUS_LABELS.get(answer_status, answer_status),
        "risk_level": cluster.risk_level,
        "risk_label": RISK_LABELS.get(cluster.risk_level, cluster.risk_level),
        "decision": decision,
        "decision_label": DECISION_LABELS.get(decision, decision),
        "recommended_next_action": next_action,
        "recommended_next_action_label": ACTION_LABELS.get(next_action, next_action),
        "heat_score": cluster.heat_score,
        "evidence_quality": cluster.evidence_quality,
        "content_opportunity_score": cluster.content_opportunity_score,
        "topic_score_components": cluster.topic_score_components,
        "content_opportunity_reasons": cluster.content_opportunity_reasons,
        "piko_value_add": cluster.piko_value_add,
        "source_search_hints": cluster.source_search_hints,
        "safety_notes": cluster.safety_notes,
        "reasons": cluster.reasons,
        "publish_ready": cluster.publish_ready,
        "requires_evidence_pipeline": cluster.requires_evidence_pipeline,
        "plain_summary": (
            f"{cluster.game_name} 的 {cluster.need_key} 被判定为"
            f"「{DECISION_LABELS.get(decision, decision)}」。"
            f"热度 {cluster.heat_score}，证据质量 {cluster.evidence_quality}，"
            f"机会分 {cluster.content_opportunity_score}，风险为 {RISK_LABELS.get(cluster.risk_level, cluster.risk_level)}。"
        ),
    }


def _top_by_decision(clusters: list[PlayerNeedCluster]) -> dict[str, list[dict[str, Any]]]:
    buckets: dict[str, list[PlayerNeedCluster]] = defaultdict(list)
    for cluster in clusters:
        buckets[str(_enum_value(cluster.decision))].append(cluster)
    return {
        DECISION_LABELS.get(decision, decision): [
            _cluster_card(cluster)
            for cluster in sorted(items, key=lambda item: item.content_opportunity_score, reverse=True)[:3]
        ]
        for decision, items in sorted(buckets.items())
    }


def discovery_funnel_trace(request: DiscoverySearchRequest | None = None) -> dict[str, Any]:
    request = request or DiscoverySearchRequest(min_game_heat=50, limit=20)
    raw_games, raw_questions = load_discovery_fixtures()
    result = search_player_needs(request)
    clusters = result.clusters
    decision_counts = Counter(str(_enum_value(cluster.decision)) for cluster in clusters)
    source_type_counts = Counter(question.source_type for question in raw_questions)
    source_region_counts = Counter(question.source_region for question in raw_questions)
    selected_publish = [cluster for cluster in clusters if str(_enum_value(cluster.decision)) == "publish_candidate"]
    selected_watchlist = [cluster for cluster in clusters if str(_enum_value(cluster.decision)) == "watchlist_waiting_for_answer"]
    selected_conflict = [cluster for cluster in clusters if str(_enum_value(cluster.decision)) == "conflict_explainer"]
    selected_high_risk = [cluster for cluster in clusters if str(_enum_value(cluster.decision)) == "blocked_high_risk"]
    first_solution = selected_publish[0] if selected_publish else (clusters[0] if clusters else None)

    steps = [
        {
            "step_id": "01-source-scan",
            "title": "大范围来源扫描",
            "agent_action": "SourceAgent 先决定要观察哪些来源族，并把本次运行限定为候选信号分析。",
            "inputs": {
                "关键词": request.query,
                "最低游戏热度": request.min_game_heat,
                "最多返回 topic": request.limit,
            },
            "outputs": {
                "计划观察的平台": SOURCE_PLAN,
                "platforms": SOURCE_PLAN,
                "是否发生真实采集": result.real_collection_performed,
                "real_collection_performed": result.real_collection_performed,
                "运行模式": result.mode,
                "mode": result.mode,
            },
            "guardrails": [
                "默认只使用 fixture/批准镜像数据。",
                "真实采集必须显式 opt-in，并且只能使用批准的 JSON endpoint。",
                "No crawler / 不 crawler、不抓完整帖子或网页正文、不发布。",
            ],
        },
        {
            "step_id": "02-raw-signals",
            "title": "读取热度和问题信号",
            "agent_action": "Collector 适配器把不同平台的热度和玩家问题统一成结构化记录。",
            "inputs": {"来源计划": [item["platform_label"] for item in SOURCE_PLAN]},
            "outputs": {
                "游戏信号数量": len(raw_games),
                "raw_game_count": len(raw_games),
                "玩家问题信号数量": len(raw_questions),
                "raw_question_count": len(raw_questions),
                "来源类型统计": dict(sorted(source_type_counts.items())),
                "source_type_counts": dict(sorted(source_type_counts.items())),
                "来源地区统计": dict(sorted(source_region_counts.items())),
                "source_region_counts": dict(sorted(source_region_counts.items())),
                "示例游戏信号": [game.model_dump(mode="json") for game in raw_games[:5]],
                "sample_games": [game.model_dump(mode="json") for game in raw_games[:5]],
                "示例问题信号": [question.model_dump(mode="json") for question in raw_questions[:8]],
                "sample_questions": [question.model_dump(mode="json") for question in raw_questions[:8]],
            },
            "guardrails": ["只保留有边界的短摘要和结构化指标，不保存长篇原文。"],
        },
        {
            "step_id": "03-cluster",
            "title": "相似问题聚类去重",
            "agent_action": "DiscoveryAgent 按游戏和问题类型把重复表达合并成 topic cluster。",
            "inputs": {
                "游戏数量": len(raw_games),
                "问题数量": len(raw_questions),
            },
            "outputs": {
                "聚类 topic 数量": len(clusters),
                "cluster_count": len(clusters),
                "聚类结果": [_cluster_card(cluster) for cluster in clusters],
                "clusters": [_cluster_card(cluster) for cluster in clusters],
            },
            "guardrails": ["聚类结果仍然只是发现信号，不等于文章审批通过。"],
        },
        {
            "step_id": "04-score",
            "title": "热度、证据、风险和机会评分",
            "agent_action": "ScoringAgent 计算热度、答案成熟度、证据质量、风险、竞争缺口和 Piko 可增加价值。",
            "inputs": {
                "评分因子": [
                    "游戏热度",
                    "问题热度",
                    "答案状态",
                    "证据质量",
                    "风险等级",
                    "新鲜度",
                    "竞争内容缺口",
                    "Piko 可增加价值",
                ],
            },
            "outputs": {
                "漏斗结论统计": {
                    DECISION_LABELS.get(decision, decision): count
                    for decision, count in sorted(decision_counts.items())
                },
                "decision_counts": dict(sorted(decision_counts.items())),
                "各结论代表 topic": _top_by_decision(clusters),
                "top_by_decision": _top_by_decision(clusters),
            },
            "guardrails": [
                "高风险 topic 会被阻断，不能进入普通攻略生成。",
                "高热但未解决的 topic 进入监控区，等可信答案出现后再处理。",
            ],
        },
        {
            "step_id": "05-funnel-routing",
            "title": "漏斗分流",
            "agent_action": "RouterAgent 把每个 topic 分到可写攻略、监控区、冲突解释、高风险阻断或暂不处理。",
            "inputs": {"聚类 topic 数量": len(clusters)},
            "outputs": {
                "可写攻略候选": [_cluster_card(cluster) for cluster in selected_publish],
                "publish_candidates": [_cluster_card(cluster) for cluster in selected_publish],
                "监控区": [_cluster_card(cluster) for cluster in selected_watchlist],
                "watchlist": [_cluster_card(cluster) for cluster in selected_watchlist],
                "冲突解释": [_cluster_card(cluster) for cluster in selected_conflict],
                "conflict_explainers": [_cluster_card(cluster) for cluster in selected_conflict],
                "高风险阻断": [_cluster_card(cluster) for cluster in selected_high_risk],
                "high_risk_blocked": [_cluster_card(cluster) for cluster in selected_high_risk],
            },
            "guardrails": ["publish_ready 仍然是 false；后续必须经过证据流水线和验证 Gate。"],
        },
        {
            "step_id": "06-solution-path",
            "title": "进入解决方案分析",
            "agent_action": "对安全候选题，ArticlePipeline 还要继续收集证据、排序步骤、写作、编辑和事实核查，最后才可能进入发布候选。",
            "inputs": {"选中的示例 topic": _cluster_card(first_solution) if first_solution else None},
            "outputs": {
                "计划经过的 Agent 路径": [
                    "SourceAgent：找来源",
                    "EvidenceAgent：生成证据卡片",
                    "RankingAgent：排序解决步骤",
                    "WriterAgent：生成草稿",
                    "EditorAgent：改写成可读文章",
                    "FactcheckAgent：核查 claims",
                    "VerificationGate：最终验证",
                ],
                "planned_agent_path": [
                    "SourceAgent",
                    "EvidenceAgent",
                    "RankingAgent",
                    "WriterAgent",
                    "EditorAgent",
                    "FactcheckAgent",
                    "VerificationGate",
                ],
                "交接必须包含": [
                    "来源搜索提示",
                    "source ids",
                    "evidence cards",
                    "claim trace",
                    "verification report",
                ],
                "handoff_requirements": [
                    "source_search_hints",
                    "source ids",
                    "evidence cards",
                    "claim trace",
                    "verification report",
                ],
            },
            "guardrails": [
                "Discovery 本身不能直接公开发布。",
                "文章必须通过验证，才可能成为 public-ready candidate。",
            ],
        },
    ]

    return {
        "status": "completed",
        "title": "Piko 漏斗透明轨迹",
        "mode": result.mode,
        "real_collection_performed": result.real_collection_performed,
        "publish_ready": False,
        "publishing_performed": False,
        "request": request.model_dump(mode="json"),
        "summary": {
            "平台族数量": len(SOURCE_PLAN),
            "platform_count": len(SOURCE_PLAN),
            "游戏信号数量": len(raw_games),
            "raw_game_count": len(raw_games),
            "玩家问题信号数量": len(raw_questions),
            "raw_question_count": len(raw_questions),
            "聚类 topic 数量": len(clusters),
            "cluster_count": len(clusters),
            "漏斗结论统计": {
                DECISION_LABELS.get(decision, decision): count
                for decision, count in sorted(decision_counts.items())
            },
            "decision_counts": dict(sorted(decision_counts.items())),
        },
        "steps": steps,
    }

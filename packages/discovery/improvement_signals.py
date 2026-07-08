from packages.shared.schemas import ImprovementPriority, ImprovementSignal, PlayerNeedCluster


def improvement_signals_from_discovery(clusters: list[PlayerNeedCluster]) -> list[ImprovementSignal]:
    signals: list[ImprovementSignal] = []
    for cluster in clusters:
        if cluster.evidence_quality < 45:
            signals.append(
                ImprovementSignal(
                    signal_id=f"discovery_weak_source_{cluster.cluster_id.replace(':', '_')}",
                    source="discovery",
                    priority=ImprovementPriority.medium,
                    warning="weak_source_quality",
                    suggested_fix="Add higher-trust, source-traceable evidence before drafting.",
                    affected_module="packages/discovery/search_engine.py",
                    evidence={
                        "cluster_id": cluster.cluster_id,
                        "decision": cluster.decision.value,
                        "evidence_quality": cluster.evidence_quality,
                    },
                )
            )
        if cluster.decision.value == "blocked_high_risk":
            signals.append(
                ImprovementSignal(
                    signal_id=f"discovery_high_risk_{cluster.cluster_id.replace(':', '_')}",
                    source="discovery",
                    priority=ImprovementPriority.high,
                    risk="high_risk_player_advice",
                    suggested_fix="Keep risky advice blocked and prepare safer alternatives.",
                    affected_module="packages/discovery/search_engine.py",
                    evidence={
                        "cluster_id": cluster.cluster_id,
                        "risk_level": cluster.risk_level,
                        "publish_ready": False,
                    },
                )
            )
    return signals

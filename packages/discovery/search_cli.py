import argparse
import json

from packages.discovery.search_engine import search_player_needs
from packages.discovery.search_engine import discovery_retrospective_report
from packages.shared.schemas import DiscoveryDecision, DiscoverySearchRequest

SEARCH_INTENT_CHOICES = [
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

LIFECYCLE_CHOICES = ["new", "rising", "stable", "declining", "resolved", "stale"]

ACTIONABILITY_CHOICES = [
    "single_page_answerable",
    "needs_more_sources",
    "too_broad",
    "too_risky",
    "too_visual",
]


def _summary_view(payload: dict) -> str:
    lines = ["decision\tintent\tgame\tneed_key\topportunity\theat\tevidence\tactionability\trisk"]
    for cluster in payload["clusters"]:
        lines.append(
            "\t".join(
                [
                    cluster["decision"],
                    cluster["search_intent"],
                    cluster["game_name"],
                    cluster["need_key"],
                    str(cluster["content_opportunity_score"]),
                    str(cluster["heat_score"]),
                    str(cluster["evidence_quality"]),
                    cluster["actionability_label"],
                    cluster["risk_level"],
                ]
            )
        )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Search player pain clusters through the Piko discovery funnel.")
    parser.add_argument("--query", default=None)
    parser.add_argument("--decision", action="append", choices=[item.value for item in DiscoveryDecision])
    parser.add_argument("--intent", action="append", choices=SEARCH_INTENT_CHOICES)
    parser.add_argument("--lifecycle", action="append", choices=LIFECYCLE_CHOICES)
    parser.add_argument("--actionability", action="append", choices=ACTIONABILITY_CHOICES)
    parser.add_argument("--min-game-heat", type=int, default=0)
    parser.add_argument("--min-question-heat", type=int, default=0)
    parser.add_argument("--min-opportunity", type=int, default=0)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--view", choices=["json", "summary"], default="json")
    parser.add_argument("--report", action="store_true")
    args = parser.parse_args()

    result = search_player_needs(
        DiscoverySearchRequest(
            query=args.query,
            decisions=[DiscoveryDecision(item) for item in args.decision or []],
            search_intents=args.intent or [],
            topic_lifecycles=args.lifecycle or [],
            actionability_labels=args.actionability or [],
            min_game_heat=args.min_game_heat,
            min_question_heat=args.min_question_heat,
            min_content_opportunity_score=args.min_opportunity,
            limit=args.limit,
        )
    )
    if args.report:
        print(json.dumps(discovery_retrospective_report(result.clusters).model_dump(mode="json"), ensure_ascii=False, indent=2))
        return
    payload = result.model_dump(mode="json")
    if args.view == "summary":
        print(_summary_view(payload))
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

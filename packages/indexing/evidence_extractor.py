from packages.collectors.local_fixtures import LocalSourceFixture


SAVE_LOCATION_PATTERNS = {
    "windows": "{{p|appdata}}\\StardewValley\\Saves\\",
    "mac": "{{p|osxhome}}/.config/StardewValley/Saves/",
    "linux": "{{p|xdgconfighome}}/StardewValley/Saves/",
}


def extract_evidence_cards_from_fixtures(fixtures: list[LocalSourceFixture]) -> list[dict[str, object]]:
    cards: list[dict[str, object]] = []
    for index, fixture in enumerate(fixtures, start=1):
        text = fixture.content.lower()
        if "verify game files" in text:
            cards.append(
                {
                    "evidence_card_id": f"ev_{fixture.source_id}_{index}_verify",
                    "source_id": fixture.source_id,
                    "claim_type": "solution",
                    "claim": "Verify game files",
                    "symptom": "crash on startup or black screen",
                    "solution": "Verify game files",
                    "platform": fixture.platform,
                    "observed_version": fixture.date,
                    "confidence": 82 if fixture.trust_tier == "official" else 70,
                    "quote_snippet": "verify game files",
                    "risk_note": "Low risk.",
                }
            )
        if "disabling steam overlay" in text or "disable steam overlay" in text:
            cards.append(
                {
                    "evidence_card_id": f"ev_{fixture.source_id}_{index}_overlay",
                    "source_id": fixture.source_id,
                    "claim_type": "solution",
                    "claim": "Disable Steam Overlay",
                    "symptom": "black screen after clicking Play",
                    "solution": "Disable Steam Overlay",
                    "platform": fixture.platform,
                    "observed_version": fixture.date,
                    "confidence": 74,
                    "quote_snippet": "Disabling Steam Overlay helped some players",
                    "risk_note": "Low risk; reversible setting.",
                }
            )
        if "proton version" in text:
            cards.append(
                {
                    "evidence_card_id": f"ev_{fixture.source_id}_{index}_proton",
                    "source_id": fixture.source_id,
                    "claim_type": "platform_note",
                    "claim": "Switch Proton version",
                    "symptom": "Steam Deck launch failure",
                    "solution": "Switch Proton version",
                    "platform": fixture.platform,
                    "observed_version": fixture.date,
                    "confidence": 68,
                    "quote_snippet": "switching Proton version can help launch failures",
                    "risk_note": "Only applies to Steam Deck / Proton contexts.",
                }
            )
    return cards


def extract_evidence_cards_from_source_records(source_records: list[dict[str, object]]) -> list[dict[str, object]]:
    cards: list[dict[str, object]] = []
    for index, record in enumerate(source_records, start=1):
        source_id = str(record.get("source_id") or "").strip()
        if not source_id:
            continue
        source_type = str(record.get("source_type") or "unknown")
        title = str(record.get("title") or "Untitled source")
        snippet = str(record.get("clean_text") or record.get("snippet") or "").strip()
        if not snippet:
            continue
        cards.append(
            {
                "evidence_card_id": f"ev_{source_id}_{index}_candidate",
                "source_id": source_id,
                "source_type": source_type,
                "url": record.get("url"),
                "retrieved_at": record.get("retrieved_at"),
                "claim_type": "source_candidate",
                "claim": f"{title} is a {source_type} source candidate for the player question.",
                "symptom": None,
                "solution": None,
                "platform": None,
                "confidence": 35,
                "quote_snippet": snippet[:300],
                "risk_note": "Source candidate only; needs page-level extraction before recommending an answer.",
                "uncertainty": "needs_more_evidence",
            }
        )
        text = snippet.lower()
        if "save game data location" in text or "game data/saves" in text:
            cards.extend(_extract_save_location_cards(record, source_id, source_type, index))
    return cards


def _extract_save_location_cards(record: dict[str, object], source_id: str, source_type: str, index: int) -> list[dict[str, object]]:
    text = str(record.get("clean_text") or record.get("snippet") or "")
    cards: list[dict[str, object]] = []
    for platform, pattern in SAVE_LOCATION_PATTERNS.items():
        if pattern.lower() not in text.lower():
            continue
        normalized_path = _normalize_pcgw_path(pattern)
        cards.append(
            {
                "evidence_card_id": f"ev_{source_id}_{index}_save_{platform}",
                "source_id": source_id,
                "source_type": source_type,
                "url": record.get("url"),
                "retrieved_at": record.get("retrieved_at"),
                "claim_type": "save_location",
                "claim": f"Stardew Valley save files are stored at {normalized_path} on {platform}.",
                "symptom": "Player needs to find or troubleshoot save files.",
                "solution": f"Check {normalized_path}",
                "platform": platform,
                "confidence": 78,
                "quote_snippet": pattern,
                "risk_note": "Low risk for locating files; back up saves before moving, deleting, or editing anything.",
            }
        )
    return cards


def _normalize_pcgw_path(path: str) -> str:
    return (
        path.replace("{{p|appdata}}", "%AppData%")
        .replace("{{p|osxhome}}", "~")
        .replace("{{p|xdgconfighome}}", "$XDG_CONFIG_HOME or ~/.config")
    )

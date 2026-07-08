import hashlib

from packages.collectors.base import ConnectorSearchResult


TRUST_TIERS = {
    "official_notes": "official",
    "pcgamingwiki": "reference",
    "mediawiki": "reference",
    "protondb": "compatibility",
    "steam_discussion": "community",
    "reddit": "community",
}


def content_hash(text: str | None) -> str | None:
    if not text:
        return None
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def assign_trust_tier(source_type: str) -> str:
    return TRUST_TIERS.get(source_type, "unknown")


def deduplicate_sources(items: list[ConnectorSearchResult]) -> list[ConnectorSearchResult]:
    seen: set[tuple[str, str, str | None]] = set()
    deduped: list[ConnectorSearchResult] = []
    for item in items:
        key = (item.url.lower(), item.title.strip().lower(), content_hash(item.clean_text or item.raw_text))
        if key in seen:
            continue
        seen.add(key)
        if item.trust_tier == "unknown":
            item.trust_tier = assign_trust_tier(item.source_type)
        deduped.append(item)
    return deduped

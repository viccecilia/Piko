from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


class Base(DeclarativeBase):
    pass


class SourceType(str, Enum):
    official_notes = "official_notes"
    steam_review = "steam_review"
    steam_news = "steam_news"
    steam_discussion = "steam_discussion"
    pcgamingwiki = "pcgamingwiki"
    protondb = "protondb"
    mediawiki = "mediawiki"
    reddit = "reddit"
    serp = "serp"
    other = "other"


class GateDecision(str, Enum):
    passed = "pass"
    failed = "fail"


class Game(Base):
    __tablename__ = "games"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: new_id("game"))
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    sources: Mapped[list["Source"]] = relationship(back_populates="game")
    articles: Mapped[list["Article"]] = relationship(back_populates="game")


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: new_id("source"))
    game_id: Mapped[str] = mapped_column(ForeignKey("games.id"), nullable=False, index=True)
    source_type: Mapped[str] = mapped_column(String(64), nullable=False)
    url: Mapped[str | None] = mapped_column(Text)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    raw_text: Mapped[str | None] = mapped_column(Text)
    clean_text: Mapped[str | None] = mapped_column(Text)
    language: Mapped[str] = mapped_column(String(16), default="en")
    platform: Mapped[str | None] = mapped_column(String(64))
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    content_hash: Mapped[str | None] = mapped_column(String(128), index=True)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)

    game: Mapped[Game] = relationship(back_populates="sources")
    evidence_cards: Mapped[list["EvidenceCard"]] = relationship(back_populates="source")


class EvidenceCard(Base):
    __tablename__ = "evidence_cards"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: new_id("ev"))
    source_id: Mapped[str] = mapped_column(ForeignKey("sources.id"), nullable=False, index=True)
    game_id: Mapped[str] = mapped_column(ForeignKey("games.id"), nullable=False, index=True)
    claim_type: Mapped[str] = mapped_column(String(64), nullable=False)
    symptom: Mapped[str | None] = mapped_column(Text)
    solution: Mapped[str | None] = mapped_column(Text)
    platform: Mapped[str | None] = mapped_column(String(64))
    version: Mapped[str | None] = mapped_column(String(64))
    confidence: Mapped[int] = mapped_column(Integer, default=0)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    source: Mapped[Source] = relationship(back_populates="evidence_cards")


class SolutionClaim(Base):
    __tablename__ = "solution_claims"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: new_id("claim"))
    game_id: Mapped[str] = mapped_column(ForeignKey("games.id"), nullable=False, index=True)
    issue: Mapped[str] = mapped_column(Text, nullable=False)
    solution: Mapped[str] = mapped_column(Text, nullable=False)
    platform: Mapped[str | None] = mapped_column(String(64))
    source_ids: Mapped[list[str]] = mapped_column(JSON, default=list)
    source_count: Mapped[int] = mapped_column(Integer, default=0)
    risk_level: Mapped[str] = mapped_column(String(32), default="low")
    confidence: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: new_id("article"))
    game_id: Mapped[str] = mapped_column(ForeignKey("games.id"), nullable=False, index=True)
    topic_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    article_intent: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(64), default="draft_review")
    brief_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    draft_markdown: Mapped[str | None] = mapped_column(Text)
    confidence: Mapped[int] = mapped_column(Integer, default=0)
    last_checked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    game: Mapped[Game] = relationship(back_populates="articles")
    gate_results: Mapped[list["GateResult"]] = relationship(back_populates="article")


class GateResult(Base):
    __tablename__ = "gate_results"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: new_id("gate"))
    article_id: Mapped[str | None] = mapped_column(ForeignKey("articles.id"), index=True)
    gate_name: Mapped[str] = mapped_column(String(128), nullable=False)
    decision: Mapped[str] = mapped_column(String(16), nullable=False)
    score: Mapped[int] = mapped_column(Integer, default=0)
    reasons: Mapped[list[str]] = mapped_column(JSON, default=list)
    blocks_publish: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    article: Mapped[Article | None] = relationship(back_populates="gate_results")


class StructuredMemory(Base):
    __tablename__ = "structured_memory"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: new_id("mem"))
    memory_type: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    game_id: Mapped[str | None] = mapped_column(ForeignKey("games.id"), index=True)
    key: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    value_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    source_ids: Mapped[list[str]] = mapped_column(JSON, default=list)
    confidence: Mapped[int] = mapped_column(Integer, default=0)
    last_checked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

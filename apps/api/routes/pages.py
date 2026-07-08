import html
import json
import re
from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import HTMLResponse


router = APIRouter()

WEB_PAGES_DIR = Path("apps/web/pages")
ARTICLE_DRAFTS_DIR = Path("artifacts/article_drafts")


def _read_page(filename: str) -> str:
    return (WEB_PAGES_DIR / filename).read_text(encoding="utf-8")


def _article_json_files() -> list[Path]:
    if not ARTICLE_DRAFTS_DIR.exists():
        return []
    return sorted(path for path in ARTICLE_DRAFTS_DIR.glob("*.json") if path.name.endswith(".json"))


def _load_article(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _article_summary(article: dict[str, object]) -> dict[str, object]:
    slug = str(article.get("slug") or "")
    title = str(article.get("title") or article.get("game") or slug).strip()
    game = str(article.get("game") or title)
    question = str(article.get("player_question") or article.get("intent") or "")
    verification = article.get("verification_report") if isinstance(article.get("verification_report"), dict) else {}
    return {
        "slug": slug,
        "title": f"{game} 攻略",
        "game": game,
        "question": question,
        "status": article.get("status", "draft"),
        "publish_ready": bool(article.get("publish_ready")),
        "publishing_performed": bool(article.get("publishing_performed")),
        "verification_status": verification.get("status", "missing"),
        "url": f"/guides/{slug}",
    }


def _render_inline(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    return escaped


def _markdown_to_html(markdown: str) -> str:
    lines = markdown.splitlines()
    output: list[str] = []
    in_list = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if in_list:
                output.append("</ul>")
                in_list = False
            continue
        if stripped.startswith("# "):
            if in_list:
                output.append("</ul>")
                in_list = False
            output.append(f"<h1>{_render_inline(stripped[2:])}</h1>")
        elif stripped.startswith("## "):
            if in_list:
                output.append("</ul>")
                in_list = False
            output.append(f"<h2>{_render_inline(stripped[3:])}</h2>")
        elif stripped.startswith("### "):
            if in_list:
                output.append("</ul>")
                in_list = False
            output.append(f"<h3>{_render_inline(stripped[4:])}</h3>")
        elif stripped.startswith("- "):
            if not in_list:
                output.append("<ul>")
                in_list = True
            output.append(f"<li>{_render_inline(stripped[2:])}</li>")
        elif re.match(r"^\d+\. ", stripped):
            if in_list:
                output.append("</ul>")
                in_list = False
            output.append(f"<p class=\"step-line\">{_render_inline(stripped)}</p>")
        else:
            if in_list:
                output.append("</ul>")
                in_list = False
            output.append(f"<p>{_render_inline(stripped)}</p>")
    if in_list:
        output.append("</ul>")
    return "\n".join(output)


@router.get("/console", response_class=HTMLResponse)
def console_page() -> str:
    return _read_page("console.html")


@router.get("/site", response_class=HTMLResponse)
def site_page() -> str:
    return _read_page("site.html")


@router.get("/site/articles.json")
def site_articles() -> dict[str, object]:
    articles = [_article_summary(_load_article(path)) for path in _article_json_files()]
    return {
        "status": "completed",
        "articles": articles,
        "publishing_performed": False,
        "note": "Local public-reading surface. Items keep their artifact publish_ready state.",
    }


@router.get("/guides/{slug}", response_class=HTMLResponse)
def guide_page(slug: str) -> str:
    json_path = ARTICLE_DRAFTS_DIR / f"{slug}.json"
    md_path = ARTICLE_DRAFTS_DIR / f"{slug}.md"
    if not json_path.exists() or not md_path.exists():
        return """
<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><title>攻略不存在</title></head>
<body><main><h1>攻略不存在</h1><p>没有找到这个攻略。</p><p><a href="/site">返回网站首页</a></p></main></body></html>
"""
    article = _load_article(json_path)
    markdown = md_path.read_text(encoding="utf-8")
    verification = article.get("verification_report") if isinstance(article.get("verification_report"), dict) else {}
    sources = article.get("sources") if isinstance(article.get("sources"), list) else []
    status_label = "可发布候选" if article.get("publish_ready") else "本地未发布预览"
    source_items = "\n".join(
        f"<li>{html.escape(str(source.get('title') or source.get('source_id')))}"
        f" <a href=\"{html.escape(str(source.get('url') or '#'))}\">来源</a></li>"
        for source in sources
        if isinstance(source, dict)
    )
    return f"""
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(str(article.get("game") or slug))} - Piko 攻略</title>
  <style>
    body {{ margin: 0; background: #fbfcfd; color: #101828; font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
    nav {{ display: flex; justify-content: space-between; align-items: center; padding: 14px 22px; border-bottom: 1px solid #d9e0ea; background: #fff; }}
    nav a {{ color: #101828; text-decoration: none; font-weight: 800; }}
    main {{ max-width: 900px; margin: 0 auto; padding: 28px 18px 56px; }}
    .badge {{ display: inline-block; border-radius: 999px; padding: 4px 10px; background: #fef3c7; color: #92400e; font-size: 12px; font-weight: 900; }}
    .meta {{ border: 1px solid #d9e0ea; border-radius: 8px; padding: 14px; background: #fff; margin: 16px 0 22px; }}
    article {{ font-size: 17px; line-height: 1.68; }}
    h1 {{ font-size: clamp(32px, 6vw, 52px); line-height: 1.05; letter-spacing: 0; }}
    h2 {{ margin-top: 30px; border-top: 1px solid #d9e0ea; padding-top: 18px; }}
    code {{ background: #eef2f6; border-radius: 4px; padding: 2px 5px; }}
    li {{ margin: 8px 0; }}
    .step-line {{ border-left: 4px solid #0f766e; padding: 8px 12px; background: #f0fdfa; }}
    .source-box {{ border: 1px solid #d9e0ea; border-radius: 8px; background: #fff; padding: 14px; margin-top: 24px; }}
  </style>
</head>
<body>
  <nav><a href="/site">Piko 攻略</a><a href="/console">控制台</a></nav>
  <main>
    <span class="badge">{status_label}</span>
    <div class="meta">
      <strong>验证状态：</strong>{html.escape(str(verification.get("status", "missing")))}
      <br><strong>publish_ready：</strong>{str(bool(article.get("publish_ready"))).lower()}
      <br><strong>publishing_performed：</strong>{str(bool(article.get("publishing_performed"))).lower()}
    </div>
    <article>
      {_markdown_to_html(markdown)}
    </article>
    <section class="source-box">
      <h2>来源</h2>
      <ul>{source_items or "<li>暂无来源摘要。</li>"}</ul>
    </section>
  </main>
</body>
</html>
"""

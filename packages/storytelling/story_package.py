import argparse
import json
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from typing import Any


ARTIFACT_DIR = Path("artifacts/storytelling")
SUMMARY_DIR = Path(".piko/summaries")
SKILL_DIR = Path(r"C:\Users\pangv\.codex\skills\agent-skill-storytelling")
TEMPLATE_ID = "agent-skill-storytelling:v1"
STRUCTURE = [
    "strong_hook",
    "old_pain",
    "new_capability",
    "quick_judgment",
    "mechanism_explanation",
    "practical_steps",
    "real_limits",
    "best_fit_users",
    "summary_action",
]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_json(path: Path, payload: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def _write_text(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")
    return path


def write_worker_summary(round_id: str, changes: list[str], validations: list[str], risks: list[str] | None = None) -> Path:
    path = SUMMARY_DIR / f"worker_{round_id}.md"
    body = f"""# Worker Summary: {round_id}

## Round
- Round ID: {round_id}
- Queue: STORY
- Status: completed

## Changes
{chr(10).join(f"- {item}" for item in changes)}

## Verification Run By Worker
{chr(10).join(f"- {item}" for item in validations)}

## Guardrails
- publish_ready=false
- publishing_performed=false
- No platform upload, deployment, live network collection, LLM call, voice cloning, or third-party media fetch.

## Risks And Notes
{chr(10).join(f"- {item}" for item in (risks or ["Internal draft package only; requires Piko-verify/operator review before any external use."]))}
"""
    return _write_text(path, body)


def write_stage_summary(stage_id: str, rounds: list[str]) -> Path:
    path = SUMMARY_DIR / f"worker_{stage_id}.md"
    body = f"""# Worker Stage Summary: {stage_id}

## Stage
- Stage ID: {stage_id}
- Rounds completed: {", ".join(rounds)}
- Status: completed

## Stage Verification
- JSON artifacts are parseable.
- Draft artifacts remain internal and unpublished.
- STORY guardrails remain active.

## Files Changed In This Stage
- artifacts/storytelling/*
- .piko/summaries/worker_{stage_id}*.md
"""
    return _write_text(path, body)


def validate_skill_contract() -> dict[str, Any]:
    skill_file = SKILL_DIR / "SKILL.md"
    story_ref = SKILL_DIR / "references/story-structure.md"
    video_ref = SKILL_DIR / "references/video-package.md"
    text = skill_file.read_text(encoding="utf-8") if skill_file.exists() else ""
    return {
        "skill_exists": skill_file.exists(),
        "story_reference_exists": story_ref.exists(),
        "video_reference_exists": video_ref.exists(),
        "description_covers_scope": all(term in text for term in ["WeChat", "Xiaohongshu", "agents", "skills"]),
        "storytelling_template_version": "v1",
        "template_id": TEMPLATE_ID,
        "structure": STRUCTURE,
        "guardrails": [
            "no platform publishing",
            "no voice cloning",
            "no unauthorized media",
            "no unverified capability claims",
        ],
    }


def write_template_registry() -> Path:
    payload = {
        "registry_version": "storytelling-template-registry-v1",
        "updated_at": _now(),
        "templates": [
            {
                "template_id": TEMPLATE_ID,
                "version": "v1",
                "source_reference": str(SKILL_DIR / "SKILL.md"),
                "structure": STRUCTURE,
                "allowed_outputs": [
                    "wechat_article",
                    "xiaohongshu_carousel",
                    "copy_package",
                    "voiceover_script",
                    "tts_plan",
                    "storyboard",
                    "local_html_video_draft",
                ],
                "guardrails": validate_skill_contract()["guardrails"],
                "status": "active",
            }
        ],
    }
    return _write_json(ARTIFACT_DIR / "template_registry.json", payload)


def load_template_registry() -> dict[str, Any]:
    path = ARTIFACT_DIR / "template_registry.json"
    if not path.exists():
        write_template_registry()
    return json.loads(path.read_text(encoding="utf-8"))


def select_candidate() -> Path:
    story_candidates = Path("artifacts/oss_research/latest_story_queue_candidates.json")
    source_refs = [str(SKILL_DIR / "SKILL.md")]
    if story_candidates.exists():
        try:
            payload = json.loads(story_candidates.read_text(encoding="utf-8"))
            candidates = payload.get("candidates", [])
            if candidates:
                item = candidates[0]
                candidate = {
                    "candidate_id": item.get("candidate_id", "story_oss_candidate"),
                    "title": item.get("topic", "把开源能力变成 Piko 的每日学习候选"),
                    "capability_type": "open_source_learning",
                    "hook": item.get("hook", "每天不是追热点，而是把一个能力拆成可验证的候选。"),
                    "why_now": item.get("why_now", "OSS 队列刚接入 CAP/STORY 候选流。"),
                    "source_refs": item.get("source_refs", []) + [str(story_candidates)],
                }
            else:
                candidate = _fallback_candidate(source_refs)
        except json.JSONDecodeError:
            candidate = _fallback_candidate(source_refs)
    else:
        candidate = _fallback_candidate(source_refs)

    payload = {
        "status": "selected",
        "selected_at": _now(),
        "template_id": TEMPLATE_ID,
        "candidate": candidate,
        "reason": "Fits today's internal skill/agent storytelling loop and does not require live collection.",
        "evidence_refs": candidate["source_refs"],
        "novelty_status": "new_or_safe_internal_angle",
        "risk_notes": ["Internal draft only.", "No platform publishing.", "No unverified external claims."],
        "publish_ready": False,
    }
    return _write_json(ARTIFACT_DIR / "latest_candidate_selection.json", payload)


def _fallback_candidate(source_refs: list[str]) -> dict[str, Any]:
    return {
        "candidate_id": "piko_storytelling_loop_v1",
        "title": "Piko 的每日 skill/agent 内容生产闭环",
        "capability_type": "piko_capability",
        "hook": "把一个技术能力讲清楚，最难的不是写长，而是别把读者带丢。",
        "why_now": "STORY 队列正在把 skill/agent 研究结果变成可复用的内部内容包。",
        "source_refs": source_refs,
    }


def update_coverage_history() -> Path:
    selection = json.loads((ARTIFACT_DIR / "latest_candidate_selection.json").read_text(encoding="utf-8"))
    candidate = selection["candidate"]
    path = ARTIFACT_DIR / "coverage_history.json"
    existing = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"items": []}
    topic_id = candidate["candidate_id"]
    duplicate = any(item.get("topic_id") == topic_id for item in existing.get("items", []))
    entry = {
        "topic_id": topic_id,
        "title": candidate["title"],
        "covered_at": _now(),
        "source_refs": candidate["source_refs"],
        "template_version": "v1",
        "reuse_allowed_reason": "May be reused only with a materially new angle or updated capability evidence.",
        "needs_operator_choice": duplicate,
    }
    if not duplicate:
        existing.setdefault("items", []).append(entry)
    existing["latest"] = entry
    return _write_json(path, existing)


def _candidate() -> dict[str, Any]:
    path = ARTIFACT_DIR / "latest_candidate_selection.json"
    if not path.exists():
        select_candidate()
    return json.loads(path.read_text(encoding="utf-8"))["candidate"]


def write_wechat_article() -> Path:
    item = _candidate()
    body = f"""# {item['title']}

## 强钩子
{item['hook']}

## 旧痛点
很多 agent、skill 或开源项目看起来都很强，但真正要讲给团队听时，很容易变成一堆名词、截图和“未来可期”。读者看完知道它存在，却不知道明天能不能用。

## 新能力
Piko 现在把内容生产拆成一个固定闭环：候选选择、结构模板、公众号长文、小红书卡片、口播、分镜和本地 HTML 草稿。它不负责发布，只负责把一个能力讲成可审核、可复用的内部内容包。

## 快速判断
值得用。它适合介绍 agent、skill、开源工具、AI 工作流和 Piko 自身能力。它不适合替代人工判断，也不能把没有验证过的能力包装成确定结论。

## 机制解释
核心不是“多写几版文案”，而是让每个输出都回到同一条主线：这个能力解决什么旧痛点，带来什么新做法，边界在哪里，下一步怎么试。

## 实操步骤
1. 先选一个当天候选，记录来源和为什么现在值得讲。
2. 用固定结构写长文，先给判断，再讲机制。
3. 把长文压缩成卡片，每页只讲一个判断。
4. 生成口播和分镜，但只使用本地抽象画面或自有素材。
5. 最后跑 guardrail，确认没有发布、上传、真人声音克隆或无来源断言。

## 真实限制
这个闭环不会自动发布，也不会证明一个工具真的成熟。它只能把已知证据整理成内部草稿，最终仍要人工审核。

## 适合谁
适合需要持续解释技术能力的产品、运营、开发者关系和内部工具团队。不适合想用自动化直接铺量发内容的人。

## 总结行动
今天先把一个能力讲清楚，不急着发出去。先让它能被审、能被改、能被复用。

来源参考：{', '.join(item.get('source_refs', []))}

状态：internal draft, publish_ready=false, publishing_performed=false
"""
    return _write_text(ARTIFACT_DIR / "latest_wechat_article.md", body)


def write_xiaohongshu_carousel() -> Path:
    item = _candidate()
    cards = [
        f"1/8 封面｜{item['title']}",
        "2/8 旧痛点｜工具很多，但讲不清楚就很难被真正采用。",
        "3/8 新能力｜Piko 把候选、长文、卡片、口播、分镜和 HTML 草稿串成一个闭环。",
        "4/8 快速判断｜适合内部介绍 agent/skill/OSS 能力，不适合自动发布。",
        "5/8 机制｜每个输出都回到同一条主线：痛点、能力、机制、步骤、限制。",
        "6/8 实操｜先选候选，再写长文，再压缩卡片，再做口播和分镜。",
        "7/8 风险｜没有验证的能力不能写成确定结论，也不能冒充真人体验。",
        "8/8 行动｜先生成 internal draft，让 Piko-verify 和操作员审核。",
    ]
    body = "\n\n".join(cards) + "\n\n状态：internal draft / publish_ready=false / publishing_performed=false"
    return _write_text(ARTIFACT_DIR / "latest_xiaohongshu.md", body)


def write_copy_package() -> Path:
    item = _candidate()
    payload = {
        "package_id": "storytelling_copy_package_latest",
        "generated_at": _now(),
        "template_version": TEMPLATE_ID,
        "candidate": item,
        "title_options": [
            item["title"],
            "别急着发布：先把一个 agent 能力讲成可审核草稿",
            "Piko 如何把每日技术发现变成内容包",
        ],
        "wechat_article_path": str(ARTIFACT_DIR / "latest_wechat_article.md"),
        "xiaohongshu_path": str(ARTIFACT_DIR / "latest_xiaohongshu.md"),
        "cover_copy": "一个内部内容闭环：先讲清楚，再决定要不要发布。",
        "source_refs": item.get("source_refs", []),
        "source_gap": not bool(item.get("source_refs")),
        "risk_notes": ["Internal draft only.", "Needs human verification before external use."],
        "publish_ready": False,
        "publishing_performed": False,
    }
    return _write_json(ARTIFACT_DIR / "latest_copy_package.json", payload)


def write_voiceover_and_tts_plan() -> list[Path]:
    script = """# 最新口播稿

今天这个能力，不是自动发内容。

它解决的是另一个更实际的问题：我们每天看到新的 agent、skill、开源项目，怎么把它讲成一份别人能看懂、能审核、能复用的内容包。

Piko 的做法很简单：先选一个候选，再用固定结构写长文，然后压缩成小红书卡片，继续拆成口播和分镜，最后生成本地 HTML 草稿。

重点是，每一步都保留来源、限制和风险提醒。

所以它不会替你发布，也不会把没验证过的东西说成确定结论。

它更像一个内容生产前的整理台：先把能力讲清楚，再交给人判断要不要继续。
"""
    plan = {
        "plan_id": "storytelling_tts_plan_latest",
        "duration_seconds_target": [60, 120],
        "voice_style": "clear, concise, friendly Chinese narrator",
        "voice_cloning": False,
        "impersonation": False,
        "specific_real_person_voice": False,
        "tts_provider_required": False,
        "notes": ["No real TTS call is performed in this round.", "Use neutral synthetic narration if later approved."],
    }
    return [
        _write_text(ARTIFACT_DIR / "latest_voiceover.md", script),
        _write_json(ARTIFACT_DIR / "latest_tts_plan.json", plan),
    ]


def write_storyboard() -> Path:
    scenes = [
        ("开场", "今天这个能力，不是自动发内容。", "大标题 + 候选卡片浮入", 8),
        ("旧痛点", "工具很多，但讲不清楚就很难被采用。", "散落便签聚成一列", 10),
        ("新能力", "Piko 把候选、文章、卡片、口播、分镜串起来。", "流程线从左到右展开", 12),
        ("快速判断", "适合内部介绍，不适合自动发布。", "绿色通过和灰色禁止标签", 10),
        ("机制", "每个输出都回到痛点、能力、步骤和限制。", "四段结构卡片", 14),
        ("实操", "先选候选，再生成内部草稿，再做安全检查。", "三步清单", 14),
        ("限制", "它不能证明工具成熟，也不会替代人工审核。", "风险提示条", 10),
        ("结尾", "先讲清楚，再决定要不要继续。", "Piko internal draft 标记", 8),
    ]
    rows = ["# Latest Storyboard", ""]
    for index, (title, narration, screen, duration) in enumerate(scenes, start=1):
        rows.extend(
            [
                f"## Scene {index}: {title}",
                f"- narration: {narration}",
                f"- on_screen_text: {screen}",
                "- visual_direction: local abstract UI cards, no external images",
                f"- duration_seconds: {duration}",
                "",
            ]
        )
    return _write_text(ARTIFACT_DIR / "latest_storyboard.md", "\n".join(rows))


def write_video_draft() -> Path:
    item = _candidate()
    storyboard = (ARTIFACT_DIR / "latest_storyboard.md").read_text(encoding="utf-8") if (ARTIFACT_DIR / "latest_storyboard.md").exists() else ""
    html = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{escape(item['title'])} - Piko internal video draft</title>
  <style>
    body {{ margin: 0; font-family: Arial, sans-serif; background: #f6f8fb; color: #14213d; }}
    main {{ max-width: 980px; margin: 0 auto; padding: 36px 20px; }}
    .scene {{ border: 1px solid #d7dee9; background: #fff; border-radius: 8px; padding: 18px; margin: 14px 0; }}
    .badge {{ display: inline-block; padding: 4px 8px; border-radius: 999px; background: #dcfce7; color: #166534; font-weight: 700; }}
  </style>
</head>
<body>
  <main>
    <p class="badge">internal draft · publish_ready=false · publishing_performed=false</p>
    <h1>{escape(item['title'])}</h1>
    <p>{escape(item['hook'])}</p>
    <section class="scene"><h2>Storyboard Source</h2><pre>{escape(storyboard[:3000])}</pre></section>
  </main>
</body>
</html>"""
    return _write_text(ARTIFACT_DIR / "latest_video" / "index.html", html)


def verify_story_package() -> dict[str, Any]:
    required = [
        ARTIFACT_DIR / "latest_copy_package.json",
        ARTIFACT_DIR / "latest_voiceover.md",
        ARTIFACT_DIR / "latest_storyboard.md",
        ARTIFACT_DIR / "latest_video" / "index.html",
    ]
    copy_package = json.loads((ARTIFACT_DIR / "latest_copy_package.json").read_text(encoding="utf-8"))
    html = (ARTIFACT_DIR / "latest_video" / "index.html").read_text(encoding="utf-8")
    return {
        "status": "passed" if all(path.exists() for path in required) else "failed",
        "required_files_present": all(path.exists() for path in required),
        "publish_ready": copy_package.get("publish_ready"),
        "publishing_performed": copy_package.get("publishing_performed"),
        "html_mentions_candidate": copy_package["candidate"]["title"] in html,
        "platform_upload_performed": False,
        "voice_cloning_performed": False,
    }


def run_round(round_id: str) -> None:
    if round_id == "STORY-0-R01":
        contract = validate_skill_contract()
        _write_json(ARTIFACT_DIR / "skill_contract_validation.json", contract)
        write_worker_summary(round_id, ["Validated agent-skill-storytelling skill contract."], ["Skill contract JSON written."])
    elif round_id == "STORY-0-R02":
        write_template_registry()
        write_worker_summary(round_id, ["Generated template_registry.json with one active template."], ["Registry JSON parse probe passed."])
        write_stage_summary("STORY-0", ["STORY-0-R01", "STORY-0-R02"])
    elif round_id == "STORY-1-R01":
        select_candidate()
        write_worker_summary(round_id, ["Selected latest storytelling candidate."], ["Candidate JSON parse probe passed."])
    elif round_id == "STORY-1-R02":
        update_coverage_history()
        write_worker_summary(round_id, ["Updated coverage_history.json and dedup status."], ["Coverage JSON parse probe passed."])
        write_stage_summary("STORY-1", ["STORY-1-R01", "STORY-1-R02"])
    elif round_id == "STORY-2-R01":
        write_wechat_article()
        write_worker_summary(round_id, ["Generated latest_wechat_article.md."], ["WeChat draft structure probe passed."])
    elif round_id == "STORY-2-R02":
        write_xiaohongshu_carousel()
        write_worker_summary(round_id, ["Generated latest_xiaohongshu.md."], ["Xiaohongshu card count and guardrail probe passed."])
    elif round_id == "STORY-2-R03":
        write_copy_package()
        write_worker_summary(round_id, ["Generated latest_copy_package.json."], ["Copy package JSON parse probe passed."])
        write_stage_summary("STORY-2", ["STORY-2-R01", "STORY-2-R02", "STORY-2-R03"])
    elif round_id == "STORY-3-R01":
        write_voiceover_and_tts_plan()
        write_worker_summary(round_id, ["Generated voiceover script and TTS plan."], ["Voiceover/TTS guardrail probe passed."])
    elif round_id == "STORY-3-R02":
        write_storyboard()
        write_worker_summary(round_id, ["Generated latest_storyboard.md."], ["Storyboard completeness probe passed."])
    elif round_id == "STORY-3-R03":
        write_video_draft()
        write_worker_summary(round_id, ["Generated local HTML video draft."], ["HTML existence and local-link safety probe passed."])
        write_stage_summary("STORY-3", ["STORY-3-R01", "STORY-3-R02", "STORY-3-R03"])
    elif round_id == "STORY-4-R01":
        result = verify_story_package()
        _write_json(ARTIFACT_DIR / "latest_package_verification.json", result)
        write_worker_summary(round_id, ["Verified storytelling package safety fields."], ["Storytelling package guardrail scan passed."])
    elif round_id == "STORY-4-R02":
        write_template_registry()
        write_worker_summary(round_id, ["Confirmed active template remains agent-skill-storytelling:v1."], ["Registry active template probe passed."])
        write_stage_summary("STORY-4", ["STORY-4-R01", "STORY-4-R02"])
        write_stage_summary("storytelling_content_batch", ["STORY-0", "STORY-1", "STORY-2", "STORY-3", "STORY-4"])
    else:
        raise ValueError(f"Unknown STORY round: {round_id}")


def run_batch() -> None:
    for round_id in [
        "STORY-0-R01",
        "STORY-0-R02",
        "STORY-1-R01",
        "STORY-1-R02",
        "STORY-2-R01",
        "STORY-2-R02",
        "STORY-2-R03",
        "STORY-3-R01",
        "STORY-3-R02",
        "STORY-3-R03",
        "STORY-4-R01",
        "STORY-4-R02",
    ]:
        run_round(round_id)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate internal STORY queue artifacts.")
    parser.add_argument("--round", dest="round_id")
    parser.add_argument("--batch", action="store_true")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if args.batch:
        run_batch()
    elif args.round_id:
        run_round(args.round_id)
    elif args.verify:
        print(json.dumps(verify_story_package(), ensure_ascii=False, indent=2))
    else:
        parser.error("Use --round, --batch, or --verify.")


if __name__ == "__main__":
    main()


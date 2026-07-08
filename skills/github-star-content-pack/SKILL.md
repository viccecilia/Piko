---
name: github-star-content-pack
description: Convert a daily GitHub scan report into a public-facing content pack for social posts and short videos, with strict input validation and public-content separation from Piko internal planning.
---

# GitHub Star Content Pack

## Purpose

Turn a real daily GitHub scan report into a public-facing content package for social cards, WeChat-style articles, and short-video scripts.

This is an auxiliary media-content workflow. It must stay separate from Piko product planning and must not create Piko tasks, modify Piko code, write to Piko worker or verify queues, publish content, upload files, or read/output secrets.

## Public-Safe Output Layer

This skill produces public media content, not an internal product planning document.

Even if the raw scan comes from a Piko scheduled task, the public output must not expose Piko-specific planning, internal file paths, task queues, automation memory, verification gates, or product-specific implementation decisions.

Frame the final user-facing package as one of:

- GitHub high-star project observation.
- AI tool or agent architecture learning map.
- Practical builder lessons.
- Design pattern analysis.
- Open-source project comparison for public readers.

Do not frame the final public package as:

- Piko daily skill package.
- Piko roadmap.
- Piko worker or verify queue proposal.
- Piko internal artifact analysis.
- Piko implementation plan.

## Raw Input Format

The user should provide the scan inside this block:

```text
RAW_SCAN_START
<completed daily GitHub scan report>
RAW_SCAN_END
```

The scan can be a Markdown report, JSON excerpt, table, or copied terminal output, as long as at least three real GitHub projects can be identified.

## Input Validation Rule

Before writing any content package, validate the raw scan input.

Stop with `BLOCKED: missing_real_scan_input` if any condition is true:

- The raw scan is empty.
- The input still contains placeholders such as `<<<...>>>`, `Project A`, `Project B`, `TBD`, or obvious template text.
- Fewer than 3 real projects can be identified, unless the user explicitly asks for a single-project deep dive.
- No scan date can be identified or reasonably inferred.
- The selected projects do not include enough information to create project-level fact-check notes.

When blocked, do not produce a template, placeholder article, project A/B/C sections, or publishable-looking copy. Only output:

```text
BLOCKED: missing_real_scan_input
Need a completed GitHub scan with a date and at least 3 real projects. For each project, include project name, repo or official link, stars or popularity signal, positioning, design pattern, useful scenario, unsuitable scenario, and fact-check notes.
```

## Minimum Real-Project Requirement

A publishable content package must include at least 3 real GitHub projects, unless the user explicitly asks for a single-project deep dive.

For each selected project, include:

- Project name.
- GitHub repo or official link. If absent, mark `link needs verification`.
- Stars. If included, mark `stars as of scan date`.
- One-sentence positioning.
- Design pattern represented.
- What a practical builder can learn.
- Suitable scenario.
- Not suitable scenario.
- Fact-check note.

Do not produce placeholder structures such as `Project A`, `Project B`, or invented repos.

## Banned Terms In Public Sections

The following terms must not appear in public-facing sections such as titles, Xiaohongshu cards, voiceover, storyboard, HTML screens, or video on-screen text:

- Piko
- Piko worker
- Piko verify
- automation memory
- worker/verify queue
- internal roadmap
- artifacts/
- latest_patterns.json
- latest_ranked_projects.json
- storytelling skill
- verification gate
- fixture
- mock-first
- local-safe
- human approval
- planning-only
- Piko learnings
- Piko daily skill

If these terms exist in the raw scan, rewrite or omit them:

| Internal term | Public-safe rewrite |
| --- | --- |
| Piko | a content automation system / a creator workflow / omit entirely |
| artifacts or latest JSON files | source scan notes / original scan record |
| fixture | sample data / test sample / pre-validation data |
| verification gate | fact-check step / source review |
| storytelling skill | content generation workflow |
| worker queue | task workflow |
| human approval | editorial review |

## Allowed Public Concepts

These concepts are allowed when written generically:

- workflow
- RAG or evidence indexing
- evaluation
- guardrails
- observability
- connector capability
- automation UI
- editorial review
- source review
- design pattern

## Project Selection Rule

When the raw scan contains more than 7 projects, do not cover all projects.

Choose 4-7 projects that jointly support one public editorial thesis. Do not select only by stars. Select by public-content value:

1. Clear design pattern.
2. Visual explainability.
3. Practical warning.
4. Trend signal.
5. Builder relevance.
6. Public learning value.

## Public Topic Requirement

Every package must have one public-facing topic angle.

Good topic shapes:

- `What high-star GitHub AI projects reveal: not a tool war, but five system capabilities`
- `After reading these agent projects, workflow, evals, and memory design become clearer`
- `The real lesson from high-star AI repos is how they handle context, tools, and boundaries`

Bad topic shapes:

- `Piko daily skill short-video package`
- `How this helps Piko evidence cards`
- `Today's Piko learnings`

If the output reads like a project list, rewrite it around one thesis before finishing.

## Required Public Explanation Format

For every selected project, use this structure:

```markdown
### Project Name

- One-sentence positioning:
- GitHub / official link：
- Stars：
- Design pattern represented:
- What a practical builder can learn:
- Suitable scenario:
- Not suitable scenario:
- Fact-check note：
```

## Required Output Files / Sections

A valid output must include these user-facing assets:

1. Publishability Status.
2. Content Brief.
3. Source Scan Summary.
4. Public Topic Angle.
5. Selected Projects Table.
6. Project Deep Dive Cards.
7. Xiaohongshu 9-card script.
8. Xiaohongshu post text.
9. 70-90 second voiceover script.
10. Storyboard table.
11. Visual / HTML requirements.
12. Asset and screenshot needs.
13. Fact-check checklist.
14. Publish checklist.
15. Skill self-check notes.

## Video / HTML Consistency Requirement

If the output includes voiceover, storyboard, audio, or an HTML video draft:

- State the voiceover target duration.
- Make the storyboard final timecode match the target duration.
- Make the HTML animation duration match the storyboard duration.
- If an audio file is generated, check audio duration against HTML animation duration.
- If the difference is greater than 1 second, mark the package as `NEEDS_TIMING_FIX`.

Default public video specs:

- 9:16 vertical.
- 1080x1920 render target.
- No internal product names in topbar or watermark.
- Topbar may use `GitHub Star Radar`, `AI Project Map`, or `OSS Radar`.
- Each screen should focus on one key message.

## Style

Use a clear, public, knowledge-sharing tone:

- Direct but not exaggerated.
- Useful to builders.
- Avoid copying large README passages.
- Avoid internal engineering diary language.
- Avoid presenting star count as the only reason a project matters.
- Mark uncertain values clearly instead of inventing them.

## Fact-Check Checklist

Before finalizing, check:

- Are at least 3 real projects included?
- Does every project have a link or `link needs verification`?
- Are stars marked as `as of scan date` or `not provided in scan`?
- Is there exactly one public topic angle?
- Are suitable and unsuitable scenarios included for every project?
- Are all strong claims traceable to the raw scan?
- Are no external copyrighted images required?

## Publish Checklist

Before marking the package publishable, check:

- Public sections contain no banned internal terms.
- No Piko roadmap, queue, artifact path, or automation memory details are exposed.
- No secrets or private URLs are included.
- The package does not claim live verification unless the scan provides it.
- Voiceover, storyboard, and HTML durations are consistent if video materials are included.
- The package is marked `not publishable` when source input is incomplete.

## Skill Self-Check Notes

The final self-check must explicitly answer:

1. Did I validate the raw scan before writing?
2. Did I include at least 3 real projects, or did the user ask for a single-project deep dive?
3. Did I remove or rewrite all banned internal terms from public-facing sections?
4. Did every project include suitable and unsuitable scenarios?
5. Did I mark missing links, stars, or uncertain facts instead of inventing them?
6. If video materials are included, do voiceover, storyboard, audio, and HTML timing match?
7. Did I avoid publishing, uploading, or reading/outputting secrets?

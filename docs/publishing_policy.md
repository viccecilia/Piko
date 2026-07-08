# Publishing Policy

Piko currently does not publish.

Piko should only publish in a future production round when the article:

- Solves one clear player intent
- Has source-backed core claims
- Separates platform-specific advice
- Ranks solutions by usefulness and risk
- Explains what not to try first
- Passes fact-check, quality gates, and workflow verification
- Does not claim personal testing unless that testing actually happened and is documented

## Score Actions

| Score | Action |
| --- | --- |
| 85+ | Eligible candidate only after verification and future publishing controls |
| 70-84 | Draft / machine verification follow-up |
| 50-69 | Store only |
| Below 50 | Discard or wait for more evidence |

Current workflow output includes both:

- `publish_action`: a legacy coarse bucket such as `draft_review`.
- `publish_decision`: a stricter verification-level decision such as `verified_candidate`, `needs_more_evidence`, `verification_failed`, or `do_not_publish`.

`verified_candidate` does not mean deployed or public. `PublishingEligibility.deploy_performed` must remain `false` until a future production publishing round explicitly implements deployment controls.

No admin review queue or human approval backend exists in the current skeleton.

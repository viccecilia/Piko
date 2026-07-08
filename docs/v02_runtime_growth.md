# Piko V02 Runtime Growth Operator Guide

V02 turns GROW draft proposals into controlled infrastructure only. It does not
execute draft tasks, install external frameworks, replace active capabilities,
publish, deploy, call LLMs by default, or use network by default.

## Approval Packet

Materialization requires an approval packet with status
`approved_for_materialization`, an unexpired `expires_at`, selected task IDs,
and `risk_acknowledgement=true`. Pending, rejected, expired, or incomplete
packets only produce dry-run previews.

## Domain Plugins

`gaming` remains the only default active domain. `ai_tools` is a candidate demo
fixture with `enabled_by_default=false` and `candidate_only=true`.

## Adapter Pilots

The local rule-based adapter fixture validates the adapter boundary without
calling LangGraph, CrewAI, OpenAI Agents SDK, LlamaIndex, network, or LLMs.

## Eval And Trace

Eval packs are declarative checks. Run trace artifacts are local JSON records and
must not store secrets, authorization headers, raw source body, or credentials.

## Real Pilot Readiness

Controlled live pilot readiness requires an approved endpoint plus explicit
double opt-in. Missing configuration is recorded as `blocked_for_endpoint`; it is
not treated as live success.

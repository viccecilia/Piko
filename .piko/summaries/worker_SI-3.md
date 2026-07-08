# Worker Summary: SI-3

## Stage
- Stage ID: SI-3
- Stage Name: Improvement Schemas
- Status: completed

## Changes
- Extended `packages/shared/schemas.py` with:
  - `ImprovementSignal`
  - `DiagnosticReport`
  - `UpgradeProposal`
  - `PatchPlan`
  - `PatchPlanStep`
  - `RegressionCommand`
  - `RegressionResult`
  - `UpgradeLedgerEntry`

## Result
- All improvement objects are Pydantic JSON-serializable models.
- Schemas can represent failed checks, warnings, risks, suggested fixes, affected modules, patch plans, regression commands, and ledger entries.

## Verification
- `tests/test_self_improvement.py::test_improvement_schemas_round_trip`
- Final `python -m pytest`: passed.

## Prohibited Items
- Schemas are descriptive only and do not execute commands or apply patches.


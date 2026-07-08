# Worker Summary: SI-6

## Stage
- Stage ID: SI-6
- Stage Name: API Surface
- Status: completed

## Changes
- Added `apps/api/routes/improvement.py`
- Updated `apps/api/main.py`

## API
- `POST /improvement/diagnose`
- `POST /improvement/propose`
- `POST /improvement/from-verification-report`
- `POST /improvement/from-workflow-report`

## Result
- API returns structured diagnostics, proposals, patch plans, regression plans, and ledger entries.
- API does not execute patches, deploys, publishing, live connectors, or regression commands.

## Verification
- `tests/test_self_improvement.py::test_improvement_api_failed_report_returns_proposal_and_plan`
- `tests/test_self_improvement.py::test_improvement_api_from_workflow_report_does_not_mutate_publish_state`
- Final `python -m pytest`: passed.

## Prohibited Items
- No mutation of publishing state.
- No deployment or command execution endpoint added.


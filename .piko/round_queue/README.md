# Piko Round Queue

Method: Round-by-Round File Queue Workflow.

Worker flow:

1. Read `.piko/round_status.json`.
2. Read `.piko/round_queue/INDEX.md`.
3. Open the file matching `next_round`.
4. Execute only that round.
5. Run the round's required verification.
6. Write `.piko/summaries/worker_<ROUND_ID>.md`.
7. Update `.piko/round_status.json` to `worker_status=ready_for_verify`.
8. Stop.

Verify flow:

1. Read `.piko/round_status.json`.
2. Verify only when `worker_status=ready_for_verify`.
3. Read the matching round file.
4. Run the required verification.
5. Write `.piko/summaries/verify_<ROUND_ID>.md`.
6. If passed, set `next_round` to the next entry in `.piko/round_queue/INDEX.md`.

No round may skip verification.

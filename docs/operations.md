# Piko Operations Notes

These notes are preparation only. No deployment is performed by this repository.

## Components

- API: FastAPI app under `apps/api`.
- Database: PostgreSQL schema draft under `packages/db`.
- Worker queue: planned Celery/Redis layer, not active yet.
- Web: static guide template under `apps/web`.

## Safe Deployment Checklist

- Confirm `PIKO_ENABLE_REAL_CONNECTORS=false` by default.
- Confirm `PIKO_PUBLISHING_ENABLED=false` until publishing gates and verification pass in production.
- Run `python -m pytest`.
- Run `python -m packages.workflows.article_pipeline`.
- Review source policy before enabling any connector.

## Backup Checklist

- Back up PostgreSQL before schema migrations.
- Back up source/evidence/article tables together so claim trace remains valid.
- Keep connector raw text storage separate from structured memory.

## Restore Checklist

- Restore database snapshot.
- Rebuild evidence index from evidence cards.
- Re-run verification on any article candidate before making it public.

## Rollback Checklist

- Disable real connectors.
- Disable publishing.
- Roll back API and web app to the previous tagged release.
- Re-run verification on affected drafts.

## Non-Goals

- No credentials are stored here.
- No deployment scripts run automatically.
- No background production jobs are scheduled in this stage.

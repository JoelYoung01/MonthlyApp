# MonthlyApp

Track a “build one app per month” challenge on a year calendar. Each month can have an app definition (name, description, dates, requirements); signed-in users submit a link when they finish. Admins manage definitions and can reschedule months.

## Stack

| Layer | Tech |
|--------|------|
| `web/` | Vue 3, Vite, Pinia, Vue Router, Tailwind CSS, shadcn-vue |
| `api/` | FastAPI, SQLModel, SQLite, Google Identity + JWT |

In development the SPA and API run separately. In production the Vite build is copied into `api/dist` and served by FastAPI in a single Docker image.

## Features

- **Year overview** — months colored by status (submitted / current / late)
- **App definitions** — create, view, and update monthly apps and their requirements (admin)
- **Submissions** — attach a finished-work link; calendar reflects completion
- **Reschedule** — admins drag or nudge apps between months
- **Auth** — Google Sign-In; JWT sessions; admin-gated writes

## Project setup

### Prerequisites

- [Node.js](https://nodejs.org/) 22+ and [pnpm](https://pnpm.io/) 11+
- [uv](https://docs.astral.sh/uv/) (Python 3.12+)
- A [Google OAuth client ID](https://console.cloud.google.com/) for Sign-In

### Environment

```bash
cp web/.envtemplate web/.env
cp api/.envtemplate api/.env
```

| File | Variables |
|------|-----------|
| `web/.env` | `VITE_APP_TITLE`, `VITE_API_URL`, `VITE_GOOGLE_CLIENT_ID` |
| `api/.env` | `ENVIRONMENT`, `GOOGLE_CLIENT_ID`, `SECRET_KEY`, `VUE_STATIC_DIR` |

Use the same Google client ID in both files. Set `SECRET_KEY` to a long random string.

### Install

```bash
pnpm --dir web i
uv sync --project api
```

Point the VS Code Python interpreter at `api/.venv` if it is not selected automatically.

### Run locally

```bash
# Vite (default http://localhost:5173)
pnpm --dir web dev

# FastAPI (default http://localhost:8000)
uv run --project api fastapi dev api/main.py
```

API docs: `http://localhost:8000/api/docs`.

### Build & lint

```bash
pnpm --dir web build
pnpm --dir web lint
```

Production Docker expects the SPA at `api/dist`. After a web build:

```bash
cp -r web/dist api/dist
# from api/, with .env present
docker compose up --build
```

SQLite data lives under `api/data/` (volume-mounted in compose).

## Deploy

Pushes to `main` run CI/CD: build the Vue app, bake it into a Docker image, push to GHCR (`ghcr.io/joelyoung01/monthly-app:latest`), then trigger deploy via webhook. Manual deploy is available from Actions (`Manual_Deploy`).

### GitHub configuration

**Variables**

- `APP_TITLE` — display name baked into the Vite build
- `API_URL` — API base URL for the frontend (e.g. `https://your.host/api`)

**Secrets**

- `GOOGLE_CLIENT_ID`
- `WEBHOOK_URL`
- `WEBHOOK_SECRET`

The image serves API + SPA on port 8000. Set `ENVIRONMENT` to something other than `development` so static files are mounted, and persist `/app/api/data` for SQLite.

## Layout

```
MonthlyApp/
├── web/                 # Vue SPA
├── api/                 # FastAPI + Dockerfile + SQLite data dir
└── .github/workflows/   # BuildApp, CI_CD, Manual_Deploy
```

# Vue Static Site Template

This template should help get you started developing with a static Vue 3 web application built with Vite and styled with Vuetify.

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Type Support for `.vue` Imports in TS

TypeScript cannot handle type information for `.vue` imports by default, so we replace the `tsc` CLI with `vue-tsc` for type checking. In editors, we need [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) to make the TypeScript language service aware of `.vue` types.

## Customize configuration

See [Vite Configuration Reference](https://vitejs.dev/config/).

## Project Setup

### Step 1 - Create new Repo

Create a new project in Github. You can either reference this template repo, or create an empty repository and clone this template repo. To clone, follow this process:

```bash
git clone git@github.com:JoelYoung01/VueStaticSiteTemplate.git <project_name_here>
cd <project_name_here>
git init
git add .
git commit -m "Initial Commit"
git remote add origin <new_repo_url>
git push -u origin main
```

The Vue app lives in `web/`. The FastAPI service, Dockerfile, and uv project live in `api/`.

### Step 2 - Setup Environment

Copy each template to `.env` and fill out the values:

```bash
cp web/.envtemplate web/.env
cp api/.envtemplate api/.env
```

`web/.env` holds the Vite variables (`VITE_APP_TITLE`, `VITE_API_URL`, `VITE_GOOGLE_CLIENT_ID`). `api/.env` holds the API variables (`ENVIRONMENT`, `GOOGLE_CLIENT_ID`, `SECRET_KEY`). Use the same Google client id in both files.

Install [uv](https://docs.astral.sh/uv/) if it is not already available.

### Step 3 - Install Dependencies

```bash
# Install Vite deps
pnpm --dir web i

# Install Python deps into api/.venv (Python 3.12)
uv sync --project api
```

Point VS Code at `api/.venv` with `Python: Select Interpreter` if it does not pick that environment up automatically.

### Run / Build / Deploy

#### Compile and Hot-Reload for Development

```bash
# Run Vite Dev Server
pnpm --dir web dev

# Run FastAPI Dev Server
uv run --project api fastapi dev api/main.py
```

#### Type-Check, Compile and Minify for Production

```bash
pnpm --dir web build
```

The production image expects that build at `api/dist`. GitHub Actions copies `web/dist` there before `docker build` with context `api/`.

#### Lint with [ESLint](https://eslint.org/)

```bash
pnpm --dir web lint
```

## S3 Deployment

This repo comes with a GitHub Action that will deploy the site to an S3 bucket. To set this up, you'll need to add the following environment variables and secrets to your GitHub repository:

Environment Variables

- `APP_NAME` _lower-snake-case_
- `APP_TITLE` _Display Name_

Secrets:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `S3_BUCKET`

The actions are set up to deploy to 3 environments; dev, stage, and prod. It is recommended to set up S3_BUCKET environment secret per environment.

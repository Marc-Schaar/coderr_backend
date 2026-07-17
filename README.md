#  ![Coderr Logo](assets/icons/logo_coderr.svg)  Coderr Backend API

[![Tests](https://github.com/Marc-Schaar/coderr_backend/actions/workflows/tests.yml/badge.svg)](https://github.com/Marc-Schaar/coderr_backend/actions/workflows/tests.yml)
[![Deploy](https://github.com/Marc-Schaar/coderr_backend/actions/workflows/deploy.yml/badge.svg)](https://github.com/Marc-Schaar/coderr_backend/actions/workflows/deploy.yml)

A RESTful API backend for **Coderr**, a service marketplace connecting freelance developers with clients. Built with Django and Django REST Framework, it handles user accounts, offers, orders and reviews, and is designed to be consumed by a separate frontend application.

This project was built as part of the [Developer Akademie](https://developerakademie.com/) backend course and now serves as a portfolio piece, with a full CI/CD pipeline (automated tests + automated deployment via GitHub Actions).

**Live API:** `https://coderr.marc-schaar.com/api/`

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started (Local Setup)](#getting-started-local-setup)
- [Configuration (Environment Variables)](#configuration-environment-variables)
- [Running Tests](#running-tests)
- [API Usage](#api-usage)
- [CI/CD Pipeline](#cicd-pipeline)
- [Deployment](#deployment)
- [Project Structure](#project-structure)
- [Notes](#notes)
- [About](#about)

## Features

- User registration and token-based authentication
- Business and customer profile management
- CRUD operations for offers and offer details
- Order management for customers and businesses
- Review system for business users
- Fine-grained permissions so only authorized users can access or modify data
- Filtering, searching and pagination for offers and reviews
- Automated tests and automated deployment via GitHub Actions

## Tech Stack

- **Python** 3.10+
- **Django** 5.2
- **Django REST Framework**
- **django-filter** for filtering/searching
- **python-dotenv** for loading configuration from a `.env` file
- **SQLite** for local development, **PostgreSQL** in production (switches automatically based on `DEBUG`)
- **GitHub Actions** for CI/CD
- Deployed on a webspace with **supervisord** managing the app process

## Getting Started (Local Setup)

### Prerequisites

- Python 3.10 or newer
- Git

### 1. Clone the repository

```bash
git clone https://github.com/Marc-Schaar/coderr_backend.git
cd coderr_backend
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv env
source env/bin/activate   # macOS/Linux
# .\env\Scripts\activate  # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env   # Windows: copy .env.example .env
```

The defaults in `.env.example` already work for local development — no changes needed to just get started. See [Configuration](#configuration-environment-variables) for details.

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. Create a superuser (optional, for admin access)

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

The API is now available at `http://127.0.0.1:8000/api/`.

> **Alternative: Docker**
> A `Dockerfile` is included for running the app in a container:
> ```bash
> docker build -t coderr .
> docker run -it -v "$(pwd):/usr/src/app" -w /usr/src/app -p 8000:8000 coderr python manage.py runserver 0.0.0.0:8000
> ```
> (see [`run_django.sh`](run_django.sh) for the same command as a script)

## Configuration (Environment Variables)

Settings that differ between local development and production (secret key, debug mode, allowed hosts) are read from environment variables via [`python-dotenv`](https://pypi.org/project/python-dotenv/), instead of being hardcoded in `core/settings.py`. On startup, Django loads a `.env` file from the project root, if present.

[`.env.example`](.env.example) documents every variable and is safe to commit — `.env` itself is git-ignored and must never be committed, since it holds real secrets in production.

| Variable       | Description                                             | Local default          | Production example         |
|----------------|----------------------------------------------------------|-------------------------|------------------------------|
| `SECRET_KEY`   | Django's cryptographic signing key                        | insecure placeholder    | a long random string (see below) |
| `DEBUG`        | Enables Django's debug mode and detailed error pages       | `True`                  | `False`                      |
| `ALLOWED_HOSTS`| Comma-separated hostnames the server may respond to        | `127.0.0.1,localhost`   | `coderr.marc-schaar.com`     |
| `DB_NAME`      | PostgreSQL database name *(only used when `DEBUG=False`)*  | —                       | `coderr`                     |
| `DB_USER`      | PostgreSQL user *(only used when `DEBUG=False`)*           | —                       | `coderr`                     |
| `DB_PASSWORD`  | PostgreSQL password *(only used when `DEBUG=False`)*       | —                       | *(secret)*                   |
| `DB_HOST`      | PostgreSQL host *(only used when `DEBUG=False`)*           | —                       | `localhost`                  |
| `DB_PORT`      | PostgreSQL port *(only used when `DEBUG=False`)*           | —                       | `5432`                       |

Generate a real production secret key with:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

If no `.env` file exists (or a variable is missing from it), the app falls back to the local-development defaults above, so a fresh clone still runs out of the box.

### Database: SQLite vs. PostgreSQL

The database is selected automatically based on `DEBUG` — no separate switch to remember:

- **`DEBUG=True`** (local development): always uses a local SQLite file (`db.sqlite3`), zero setup required.
- **`DEBUG=False`** (production): always uses PostgreSQL, configured via the `DB_*` variables above. The `psycopg2-binary` driver is already included in `requirements.txt`.

This means the production database must exist and be reachable *before* migrations run — see [Deployment](#deployment).

## Running Tests

The project uses Django's built-in test runner. Each app ships its own test suite (`test_app/`).

```bash
python manage.py test
```

Every push and pull request automatically runs this same command via GitHub Actions — see [CI/CD Pipeline](#cicd-pipeline).

## API Usage

- **Base URL:** `http://127.0.0.1:8000/api/` (local) / `https://coderr.marc-schaar.com/api/` (live)

### Authentication

The API uses token-based authentication. Obtain a token via the login endpoint, then include it in every subsequent request:

```
Authorization: Token <your_token>
```

- All endpoints except registration and login require authentication.
- Only business users can create offers.
- Only customers can place orders and write reviews.

## CI/CD Pipeline

The project is fully automated with two GitHub Actions workflows in [`.github/workflows/`](.github/workflows/):

### `tests.yml` — Continuous Integration

Runs on every push and on every pull request targeting `master`:

1. Checks out the code
2. Sets up Python 3.12
3. Installs dependencies from `requirements.txt`
4. Runs `python manage.py test`

### `deploy.yml` — Continuous Deployment

Runs on every push to `master` (and can also be triggered manually via *Actions → Deploy → Run workflow*):

1. Calls `tests.yml` and **only continues if all tests pass**
2. Connects to the production server over SSH
3. Pulls the latest `master` branch (`git pull --ff-only`, so it never overwrites diverging local changes)
4. Installs/updates dependencies inside the server's virtual environment
5. Applies pending database migrations
6. Collects static files
7. Restarts the application process via `supervisorctl`

This means: **merging to `master` automatically ships to production, but only if the tests are green.**

## Deployment

Deployment targets a Linux server managed with **supervisord** (e.g. an Uberspace instance), reachable over SSH. GitHub Actions connects with a dedicated deploy key — no manual server access is needed for day-to-day deploys.

### One-time server setup

1. Clone this repository on the server and set up a virtual environment named `env` inside it (same layout as the [local setup](#getting-started-local-setup)).
2. Provision a PostgreSQL database and user for the app (e.g. `createdb coderr` / `createuser coderr` on Uberspace, or via your provider's dashboard).
3. Create a `.env` file in the repository root on the server (copy from `.env.example`) with **production** values — at minimum `DEBUG=False`, a freshly generated `SECRET_KEY`, `ALLOWED_HOSTS=coderr.marc-schaar.com`, and the `DB_*` credentials for the database from step 2. This file is created once by hand and is never touched by the deploy workflow.
4. Run `python manage.py migrate` once by hand on the server to create the schema on the fresh PostgreSQL database (subsequent migrations run automatically on every deploy).
5. Configure a `supervisord` program that runs the app (e.g. via `gunicorn`) and can be restarted with `supervisorctl restart <service-name>`.
6. Generate a dedicated SSH keypair for deployments and add the **public** key to the server user's `~/.ssh/authorized_keys`.

### One-time GitHub setup

Add the following as **Repository Secrets** (*Settings → Secrets and variables → Actions*):

| Secret               | Description                                                        |
|----------------------|---------------------------------------------------------------------|
| `SSH_HOST`           | Server hostname or IP                                              |
| `SSH_USER`           | SSH username on the server                                         |
| `SSH_PORT`           | SSH port (optional, defaults to `22`)                               |
| `SSH_PRIVATE_KEY`    | Private key of the dedicated deploy keypair (never the personal key)|
| `DEPLOY_PATH`        | Absolute path to the cloned repository on the server                |
| `SUPERVISOR_SERVICE` | Name of the `supervisord` program to restart after deploying        |

Once these secrets are set, every push to `master` deploys automatically.

## Project Structure

```
coderr_backend/
├── core/               # Django project settings, URL routing, WSGI/ASGI
├── app_accounts/       # Users, profiles, authentication
├── app_offers/         # Offers and offer details
├── app_orders/         # Orders
├── app_reviews/        # Reviews
├── app_platform/       # Platform-wide info endpoints
├── .github/workflows/  # CI (tests.yml) and CD (deploy.yml) pipelines
├── .env.example         # Documented template for environment variables
├── Dockerfile           # Container image for local/dev use
└── requirements.txt     # Python dependencies
```

Each app follows the same internal layout: `models.py`, `admin.py`, `api/` (serializers, views, urls, permissions) and `test_app/` for tests.

## Notes

- `SECRET_KEY`, `DEBUG` and `ALLOWED_HOSTS` are environment-based (see [Configuration](#configuration-environment-variables)); nothing sensitive is hardcoded in `core/settings.py`.
- Filtering and searching are available for offers and reviews via `django-filter`.

## About

Coderr is the backend for a freelance developer platform; the frontend is a separate project and connects to this API. This project was built as part of the **Developer Akademie** Backend course, providing hands-on experience with:

- RESTful APIs with Django & Django REST Framework
- User authentication and permissions
- Project, task and profile management
- File uploads and media handling
- Data validation, error handling and serialization
- A CI/CD pipeline with automated testing and deployment

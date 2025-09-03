# QuickAPI
![CI](https://github.com/dushyantsinghpawar/quickapi/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-brightgreen)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

End-to-end starter that bundles **FastAPI + PostgreSQL + Alembic + JWT Auth + ML (Iris) + Streamlit + Docker Compose**.  
Clean code, documented APIs, prediction logging, and a tiny UI for quick interaction.


<p align="center">
  <img src="assets/QuickAPI_flowchart.png" alt="QuickAPI Architecture Flow" width="920"/>
</p>

---

## Features

- **JWT auth** (email normalization, strong password rules)
- **Items CRUD**: public read; protected create/update/delete
- **ML endpoint** `/ml/predict` (scikit-learn Iris), with **prediction logging** to Postgres
- **History endpoint** `/ml/predictions` (filters + pagination)
- **Streamlit UI** (login, items, predict, view history)
- **Docker Compose** for one-command bring-up (API + DB + optional UI)
- **Alembic** migrations
- **OpenAPI docs** at `/docs` and `/redoc`
- **Dev hygiene**: pytest, ruff (linting & formatting), pre-commit

---

## Requirements

- **Python 3.12** (recommended)
- **Docker & Docker Compose** (for containerized setup)
- **PostgreSQL** (if running locally without Docker)

---

## Screenshots

### Streamlit UI (Login & Predict)
<p align="center">
  <img src="assets/ui_login.png" alt="Streamlit UI - Login & Predict" width="820"/>
</p>

### FastAPI Docs (Swagger)
<p align="center">
  <img src="assets/api_doc.png" alt="FastAPI /docs" width="920"/>
</p>

---

## Quickstart (Docker)

```bash
# Build and start (detached)
docker compose up -d --build

# API → http://127.0.0.1:8000
# Docs → http://127.0.0.1:8000/docs
# Streamlit (if enabled) → http://127.0.0.1:8501
```

**Smoke test:**

```bash
# Register (201 first time; 400 if re-run)
curl -s -X POST http://127.0.0.1:8000/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"email":"me@example.com","password":"Sup3rSaf3!Pass"}' | jq

# Login (form-encoded) → TOKEN
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/auth/login \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode "username=me@example.com" \
  --data-urlencode "password=Sup3rSaf3!Pass" | jq -r .access_token)

# Protected create
curl -s -X POST http://127.0.0.1:8000/items \
  -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"name":"secure item","description":"via docker"}' | jq

# ML predict
curl -s -X POST http://127.0.0.1:8000/ml/predict \
  -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"sepal_length":5.1,"sepal_width":3.5,"petal_length":1.4,"petal_width":0.2}' | jq

# View history
curl -s "http://127.0.0.1:8000/ml/predictions?limit=20" \
  -H "Authorization: Bearer $TOKEN" | jq
```

> **zsh tip:** if your password has `!`, keep using `--data-urlencode` or single-quote the value to avoid `event not found`.

---

## Local Development

```bash
# Python 3.12 recommended
conda create -y -n ml python=3.12
conda activate ml

pip install -r requirements.txt -r requirements-dev.txt
cp .env.example .env

# create tables
alembic upgrade head

# run API (hot reload)
uvicorn app.main:app --reload --port 8000

# optional UI (new shell)
cd ui && streamlit run streamlit_app.py
```

### Environment variables

Create `.env` (local) or use `.env.docker` (compose):

```
DATABASE_URL=postgresql://appuser:app_password@localhost:5432/appdb
SECRET_KEY=change-me-please
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

## API Overview

**Auth**

* `POST /auth/register`
* `POST /auth/login` (form fields: `username`, `password`)
* `GET /auth/me` (auth)

**Items**

* `GET /items` (public)
* `GET /items/{id}` (public)
* `POST /items` (auth)
* `PUT /items/{id}` (auth)
* `DELETE /items/{id}` (auth)

**ML**

* `POST /ml/predict` (auth) — returns predicted label (+ probability)
* `GET /ml/predictions` (auth) — supports `limit`, `offset`, `label`

Docs: **`/docs`** (Swagger) and **`/redoc`**.

---

## Data Model (simplified)

* **users**: `id`, `email` (unique), `hashed_password`, `created_at`
* **items**: `id`, `name`, `description`, `created_at`
* **predictions**: `id`, `user_id`, `features` (JSONB), `pred_label`, `pred_confidence`, `created_at`

Migrations managed via **Alembic**.

---

## Project Structure

```
quickapi/
├─ app/
│  ├─ main.py            # FastAPI app + router includes
│  ├─ models.py          # SQLAlchemy models (Item, User, Prediction)
│  ├─ schemas.py         # Pydantic models
│  ├─ db.py              # SessionLocal & Base
│  ├─ security.py        # JWT, password hashing, dependencies
│  ├─ config.py          # Settings (pydantic-settings)
│  └─ routers/
│     ├─ auth.py
│     ├─ items.py
│     └─ ml.py
├─ migrations/           # Alembic versions
├─ scripts/
│  └─ train_iris.py      # trains artifacts/iris_clf.joblib
├─ artifacts/
│  ├─ iris_clf.joblib
│  └─ iris_meta.json
├─ ui/
│  └─ streamlit_app.py
├─ assets/               # Images for README (when available)
├─ docker-compose.yml
├─ Dockerfile
├─ requirements.txt
├─ requirements-dev.txt
├─ ruff.toml
├─ .pre-commit-config.yaml
├─ .env.example
└─ README.md
```

---

## Tests & Linting

```bash
pytest -q

pre-commit install
pre-commit run --all-files

# manual (if needed)
ruff check --fix .
ruff format .
```

---

## Docker Tips

```bash
docker compose ps
docker compose logs -f api
docker compose down          # stop (keep data)
docker compose down -v       # stop + delete DB volume (fresh DB)
```

---

## Troubleshooting

* **`python-multipart` error in container** → rebuild API image
  `docker compose build --no-cache api && docker compose up -d`
* **zsh `event not found`** → quote or `--data-urlencode` passwords with `!`
* **DB connection issues** → ensure `db` service is healthy and `DATABASE_URL` matches
* **Migrations mismatch** → `alembic upgrade head`
* **403/401 from protected endpoints** → ensure `Authorization: Bearer <token>` header is present
* **Pre-commit hook failures** → run `pre-commit run --all-files` to fix formatting issues

---

## Security Notes

* Never commit secrets (keys/tokens). Rotate any accidentally exposed creds immediately.
* Lock CORS origins in production.
* Enforce unique indexes & strong password policy.

---
## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

Copyright (c) 2025 **Dushyant Singh Pawar**

# quickapi

FastAPI + PostgreSQL + Alembic + Auth + ML (Iris) + Streamlit + Docker Compose.

## Features
- JWT auth (strong password rules + email validation)
- Items CRUD: public read, protected create/update/delete
- ML endpoint `/ml/predict` (scikit-learn Iris) with prediction logging to Postgres
- History endpoint `/ml/predictions`
- Streamlit UI (login, predict, items)
- Docker Compose for reproducible dev (API + DB)
- Alembic migrations, pytest, pre-commit (black, ruff, isort)

---

## Quickstart (Docker)

```bash
docker compose up -d --build
# API docs → http://127.0.0.1:8000/docs
# DB is internal to compose; if mapped, psql is on localhost:5433
````

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
conda create -y -n ml python=3.12
conda activate ml

pip install -r requirements.txt -r requirements-dev.txt
cp .env.example .env

# create tables
alembic upgrade head

# run API
uvicorn app.main:app --reload --port 8000

# optional UI (new tab)
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

* `GET /health`
* `POST /auth/register`
* `POST /auth/login` (form: `username`, `password`)
* `GET /auth/me` (auth)
* `GET /items` (public)
* `GET /items/{id}` (public)
* `POST /items` (auth)
* `PUT /items/{id}` (auth)
* `DELETE /items/{id}` (auth)
* `POST /ml/predict` (auth)
* `GET /ml/predictions` (auth; supports `limit`, `offset`, `label`)

OpenAPI: **/docs** and **/redoc**.

---

## Tests & Linting

```bash
pytest -q

pre-commit install
pre-commit run --all-files

# manual format/lint (if needed)
ruff --fix .
black .
isort .
```

---

## Project Structure (abridged)

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
│  └─ train_iris.py
├─ artifacts/
│  ├─ iris_clf.joblib
│  └─ iris_meta.json
├─ ui/
│  └─ streamlit_app.py
├─ Dockerfile
├─ docker-compose.yml
├─ requirements.txt
├─ requirements-dev.txt
├─ .pre-commit-config.yaml
├─ ruff.toml
├─ .env.example
└─ README.md
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

* **`python-multipart` error in container** → rebuild image
  `docker compose build --no-cache api && docker compose up -d`
* **zsh `event not found`** → quote or `--data-urlencode` passwords with `!`
* **DB connection issues** → ensure `db` service is up and `DATABASE_URL` matches
* **Migrations mismatch** → `alembic upgrade head`

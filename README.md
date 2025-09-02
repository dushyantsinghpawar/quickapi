# quickapi

FastAPI + PostgreSQL + Alembic + Auth + ML (Iris) + Streamlit + Docker Compose.

## Quickstart (Docker)
```bash
cp .env.example .env
docker compose up -d --build
# API: http://127.0.0.1:8000/docs
conda create -y -n ml python=3.12
conda activate ml
pip install -r requirements.txt -r requirements-dev.txt
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload --port 8000
# Streamlit UI:
cd ui && streamlit run streamlit_app.py
pytest -q

### 6) Commit & push
```bash
git add -A
git commit -m "Docs/CI: add README, env example, ruff.toml, requirements, CI, dockerignore" --no-verify
git push

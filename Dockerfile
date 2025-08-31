FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN pip install --no-cache-dir \
  fastapi "uvicorn[standard]" sqlalchemy psycopg2-binary pydantic-settings python-dotenv alembic \
  passlib "python-jose[cryptography]" email-validator python-multipart \
  scikit-learn joblib numpy requests
COPY . /app
EXPOSE 8000
CMD ["bash","-lc","alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]

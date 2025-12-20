# Feature Votes API

Система голосования за фичи проекта. Пользователи могут предлагать свои и голосовать за уже предложенные фичи.


## Быстрый старт
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt -r requirements-dev.txt
pre-commit install
uvicorn app.main:app --reload
```
н
## Ритуал перед PR
```bash
ruff check --fix .
black .
isort .
pytest -q
pre-commit run --all-files
```

## Тесты
```bash
pytest -q
```

## CI
В репозитории настроен workflow **CI** (GitHub Actions) — required check для `main`.
Badge добавится автоматически после загрузки шаблона в GitHub.

## Контейнеры
```bash
docker build -t feature-votes .
docker run --rm -p 8000:8000 feature-votes
# или
docker compose up --build
```

### Безопасность
- Read-only файловая система
- Health checks
- Security hardening (no-new-privileges)
- Multi-stage build для минимального размера образа
- Запуск под non-root пользователем

### Запуск
```bash
# Базовый запуск
docker compose up --build

# Полный стек (БД + Redis)
docker compose --profile full up --build

# Проверка здоровья
curl http://localhost:8000/health

## Эндпойнты
### default
- `GET /health` → `{"status": "ok"}`
- `POST /items?name=...` — демо-сущность
- `GET /items/{id}`
### features
- `GET /features` - список всех фич
- `POST /features` - создать фичу
- `GET /features/{id}` - получить фичу по id
- `PUT /features/{id}` - обновить фичу по id
- `DELETE /features/{id}` - удалить фичу по id
- `POST /features/{id}/vote` - проголосовать за фичу по id
- `GET /features/top` - топ фич по числу голосов

## Примеры использования

### Получить список всех фич
curl -X GET "http://localhost:8000/features/"
### Создать фичу
curl -X POST "http://localhost:8000/features/" \
  -H "Content-Type: application/json" \
  -d '{"title":"feature title","desc":"feature desc"}'
### Получить фичу по id
curl -X GET "http://localhost:8000/features/1"
### Обновить фичу по id
curl -X PUT "http://localhost:8000/features/1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "new title",
    "desc": "new desc"
  }'
### Удалить фичу по id
curl -X DELETE "http://localhost:8000/features/1"
### Получить топ фич по числу голосов
curl -X GET "http://localhost:8000/features/top"
### Проголосовать за фичу по id
curl -X POST "http://localhost:8000/features/1/vote" \
  -H "Content-Type: application/json" \
  -d '{"value":1}'

## Формат ошибок
Все ошибки — JSON-обёртка:
```json
{
  "error": {"code": "not_found", "msg": "feature not found"}
}
```

См. также: `SECURITY.md`, `.pre-commit-config.yaml`, `.github/workflows/ci.yml`.

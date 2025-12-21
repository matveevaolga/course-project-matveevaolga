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

## DAST Security Scanning (P11)

### ZAP Integration
Проект интегрирован с OWASP ZAP для динамического тестирования безопасности:

- **Workflow**: `.github/workflows/ci-p11-dast.yml`
- **Триггеры**: ручной запуск, push в ветку P11, PR в main
- **Конфигурация**: адаптирована под FastAPI (отключены нерелевантные проверки)
- **Артефакты**: HTML и JSON отчёты сохраняются в `EVIDENCE/P11/`

### Запуск сканирования
Ручной запуск через GitHub Actions UI или создание PR в main.

## Интерпретация результатов:

### Отчёты содержат:
Уровень риска (High/Medium/Low/Informational)

Описание уязвимостей

Рекомендации по исправлению

### Критерии приёма рисков:

High/Medium риски - требуют немедленного исправления

Low риски - исправляются в течение спринта

Informational - принимаются с обоснованием

## DAST Security Scanning

Проект интегрирован с OWASP ZAP для автоматического тестирования безопасности:

### Конфигурация
- **Workflow**: `.github/workflows/ci-p11-dast.yml`
- **Триггеры**: 
  - Ручной запуск (`workflow_dispatch`)
  - Push в ветку `P11/*`
  - Pull Request в `main`
- **Адаптация**: Отключены 80+ нерелевантных проверок для API
- **Артефакты**: HTML/JSON отчеты в `EVIDENCE/P11/`

### Процесс работы
1. **Сканирование**: ZAP тестирует поднятое в Docker Compose приложение
2. **Анализ**: Результаты автоматически анализируются в PR
3. **Действия**:
   - High/Medium риски требуют немедленного исправления
   - Low риски исправляются в течение спринта  
   - Informational - принимаются с обоснованием
4. **Документирование**: Все решения фиксируются в `P11_ANALYSIS.md`

### Пример использования
```bash

# Просмотр отчета после сканирования
open EVIDENCE/P11/zap_baseline.html

# Проверка конкретного алерта
grep -A5 -B5 "Missing Anti-clickjacking" EVIDENCE/P11/zap_baseline.json

## Security Scanning

This project uses multiple security scanners:

### Static Analysis
- Hadolint: Dockerfile linting
- Checkov: Infrastructure as Code scanning
- Trivy: Container vulnerability scanning

### Reports
Security reports are available in EVIDENCE/P12/:
- hadolint_report.json - Dockerfile best practices
- checkov_report.json - IaC security checks  
- trivy_report.json - Container vulnerabilities

### Hardening Measures
- Non-root container execution
- Resource limits
- Read-only filesystem
- Network isolation
- Regular security updates
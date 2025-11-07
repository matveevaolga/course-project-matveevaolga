# ADR-002: Выбор in-memory хранилища для данных

## Status
Accepted (2025-11-03)

## Context
Проект Feature Votes начинался как MVP с требованиями:
- Максимально быстрый запуск и прототипирование
- Отсутствие внешних зависимостей для разработки
- Простота тестирования и отладки
- Данные не требуют persistence между перезапусками

Требования из P03 NFR:
- Простота развертывания
- Минимальная инфраструктура

## Decision
Мы выбрали in-memory хранилище на базе словарей Python:

```python
class FeatureStore:
    def __init__(self):
        self.features: Dict[int, dict] = {}
        self.votes: Dict[int, dict] = {}
        self._feat_cnt = 1
        self._vote_cnt = 1
```

**Архитектурные компоненты:**
- Словари Python для features и votes
- Автоинкрементные счетчики ID
- In-memory хранение без persistence

**Alternatives Considered**

**Альтернатива 1: PostgreSQL**
**Плюсы:**
- Надежное хранение данных
- Транзакции и ACID
- Масштабируемость

**Минусы:**
- Сложность настройки и развертывания
- Дополнительная зависимость
- Overkill для MVP

**Альтернатива 2: SQLite**
**Плюсы:**
- Простота использования
- Файловое хранение
- SQL-синтаксис

**Минусы:**
- Требует миграции кода
- Менее производительно для частых записей

**Альтернатива 3: Redis**
**Плюсы:**
- Высокая производительность
- In-memory с persistence
- Богатые структуры данных

**Минусы:**
- Дополнительная инфраструктура
- Кривая обучения

## Consequences
**Положительные:**
- Простота разработки - минимальная настройка
- Быстрая итерация - изменения без миграций БД
- Простое тестирование - изоляция тестовых данных
- Нет внешних зависимостей - самодостаточность

**Отрицательные:**
- Потеря данных при перезапуске - нет persistence
- Ограниченная масштабируемость - один экземпляр приложения
- Ограничения запросов - простые операции со словарями

## Security Impact
**Риски:**
- Потеря данных не критична для MVP
- Нет рисков связанных с БД (SQL injection, etc.)

**Связь с Threat Modeling (P04):**
- Упрощает модель угроз (меньше компонентов)
- Нет рисков связанных с доступом к БД

## Rollout Plan
**Definition of Done (DoD):**
- Реализован FeatureStore с in-memory хранилищем
- CRUD операции для фич и голосов
- Тесты покрывают все сценарии работы хранилища

**План внедрения:**
- Этап 1: Разработка FeatureStore (1 день)
- Этап 2: Интеграция с API endpoints (1 день)
- Этап 3: Тестирование (1 день)

## References
- [Исходный код FeatureStore](https://github.com/matveevaolga/course-project-matveevaolga/blob/p05-caching-adr/app/features/store.py)
- [P03 NFR Requirements](https://github.com/matveevaolga/course-project-matveevaolga/blob/p03-nfr-requirements/docs/NFR.md)
- [ADR-001: Caching Implementation](https://github.com/matveevaolga/course-project-matveevaolga/blob/p05-caching-adr/app/docs/ADR-001-caching.md)

## Related Issues
- [Issue #12](https://github.com/matveevaolga/course-project-matveevaolga/issues/12) - ADR-002 Storage Architecture

## Commits
- Реализация: коммит [f8282c6](https://github.com/matveevaolga/course-project-matveevaolga/commit/f8282c6a17892fa90345fff21da6a66785bcc280)

## Related ADRs
- [ADR-001: Caching implementation](https://github.com/matveevaolga/course-project-matveevaolga/blob/p05-caching-adr/app/docs/ADR-001-caching.md)
- [ADR-003: Stateless architecture](https://github.com/matveevaolga/course-project-matveevaolga/blob/p05-caching-adr/app/docs/ADR-003-stateless-architecture.md)

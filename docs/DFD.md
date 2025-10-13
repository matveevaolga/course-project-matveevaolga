# Data Flow Diagram (DFD) for Feature Votes System

## Контекстная диаграмма (Уровень 0)

```mermaid
graph TD
    USER[Пользователь] -->|F1: Запросы API<br/>GET/POST/PUT/DELETE| API[Feature Votes API]
    API -->|F2: Ответы<br/>JSON данные| USER

    USER -->|F3: Голосование<br/>POST /vote| API
    USER -->|F4: Статистика<br/>GET /stats| API

    API -->|F5: Чтение/запись данных| STORE[(In-Memory Storage)]

    subgraph Trust Boundary [Доверенная зона]
        API
        STORE
    end
```
**Описание потоков уровня 0**:
- F1: Управление фичами (создание, просмотр, обновление, удаление)
- F2: Ответы API в формате JSON
- F3: Операции голосования за фичи
- F4: Запросы статистики и аналитики
- F5: Внутренние операции с данными

## Логическая архитектура (Уровень 1)

```mermaid
graph TD
    USER[Внешний пользователь] -->|F1.1: HTTP запросы| WEB[FastAPI Web Server]

    WEB -->|F1.2: Валидация| VALID[Validation Layer]
    VALID -->|F1.3: Обработанные данные| WEB

    WEB -->|F2.1: CRUD операции| STORE[Feature Store]
    STORE -->|F2.2: Данные фич| MEM_FEAT[(Features Data)]
    STORE -->|F2.3: Данные голосов| MEM_VOTE[(Votes Data)]

    WEB -->|F3.1: Запрос статистики| STATS[Statistics Engine]
    STATS -->|F3.2: Агрегированные данные| MEM_STATS[(Stats Cache)]

    WEB -->|F4.1: Проверка лимитов| RATE[Rate Limiter]
    RATE -->|F4.2: Лимиты запросов| MEM_LIMIT[(Rate Limits)]

    subgraph Trust Boundary [Доверенная зона]
        WEB
        VALID
        STORE
        STATS
        RATE
        MEM_FEAT
        MEM_VOTE
        MEM_STATS
        MEM_LIMIT
    end

    subgraph External [Внешняя зона]
        USER
    end
```

**Описание компонентов уровня 1**:

- WEB: FastAPI веб-сервер (обработка HTTP запросов)
- VALID: Слой валидации (проверка входных данных)
- STORE: Менеджер хранения (CRUD операции)
- STATS: Движок статистики (агрегация данных)
- RATE: Ограничитель запросов (защита от DoS)

**Потоки данных уровня 1**:

- F1.1: Входящие HTTP запросы от пользователей
- F1.2: Валидация параметров и payload
- F1.3: Очищенные и проверенные данные
- F2.1: Операции с хранилищем (create, read, update, delete)
- F2.2: Данные фич (название, описание, метаданные)
- F2.3: Данные голосов (user_id, feature_id, значение, timestamp)
- F3.1: Запросы расчетов статистики
- F3.2: Кэшированные результаты статистики
- F4.1: Проверка ограничений частоты запросов
- F4.2: Хранение счетчиков запросов

## Диаграмма процессов обработки ключевых операций (Уровень 2)

### Процесс голосования

```mermaid
flowchart TD
    START[Начало голосования] --> VALIDATE{Валидация запроса}
    VALIDATE -->|Невалидный| ERROR1[Ошибка 422]
    VALIDATE -->|Валидный| RATELIMIT{Проверка лимитов}

    RATELIMIT -->|Превышен| ERROR2[Ошибка 429]
    RATELIMIT -->|В пределах| CHECKFEATURE{Существует ли фича?}

    CHECKFEATURE -->|Нет| ERROR3[Ошибка 404]
    CHECKFEATURE -->|Да| SAVEVOTE[Сохранить голос]

    SAVEVOTE --> UPDATESTATS[Обновить статистику]
    UPDATESTATS --> SUCCESS[Успешный ответ 200]

    ERROR1 --> END[Конец]
    ERROR2 --> END
    ERROR3 --> END
    SUCCESS --> END
```

### Процесс создания фичи

```mermaid
flowchart TD
    START[Запрос создания] --> VALIDATE{Валидация данных}
    VALIDATE -->|Ошибка| ERROR[422 Validation Error]
    VALIDATE -->|Успех| SANITIZE[Санитизация контента]

    SANITIZE --> CREATEFEATURE[Создать запись фичи]
    CREATEFEATURE --> LOG[Записать в лог]
    LOG --> SUCCESS[201 Created]

    ERROR --> END[Конец]
    SUCCESS --> END
```

### Trust Boundaries

**Основные границы**:

1) Внешняя граница: Пользователь ↔ API
- Недоверенные входные данные
- Требуется валидация и санитизация

2) Внутренняя граница: Компоненты приложения
- Доверенная коммуникация
- Контроль целостности данных

**Ключевые точки безопасности**:

- F1.1: Входная валидация (XSS, SQL injection protection)
- F4.1: Rate limiting (DoS protection)
- F2.1: Авторизация операций (если будет реализована)
- F1.2: Санитизация данных (HTML/JS escaping)


### Связь с компонентами кода

| DFD Компонент | Файл в коде           | Реализация                     |
|---------------|-----------------------|--------------------------------|
| WEB           | app/main.py           | FastAPI приложение             |
| VALID         | app/features/models.py | Pydantic модели               |
| STORE         | app/features/store.py | FeatureStore класс            |
| STATS         | app/features/routes.py | Эндпоинт /stats               |
| RATE          | app/main.py, app/features/routes.py | @limiter декораторы |
| MEM_*         | В памяти Python       | Словари и списки              |

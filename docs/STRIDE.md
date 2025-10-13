# STRIDE Threat Analysis for Feature Votes

| Узел/Поток | Угроза | STRIDE | Описание |
|------------|---------|---------|-----------|
| Пользователь → API | Подделка пользователя | **S**poofing | Анонимный доступ позволяет накручивать голоса |
| POST /vote | Повторная отправка голосов | **T**ampering | Манипуляция с голосами без авторизации |
| In-Memory Storage | Потеря данных при перезапуске | **R**epudiation | Нет аудита кто и когда голосовал |
| GET /features | Раскрытие списка всех фич | **I**nformation Disclosure | Потенциально чувствительная информация |
| Feature Store | Отказ в обслуживании | **D**enial of Service | Множественные запросы могут перегрузить систему |
| POST /features | Создание фич с вредоносным контентом | **E**levation of Privilege | Любой может создавать фичи без ограничений |
| API Validation | Обход валидации входных данных | **T**ampering | Injection атаки через специальные payloads |
| Statistics Endpoint | Манипуляция статистикой | **I**nformation Disclosure | Искажение результатов голосования |
| Health Check | DoS через health endpoint | **D**enial of Service | Постоянные запросы к /health |
| Vote Storage | Подмена голосов в памяти | **T**ampering | Модификация данных напрямую в store |
| User Input | XSS через поля title/desc | **S**poofing | Внедрение恶意脚本 в пользовательский ввод |
| API Rate Limits | Обход ограничений частоты | **D**enial of Service | Отсутствие rate limiting |

**Исключения:**
- SQL Injection: не применимо (используется in-memory storage)
- Network sniffing: не в scope (приложение локальное)

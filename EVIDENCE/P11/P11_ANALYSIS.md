# P11 DAST Scan Analysis
## Общая информация
- **Дата сканирования**: 2025-12-15 21:27:15
- **Версия ZAP**: 2.17.0
- **Цель**: http://172.18.0.2:8000
- **Конфигурация**: Docker Compose с реальными зависимостями
- **Настройки ZAP**: Отключены нерелевантные проверки для API

## Результаты сканирования

### Статистика алертов
- **High**: 0
- **Medium**: 3
- **Low**: 2
- **Informational**: 1

**Всего алертов**: 6

### Анализ критических алертов (для C4 ★★2)

1. **Content Security Policy (CSP) Header Not Set** (риск: Medium)
   - **URL**: N/A
   - **Описание**: N/A
   - **Рекомендуемое решение**: <p>Ensure that your web server, application server, load balancer, etc. is configured to set the Content-Security-Policy header.</p>
   - **Действие**: Требует исправления в коде приложения

2. **Missing Anti-clickjacking Header** (риск: Medium)
   - **URL**: N/A
   - **Описание**: N/A
   - **Рекомендуемое решение**: <p>Modern Web browsers support the Content-Security-Policy and X-Frame-Options HTTP headers. Ensure one of them is set on all web pages returned by your site/app.</p><p>If you expect the page to be fr
   - **Действие**: Требует исправления в коде приложения


## Интеграция в CI/CD (C5 ★★2)

1. **Workflow интегрирован в CI**: запускается при push в main, создании PR и вручную
2. **Concurrency настроен**: предотвращает накопление висящих запусков
3. **Адаптирован под проект**: используется Docker Compose, реальные зависимости
4. **Настройки ZAP оптимизированы**: отключены нерелевантные для API проверки

## Ссылки на артефакты (C3 ★★2)

1. HTML отчёт: доступен в артефакте zap-reports
2. JSON отчёт: для автоматического анализа
3. Анализ: этот файл с результатами и рекомендациями

---
*Создано автоматически. Для достижения ★★2 уровня добавьте фиксы для критических алертов или обоснование принятия рисков.*

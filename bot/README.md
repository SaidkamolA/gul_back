# Телеграм Бот для Администратора

Этот бот предназначен для удобного управления заказами администратором интернет-магазина.

## Основные функции

- **Просмотр заказов**:
  - Ожидающие подтверждения
  - Одобренные заказы
  - Отклоненные заказы
  - Фильтрация по периоду времени (сегодня, 3 дня, неделя, месяц)

- **Статистика**:
  - Отображение общего количества заказов и их распределения по статусам
  - Процентное соотношение заказов по категориям

- **Настройки**:
  - Управление уведомлениями
  - Изменение контактных данных

- **Поиск заказов**:
  - Поиск по ID заказа

## Команды

- `/start` - Запуск бота и отображение главного меню
- `/find_order ID` - Поиск заказа по его ID номеру

## Требования

- Python 3.7 или выше
- aiogram 3.x
- requests
- python-dotenv

## Начало работы

1. Настройте переменные окружения в файле `.env`:
   ```
   BOT_TOKEN=ваш_токен_от_BotFather
   ADMIN_CHAT_ID=ваш_id_чата
   ```

2. Запустите бота:
   ```
   python bot.py
   ```

## Структура проекта

- `bot.py` - Главный файл бота
- `handlers.py` - Обработчики команд и кнопок
- `order_checker.py` - Фоновый процесс проверки новых заказов
- `config.py` - Файл конфигурации

## Интерфейс

Интерфейс бота построен на кнопках и интуитивно понятен. После запуска бота введите команду `/start`, чтобы увидеть главное меню с доступными функциями.

## Настройка уведомлений

В файле `config.py` можно настроить параметры уведомлений:
- `NOTIFICATIONS_ENABLED` - включение/отключение уведомлений
- `NOTIFICATION_SOUND` - включение/отключение звука уведомлений 
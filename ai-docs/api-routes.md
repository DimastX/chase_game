# API Routes Documentation - Chase Game

## Обзор API

Chase Game предоставляет REST API для управления игровым процессом, включая создание игр, управление заданиями, транспортом и геолокацией. Все эндпоинты возвращают JSON и используют стандартные HTTP коды ответов.

**Base URL:** `https://chasegametestapi.dimastx.keenetic.link`

## Управление игрой

### GET `/api/game`
Проверка работоспособности API.

**Запрос:** Без параметров  
**Ответ:**
```json
{
  "message": "Добро пожаловать в API игры!"
}
```

### POST `/create-game`
Создание новой игры с тремя игроками.

**Запрос:**
```json
{
  "password": "string",
  "playerNames": ["player1", "player2", "player3"]
}
```

**Ответ (201):**
```json
{
  "message": "Игра успешно создана!"
}
```

**Ошибки:**
- `400` - Необходимо ввести имена для 3 игроков

### POST `/join-game`
Присоединение игрока к существующей игре.

**Запрос:**
```json
{
  "gameNumber": "integer",
  "playerName": "string", 
  "password": "string"
}
```

**Ответ (200):**
```json
{
  "status": "runner|chaser",
  "gameNumber": "integer",
  "playerNumber": "integer",
  "points": "integer",
  "currentTask": "integer|null"
}
```

**Ошибки:**
- `400` - Все поля обязательны для заполнения
- `403` - Неверный пароль
- `404` - Игра не найдена / Игрок не найден в этой игре

### GET `/games`
Получение списка всех игр.

**Запрос:** Без параметров  
**Ответ:**
```json
[
  {
    "id": "integer",
    "players": ["string", "string", "string"],
    "status": "string"
  }
]
```

### POST `/catch`
Смена ролей игроков (догоняющий поймал убегающего).

**Запрос:**
```json
{
  "player_id": "integer"
}
```

**Ответ:**
```json
{
  "message": "Роли игроков изменены"
}
```

## Игровая механика

### GET `/api/runner_data`
Получение данных убегающего игрока.

**Параметры URL:** `?player_id=integer`

**Ответ:**
```json
{
  "points": "integer",
  "refuseTime": "datetime|null",
  "currentTask": {
    "id": "integer",
    "description": "string",
    "task_cost": "integer"
  }
}
```

**Ошибки:**
- `400` - player_id не передан
- `404` - Игрок не найден

### POST `/api/get_task_by_difficulty`
Получение трех случайных заданий по уровню сложности.

**Запрос:**
```json
{
  "player_id": "integer",
  "difficulty": "easy|medium|hard"
}
```

**Ответ:**
```json
[
  {
    "id": "integer",
    "description": "string",
    "task_cost": "integer"
  }
]
```

**Ошибки:**
- `403` - Действия заблокированы из-за отказа от задания

### POST `/api/choose_task`
Выбор конкретного задания из предложенных.

**Запрос:**
```json
{
  "player_id": "integer",
  "task_id": "integer"
}
```

**Ответ:**
```json
{
  "points": "integer",
  "currentTask": {
    "id": "integer", 
    "description": "string",
    "task_cost": "integer"
  }
}
```

### POST `/api/complete_task`
Завершение выполнения задания и начисление очков.

**Запрос:**
```json
{
  "player_id": "integer",
  "task_id": "integer"
}
```

**Ответ:**
```json
{
  "message": "Задание выполнено!",
  "points": "integer",
  "task_cost": "integer"
}
```

**Ошибки:**
- `404` - Игрок не найден / Задание не найдено

### POST `/api/refuse_task`
Отказ от задания с установкой таймаута на 3 минуты.

**Запрос:**
```json
{
  "player_id": "integer",
  "task_id": "integer"
}
```

**Ответ:**
```json
{
  "message": "Вы отказались от задания.",
  "refuse_time": "datetime"
}
```

**Ошибки:**
- `404` - Игрок не найден / Задание не найдено

### POST `/api/get_new_task`
Получение случайного задания (устаревший метод).

**Запрос:**
```json
{
  "player_id": "integer"
}
```

**Ответ:**
```json
{
  "points": "integer",
  "currentTask": {
    "id": "integer",
    "description": "string", 
    "task_cost": "integer"
  }
}
```

**Ошибки:**
- `404` - Игрок не найден / Нет доступных заданий

## Транспорт и геолокация

### POST `/api/runner_transport`
Списание очков за использование транспорта.

**Запрос:**
```json
{
  "runner_id": "integer",
  "transport_id": "integer",
  "stops": "integer"
}
```

**Ответ (200):**
```json
{
  "message": "Транспортный расход списан",
  "points": "integer"
}
```

**Ошибки:**
- `400` - Транспорт не выбран / Недостаточно очков
- `403` - Действия заблокированы из-за отказа от задания
- `404` - Игрок не найден

### GET `/api/transports`
Получение списка доступного транспорта.

**Запрос:** Без параметров  
**Ответ:**
```json
[
  {
    "id": "integer",
    "type": "string",
    "cost": "integer"
  }
]
```

### POST `/api/update-location`
Обновление координат игрока.

**Запрос:**
```json
{
  "player_id": "integer",
  "latitude": "float",
  "longitude": "float"
}
```

**Ответ:**
```json
{
  "status": "success"
}
```

## Интеграция с Telegram

### POST `/api/verify-telegram-user`
Верификация пользователя Telegram Mini App.

**Запрос:**
```json
{
  "initData": "string",
  "user_id": "string"
}
```

**Ответ:**
```json
{
  "verified": true,
  "games": [],
  "auth_token": "string"
}
```

## Коды ошибок и статусы

### HTTP коды ответов
- `200` - Успешный запрос
- `201` - Ресурс создан
- `400` - Неверные параметры запроса
- `403` - Доступ запрещен (блокировка из-за отказа)
- `404` - Ресурс не найден
- `500` - Внутренняя ошибка сервера

### Система блокировок
При отказе от задания игрок блокируется на 3 минуты. В этот период запросы к следующим эндпоинтам возвращают ошибку `403`:
- `/api/get_task_by_difficulty`
- `/api/runner_transport`

### Игровые ограничения
- Максимальное количество очков: 1000
- Количество игроков в игре: 3
- Количество заданий при выборе по сложности: 3
- Время блокировки при отказе: 3 минуты

### Уровни сложности заданий
- **easy**: 100-300 очков
- **medium**: 200-350 очков  
- **hard**: 250-500 очков

### Типы транспорта
- **Автобус/троллейбус**: 100 очков за остановку
- **Трамвай**: 150 очков за остановку
- **Самокат**: 30 очков за остановку
- **Электричка**: 450 очков за остановку

## Примеры использования

### Создание игры и присоединение
1. `POST /create-game` - создать игру
2. `POST /join-game` - присоединиться как конкретный игрок
3. `GET /api/runner_data` - получить данные для убегающего

### Игровой цикл для убегающего
1. `POST /api/get_task_by_difficulty` - получить задания
2. `POST /api/choose_task` - выбрать задание
3. `POST /api/complete_task` или `POST /api/refuse_task` - завершить или отказаться
4. `POST /api/runner_transport` - потратить очки на транспорт

### Смена ролей
1. `POST /catch` - догоняющий поймал убегающего
2. Роли автоматически меняются по кругу 
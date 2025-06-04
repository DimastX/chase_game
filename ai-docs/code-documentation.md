# Техническая документация и примеры кода Chase Game

## Обзор архитектуры

Chase Game построен на архитектуре клиент-сервер с RESTful API и базой данных SQLite.

```
Frontend (React) ←→ REST API (Flask) ←→ Database (SQLite)
                          ↓
                Geographic APIs (2GIS, OpenStreetMap)
```

## Установка и запуск

### Backend (сервер)
```bash
# Переход в директорию сервера
cd server

# Установка зависимостей
pip install -r ../requirements.txt

# Запуск сервера
python app.py
```

### Frontend (клиент)
```bash
# Переход в директорию клиента
cd client

# Установка зависимостей
npm install

# Запуск разработческого сервера
npm start
```

## Модели данных

### Игра (Game)
```python
class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(80), nullable=False)
    player1_name = db.Column(db.String(80))
    player2_name = db.Column(db.String(80)) 
    player3_name = db.Column(db.String(80))
    players = db.relationship('Player', backref='game')
```

### Игрок (Player)
```python
class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'))
    status = db.Column(db.String(50))  # 'runner' или 'chaser'
    points = db.Column(db.Integer, default=0)
    refuse_time = db.Column(db.DateTime)
    current_task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    completed_tasks = db.Column(db.String(1000))
```

### Задание (Task)
```python
class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    difficulty = db.Column(db.String, nullable=False)  # 'easy', 'medium', 'hard'
    refuse_time_minutes = db.Column(db.Integer, default=10)
```

## Примеры API запросов

### Создание игры
```javascript
// Frontend (React)
const createGame = async (gameData) => {
    const response = await fetch(`${API_URL}/create-game`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            password: "secret123",
            playerNames: ["Алексей", "Мария", "Дмитрий"]
        })
    });
    return await response.json();
};
```

```python
# Backend (Flask)
@app.route('/create-game', methods=['POST'])
def create_game_route():
    data = request.get_json()
    password = data['password']
    player_names = data['playerNames']

    if len(player_names) != 3:
        return jsonify({'error': 'Необходимо ввести имена для 3 игроков'}), 400

    create_game(password, player_names)
    return jsonify({'message': 'Игра успешно создана!'}), 201
```

### Получение заданий по сложности
```javascript
// Frontend
const getTasksByDifficulty = async (playerId, difficulty) => {
    const response = await axios.post(`${API_URL}/api/get_task_by_difficulty`, {
        player_id: playerId,
        difficulty: difficulty
    });
    return response.data;
};

// Использование
const tasks = await getTasksByDifficulty(12, 'medium');
```

```python
# Backend
@app.route('/api/get_task_by_difficulty', methods=['POST'])
def get_task_by_difficulty():
    data = request.get_json()
    player_id = data.get('player_id')
    difficulty = data.get('difficulty')
    
    player = Player.query.get(player_id)
    
    # Проверка блокировки
    if check_refuse_timeout(player):
        return jsonify({
            'error': 'Действия заблокированы из-за отказа от задания',
            'blocked_until': player.refuse_time.isoformat()
        }), 403
    
    # Получение доступных заданий
    completed_tasks = player.completed_tasks.split(',') if player.completed_tasks else []
    available_tasks = Task.query.filter_by(difficulty=difficulty)\
                               .filter(~Task.id.in_(completed_tasks)).all()
    
    # Выбор трех случайных заданий
    tasks = random.sample(available_tasks, 3)
    return jsonify([{
        'id': task.id, 
        'description': task.description, 
        'task_cost': task.cost
    } for task in tasks])
```

### Обновление местоположения
```javascript
// Frontend - получение геолокации
const updateLocation = async (playerId) => {
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(async (position) => {
            await axios.post(`${API_URL}/api/update-location`, {
                player_id: playerId,
                latitude: position.coords.latitude,
                longitude: position.coords.longitude
            });
        });
    }
};
```

## Система блокировок

```python
# Проверка таймаута отказа
def check_refuse_timeout(player):
    if player.refuse_time:
        current_time = datetime.datetime.now()
        if current_time < player.refuse_time:
            return True
    return False

# Установка блокировки при отказе
@app.route('/api/refuse_task', methods=['POST'])
def refuse_task():
    # ... проверки ...
    
    # Блокировка на 3 минуты
    player.refuse_time = datetime.datetime.now() + datetime.timedelta(minutes=3)
    player.current_task_id = None
    db.session.commit()
    
    return jsonify({
        'message': 'Вы отказались от задания.',
        'refuse_time': player.refuse_time
    }), 200
```

## Интеграция с 2GIS API

```python
# Класс для работы с маршрутами
class ParkRouter:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = f"https://routing.api.2gis.com/public_transport/6.0.0/global?key={api_key}"
    
    def get_routes(self, start: Tuple[float, float], end: Tuple[float, float]):
        data = {
            "locale": "ru",
            "source": {"point": {"lat": start[0], "lon": start[1]}},
            "target": {"point": {"lat": end[0], "lon": end[1]}},
            "transport": ["bus", "tram", "trolleybus"],
            "max_result_count": 5
        }
        
        response = requests.post(self.base_url, json=data)
        return parse_2gis_response(response.content)

# Использование
router = ParkRouter("API_KEY")
routes = router.get_routes((59.927067, 30.320826), (59.956156, 30.313245))
```

## Компоненты React

### Страница убегающего
```jsx
// RunnerPage.js
const RunnerPage = () => {
    const [runnerData, setRunnerData] = useState({
        points: null, 
        currentTask: null, 
        refuseTime: null
    });
    const [tasks, setTasks] = useState([]);

    // Получение данных игрока
    const fetchRunnerData = async () => {
        const playerId = localStorage.getItem('playerName');
        const response = await axios.get(
            `${API_URL}/api/runner_data?player_id=${playerId}`
        );
        setRunnerData(response.data);
    };

    // Выбор задания
    const handleChooseTask = async (task) => {
        const playerId = localStorage.getItem('playerName');
        const response = await axios.post(`${API_URL}/api/choose_task`, {
            player_id: playerId,
            task_id: task.id
        });
        setRunnerData(response.data);
        setTasks([]);
    };

    return (
        <div>
            <h1>Интерфейс убегающего</h1>
            <p>Ваши баллы: {runnerData.points}</p>
            
            {runnerData.currentTask ? (
                <TaskDisplay 
                    task={runnerData.currentTask}
                    onComplete={handleCompleteTask}
                    onRefuse={handleRefuseTask}
                />
            ) : (
                <TaskSelection 
                    tasks={tasks}
                    onGetTasks={handleGetTaskByDifficulty}
                    onChoose={handleChooseTask}
                />
            )}
        </div>
    );
};
```

# Пример игрового процесса

## Сценарий игры: "Погоня по Санкт-Петербургу"

### Подготовка игры

**Шаг 1: Создание игры**
```
Организатор:
- Заходит на сайт chase-game.ru
- Нажимает "Создать игру"
- Вводит пароль: "spb2024"
- Указывает имена игроков: ["Анна", "Борис", "Виктор"]
- Получает номер игры: #1234
```

**Шаг 2: Присоединение игроков**
```
Каждый игрок:
- Открывает приложение
- Выбирает "Присоединиться к игре"
- Вводит номер игры: 1234
- Вводит свое имя и пароль
- Система случайно назначает роли:
  * Анна - убегающая (runner)
  * Борис - догоняющий (chaser)  
  * Виктор - догоняющий (chaser)
```

### Начало игры (10:00)

**Анна (убегающая) - Метро Невский проспект**
```
Статус: 0 очков, нет активного задания
Действие: Выбирает "Получить среднее задание"

Полученные задания:
1. "Найти и сфотографировать уличного музыканта" (250 очков)
2. "Посетить ближайший музей и сделать фото экспоната" (250 очков) 
3. "Сообщить преследователям свой следующий транспорт" (150 очков)

Выбор: Задание #3 (стратегическое, дает информацию противникам)
```

**Борис и Виктор (догоняющие)**
```
Получают уведомление: "Анна выбрала задание"
Видят местоположение Анны: Метро Невский проспект
Планируют стратегию перехвата
```

### Развитие игры (10:05)

**Анна выполняет задание**
```
Анна пишет в чат: "Еду на автобусе №7 до остановки Дворцовая площадь"
Система: +150 очков
Статус: 150 очков

Списывает транспорт:
- Автобус: 100 очков × 3 остановки = 300 очков
- НО: У неё только 150 очков!
- Решение: Взять ещё одно задание
```

**Получение простого задания**
```
Анна выбирает "Получить простое задание":
1. "Найти припаркованный велосипед" (100 очков)
2. "Сделать селфи на детской площадке" (100 очков)  
3. "Найти знак 'кирпич'" (150 очков)

Выбор: Задание #3 (быстро выполнимо)
```

**Борис и Виктор реагируют**
```
Зная маршрут Анны, они:
- Борис едет к остановке Дворцовая площадь
- Виктор остается на Невском для перехвата
- Тратят очки на транспорт из стартового бонуса
```

### Кульминация (10:15)

**Анна на Дворцовой площади**
```
Статус: 300 очков (150 + 150 за найденный знак)
Действие: Ищет сложное задание для большого заработка

Сложные задания:
1. "Найти и сфотографировать кота" (300 очков)
2. "Не использовать навигацию 20 минут" (250 очков)
3. "Стрельнуть 5 сигарет у разных людей" (300 очков)

Выбор: Задание #2 (ограничивает навигацию, но выполнимо)
```

**Погоня**
```
Борис прибывает на Дворцовую площадь
Видит Анну возле Эрмитажа
Начинается физическая погоня!

Анна убегает в сторону Дворцового моста
Борис преследует, но Анна быстрее
Виктор движется на перехват к мосту
```

### Неожиданный поворот (10:25)

**Анна попадает в затруднение**
```
Задание: "20 минут без навигации"
Проблема: Заблудилась в районе Васильевского острова
Не может использовать GPS до 10:35

Борис и Виктор:
- Координируются через чат
- Сужают круг поиска
- Используют знание города в свою пользу
```

**Виктор замечает Анну (10:30)**
```
Место: Университетская набережная
Действие: Виктор бежит к Анне
Анна пытается убежать, но направление неизвестно (нет навигации)

РЕЗУЛЬТАТ: Виктор ловит Анну!
```

### Смена ролей (10:35)

**Система автоматически меняет роли:**
```
Новые роли (сдвиг по кругу):
- Анна → догоняющая (chaser)
- Борис → догоняющий (chaser)  
- Виктор → убегающий (runner)

Виктор получает очки Анны: 550 очков
Анна и Борис: сброс очков, новая охота
```

### Вторая фаза игры (10:40)

**Виктор (новый убегающий)**
```
Стартовая позиция: Университетская набережная
Стратегия: Использовать заработанные очки для дальних поездок

Выбирает сложное задание:
"Зайти в любой дом, подняться пешком до последнего этажа" (300 очков)

Планирует поездку на электричке в пригород (450 очков за поездку)
Остается 100 очков - критическая ситуация!
```

**Анна и Борис преследуют**
```
Видят, что Виктор движется к Балтийскому вокзалу
Понимают его стратегию: уехать далеко на электричке
Спешат на перехват, тратя последние очки на быстрый транспорт
```

### Финал (11:00)

**Критический момент**
```
Виктор на Балтийском вокзале:
- Выполнил задание в 9-этажном доме (+300 очков = 400 всего)
- НО: Не хватает 50 очков на электричку!
- Должен взять ещё одно задание

Анна и Борис прибывают на вокзал:
- Видят Виктора в толпе
- Начинается финальная погоня по вокзалу
```

**Развязка**
```
Виктор пытается выполнить быстрое задание:
"Найти прохожего в костюме" (100 очков)

Находит бизнесмена, делает фото
+100 очков = 500 очков общего

Успевает купить билет на электричку и скрыться!
Анна и Борис опаздывают на 2 минуты
```

## Итоги игры

**Финальные результаты:**
- **Виктор (победитель):** 500 очков, успешно скрылся
- **Анна:** Эффективная игра в роли убегающей, хорошая адаптация  
- **Борис:** Отличная командная работа, знание города

**Статистика игры:**
- Длительность: 1 час
- Заданий выполнено: 6
- Пройденное расстояние: ~15 км на транспорте + 5 км пешком
- Исследованные районы: Центр, Васильевский остров, Балтийская
- Использованный транспорт: автобус, метро, трамвай, электричка

**Образовательный эффект:**
- Изучение маршрутов общественного транспорта
- Знакомство с историческими районами
- Развитие навигационных навыков
- Социальное взаимодействие с горожанами
- Командная работа и стратегическое мышление

Этот пример демонстрирует, как техническая реализация Chase Game создает увлекательный игровой опыт, объединяющий цифровые технологии с реальным городским пространством. 
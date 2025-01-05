import random
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
tasks = [
    {"description": "Следующий транспорт, который возьмёшь должен содержать рандомную цифру", "cost": 200, "difficulty": "easy"},
    {"description": "Найди нелегальное объявление", "cost": 300, "difficulty": "easy"},
    {"description": "Доедь до ближайшего большого парка/сквера. Монетки за транспорт не списываются", "cost": 0, "difficulty": "easy"},
    {"description": "Найдите азиатский магазин/кафе", "cost": 100, "difficulty": "easy"},
    {"description": "Найдите магазин в котором продаются сувениры", "cost": 250, "difficulty": "easy"},
    {"description": "Найдите уличное графити", "cost": 100, "difficulty": "easy"},
    {"description": "Доедь до водоёма", "cost": 200, "difficulty": "easy"},
    {"description": "Накорми хотя бы 10 птиц", "cost": 300, "difficulty": "medium"},
    {"description": "Поедь на следующем транспорте, который придёт на ближайшую остановку как минимум 2 остановки", "cost": 200, "difficulty": "easy"},
    {"description": "Сообщи на каком транспорте и на какую остановку ты поедешь своим преследователям", "cost": 150, "difficulty": "medium"},
    {"description": "Найти книгу, название которой начинается на букву «М»", "cost": 200, "difficulty": "easy"},
    {"description": "Найти прохожего в костюме или рубашке", "cost": 100, "difficulty": "easy"},
    {"description": "Найти знак «кирпич»", "cost": 150, "difficulty": "easy"},
    {"description": "Пройди через подземный переход", "cost": 100, "difficulty": "easy"},
    {"description": "Найти припаркованный велосипед", "cost": 100, "difficulty": "easy"},
    {"description": "Найти велокурьера (Деливери Клаб / Яндекс еда)", "cost": 100, "difficulty": "easy"},
    {"description": "Найти рисунок мелками на асфальте или нарисовать", "cost": 350, "difficulty": "medium"},
    {"description": "Успешно взять номер телефона у девушки", "cost": 350, "difficulty": "medium"},
    {"description": "Сделать селфи на детской площадке", "cost": 100, "difficulty": "easy"},
    {"description": "Следующие 30 минут тебе нельзя пользоваться транспортом, где можно оплатить проезд «подорожником»", "cost": 100, "difficulty": "easy"},
    {"description": "Найти и сфотографировать граффити с изображением животного", "cost": 200, "difficulty": "medium"},
    {"description": "Посетить ближайший музей или галерею и сделать фото любого экспоната", "cost": 250, "difficulty": "medium"},
    {"description": "Найти и сфотографировать уличные часы", "cost": 150, "difficulty": "easy"},
    {"description": "Посетить ближайшую станцию метро и сделать фото с названием станции", "cost": 250, "difficulty": "medium"},
    {"description": "Найти и сфотографировать уличного музыканта", "cost": 250, "difficulty": "medium"},
    {"description": "Найти и сфотографировать скульптуру на здании", "cost": 200, "difficulty": "easy"},
    {"description": "Посетить ближайший книжный магазин и сфотографировать обложку книги на тему района, в котором вы находитесь", "cost": 250, "difficulty": "medium"},
    {"description": "Найдите автомобиль с номерным знаком, содержащим две одинаковые буквы подряд", "cost": 200, "difficulty": "medium"},
    {"description": "Сфотографируйте три разных вида уличных фонарей в одном кадре", "cost": 250, "difficulty": "medium"},
    {"description": "Найдите и сфотографируйте кота", "cost": 300, "difficulty": "hard"},
    {"description": "Найдите уличную вывеску с орфографической ошибкой", "cost": 300, "difficulty": "medium"},
    {"description": "Найдите и сфотографируйте три разных вида деревьев в одном парке или сквере", "cost": 200, "difficulty": "medium"},
    {"description": "До конца твоего забега ты не можешь использовать телефон для навигации", "cost": 500, "difficulty": "hard"},
    {"description": "Следующая остановка общественного транспорта должна содержать две рандомные буквы", "cost": 250, "difficulty": "medium"},
    {"description": "Выберете ближайший перекрёсток со светофором, предскажите сколько людей перейдёт на следующий зелёный", "cost": 300, "difficulty": "hard"},
    {"description": "Предскажите сколько человек зайдёт в ближайший магазин за 2 минуты", "cost": 350, "difficulty": "hard"},
    {"description": "Предскажите сколько машин пересечёт перекрёсток на следующий зелёный", "cost": 350, "difficulty": "hard"},
    {"description": "Дойти до ближайшей улицы с брусчаткой", "cost": 250, "difficulty": "hard"},
    {"description": "Найти дуб или берёзу и дотронуться", "cost": 50, "difficulty": "easy"},
    {"description": "Найти площадку с турником и сделать 5 подходов", "cost": 300, "difficulty": "hard"},
    {"description": "Найти памятник с протёртым носом и потереть", "cost": 300, "difficulty": "hard"},
    {"description": "Стрельнуть 5 сигарет у разных людей", "cost": 300, "difficulty": "hard"},
    {"description": "Зайти в любой дом неподалёку, подняться пешком до последнего этажа", "cost": 300, "difficulty": "hard"},
    {"description": "Залезть на любое дерево (минимум на полметра)", "cost": 250, "difficulty": "hard"},
    {"description": "Купить свисток и свистнуть в следующем транспорте", "cost": 250, "difficulty": "hard"},
    {"description": "20 минут не пользоваться навигатором и спросить дорогу", "cost": 250, "difficulty": "medium"},
    {"description": "Купить только лаваш в шаверме", "cost": 300, "difficulty": "hard"}
]

transports = [
    {"type": "Автобус/троллейбус","cost": 100}, 
    {"type": "Трамвай","cost": 150},
    {"type": "Самокат", "cost": 30},
    {"type": "Электричка", "cost": 450}
]

from sqlalchemy.orm import backref


class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(80), nullable=False)
    players = db.relationship('Player', backref='game')  # Связь с таблицей Player
    player1_name = db.Column(db.String(80))  # Имя первого игрока
    player2_name = db.Column(db.String(80))  # Имя второго игрока
    player3_name = db.Column(db.String(80))  # Имя третьего игрока



class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'))
    order_number = db.Column(db.Integer)  # Поле order_number
    status = db.Column(db.String(50))  # Добавьте это поле для статуса
    points = db.Column(db.Integer, default=0)    # По умолчанию 0 очков
    refuse_time = db.Column(db.DateTime)  # Время отказа
    current_task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), default=9)  # Ссылка на текущее задание. по умолчанию - стартовое
    telegram_user_id = db.Column(db.String(100))
    available_tasks = db.Column(db.String(500))  # Store comma-separated task IDs
    completed_tasks = db.Column(db.String(1000))  # Store completed task history
    estimated_travel_time = db.Column(db.Integer)  # In minutes
    remaining_travel_time = db.Column(db.Integer)  # In minutes
    time_gap = db.Column(db.Integer)  # Time gap in minutes
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def deduct_transport_cost(self, transport_id, stops):
            print("Вызван метод deduct_transport_cost")
            transport = Transport.query.get(transport_id)
            print("Транспорт:", transport)
            if transport and int(transport.cost) * int(stops) <= int(self.points):
                print("Списываем транспортный расход...")
                self.points -= int(transport.cost) * int(stops)
                db.session.commit()
                print("Транспортный расход списан успешно!")
                return True
            else:
                print(int(transport.cost))
                print(stops)
                print(int(self.points))
                print("Недостаточно очков для списания транспортного расхода!")
                return False
            
    def add_points(self, points):
        new_points = self.points + points
        if new_points > 1000:
            return False
        self.points = new_points
        return True

    # Другие атрибуты и отношения

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    difficulty = db.Column(db.String, nullable=False)  # 'easy', 'medium', 'hard'
    refuse_time_minutes = db.Column(db.Integer, default=10)

    
class Transport(db.Model):
    __tablename__ = 'transports'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(80), nullable=False)
    cost = db.Column(db.Integer, nullable=False)


def get_random_task_for_player():
    # Получаем все задания из базы данных
    tasks = Task.query.all()
    print(tasks)
    if tasks:
        # Выбираем случайное задание
        return random.choice(tasks)
    else:
        return None  # Возвращаем None, если нет заданий
    
def update_tasks(app):
    with app.app_context():
        tasks_data = tasks  # Using the existing tasks list
        Task.query.delete()
        
        for task_data in tasks_data:
            task = Task(
                description=task_data["description"],
                cost=task_data["cost"],
                difficulty=task_data["difficulty"]
            )
            db.session.add(task)

    with app.app_context():
        Transport.query.delete()
        
        for transport_data in transports:
            transport = Transport(
                type=transport_data["type"],
                cost=transport_data["cost"]
            )
            db.session.add(transport)

        db.session.commit()



def create_game(password, player_names):
    """Функция для создания новой игры и игроков"""
    if len(player_names) != 3:
        return jsonify({'error': 'Необходимо ввести имена для 3 игроков'}), 400

    # Сохраняем имена трёх игроков в отдельные поля
    new_game = Game(
        password=password,
        player1_name=player_names[0],
        player2_name=player_names[1],
        player3_name=player_names[2]
    )
    db.session.add(new_game)
    db.session.commit()

    # Создаем игроков с рандомным порядковым номером
    order_numbers = list(range(1, len(player_names) + 1))
    random.shuffle(order_numbers)

    for i, player_name in enumerate(player_names):
        status = 'runner' if order_numbers[i] == 1 else 'chaser'
        new_player = Player(name=player_name, order_number=order_numbers[i], status=status, game_id=new_game.id)
        db.session.add(new_player)

    db.session.commit()
    
    # # Наполнение базы данных
    # for task_data in tasks:
    #     task = Task(description=task_data['description'], cost=task_data['cost'], difficulty=task_data['difficulty'])
    #     db.session.add(task)
    
    # for transport_data in transports:
    #     transport = Transport(type=transport_data['type'], cost=transport_data['cost'])
    #     db.session.add(transport)
    # # Сохранение изменений в базе данных
    # db.session.commit()

    return jsonify({"message": "Game created successfully!"}), 201

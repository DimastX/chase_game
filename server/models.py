import random
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
tasks = [
    {"description": "Следующий транспорт, который возьмёшь должен содержать рандомную цифру", "cost": 500, "difficulty": "easy"},
    {"description": "Найди нелегальное объявление", "cost": 300, "difficulty": "easy"},
    {"description": "Доедь до ближайшего большого парка/сквера. Монетки за транспорт не списываются", "cost": 0, "difficulty": "easy"},
    {"description": "Найдите азиатский магазин/кафе", "cost": 300, "difficulty": "easy"},
    {"description": "Найдите магазин в котором продаются сувениры", "cost": 500, "difficulty": "easy"},
    {"description": "Найдите уличное графити", "cost": 250, "difficulty": "easy"},
    {"description": "Доедь до водоёма", "cost": 500, "difficulty": "easy"},
    {"description": "Накорми хотя бы 10 птиц", "cost": 750, "difficulty": "medium"},
    {"description": "Поедь на следующем транспорте, который придёт на ближайшую остановку как минимум 2 остановки", "cost": 500, "difficulty": "easy"},
    {"description": "Сообщи на каком транспорте и на какую остановку ты поедешь своим преследователям", "cost": 0, "difficulty": "medium"},
    {"description": "Найти книгу, название которой начинается на букву «М»", "cost": 500, "difficulty": "easy"},
    {"description": "Найти прохожего в костюме или рубашке", "cost": 200, "difficulty": "easy"},
    {"description": "Найти знак «кирпич»", "cost": 400, "difficulty": "easy"},
    {"description": "Пройди через подземный переход", "cost": 300, "difficulty": "easy"},
    {"description": "Найти припаркованный велосипед", "cost": 300, "difficulty": "easy"},
    {"description": "Найти велокурьера (Деливери Клаб / Яндекс еда)", "cost": 200, "difficulty": "easy"},
    {"description": "Найти рисунок мелками на асфальте или нарисовать", "cost": 1000, "difficulty": "medium"},
    {"description": "Успешно взять номер телефона у девушки", "cost": 1000, "difficulty": "medium"},
    {"description": "Сделать селфи на детской площадке", "cost": 300, "difficulty": "easy"},
    {"description": "Следующие 30 минут тебе нельзя пользоваться транспортом, где можно оплатить проезд «подорожником»", "cost": 200, "difficulty": "easy"},
    {"description": "Найти и сфотографировать граффити с изображением животного", "cost": 600, "difficulty": "medium"},
    {"description": "Посетить ближайший музей или галерею и сделать фото любого экспоната", "cost": 800, "difficulty": "medium"},
    {"description": "Найти и сфотографировать уличные часы", "cost": 400, "difficulty": "easy"},
    {"description": "Посетить ближайшую станцию метро и сделать фото с названием станции", "cost": 600, "difficulty": "medium"},
    {"description": "Найти и сфотографировать уличного музыканта", "cost": 700, "difficulty": "medium"},
    {"description": "Найти и сфотографировать скульптуру на здании", "cost": 500, "difficulty": "easy"},
    {"description": "Посетить ближайший книжный магазин и сфотографировать обложку книги на тему района, в котором вы находитесь", "cost": 1000, "difficulty": "medium"},
    {"description": "Найдите автомобиль с номерным знаком, содержащим две одинаковые буквы подряд", "cost": 600, "difficulty": "medium"},
    {"description": "Сфотографируйте три разных вида уличных фонарей в одном кадре", "cost": 800, "difficulty": "medium"},
    {"description": "Найдите и сфотографируйте кота", "cost": 1000, "difficulty": "hard"},
    {"description": "Найдите уличную вывеску с орфографической ошибкой", "cost": 900, "difficulty": "medium"},
    {"description": "Найдите и сфотографируйте три разных вида деревьев в одном парке или сквере", "cost": 800, "difficulty": "medium"},
    {"description": "До конца твоего забега ты не можешь использовать телефон для навигации", "cost": 1500, "difficulty": "hard"},
    {"description": "Следующая остановка общественного транспорта должна содержать две рандомные буквы", "cost": 750, "difficulty": "medium"},
    {"description": "Выберете ближайший перекрёсток со светофором, предскажите сколько людей перейдёт на следующий зелёный", "cost": 1000, "difficulty": "hard"},
    {"description": "Предскажите сколько человек зайдёт в ближайший магазин за 2 минуты", "cost": 1500, "difficulty": "hard"},
    {"description": "Предскажите сколько машин пересечёт перекрёсток на следующий зелёный", "cost": 2000, "difficulty": "hard"},
    {"description": "Дойти до ближайшей улицы с брусчаткой", "cost": 1000, "difficulty": "hard"},
    {"description": "Найти дуб или берёзу и дотронуться", "cost": 1000, "difficulty": "hard"},
    {"description": "Найти площадку с турником и сделать 5 подходов", "cost": 1500, "difficulty": "hard"},
    {"description": "Найти памятник с протёртым носом и потереть", "cost": 2000, "difficulty": "hard"},
    {"description": "Стрельнуть 5 сигарет у разных людей", "cost": 1500, "difficulty": "hard"},
    {"description": "Зайти в любой дом неподалёку, подняться пешком до последнего этажа", "cost": 1500, "difficulty": "hard"},
    {"description": "Залезть на любое дерево (минимум на полметра)", "cost": 1000, "difficulty": "hard"},
    {"description": "Купить свисток и свистнуть в следующем транспорте", "cost": 1000, "difficulty": "hard"},
    {"description": "20 минут не пользоваться навигатором и спросить дорогу", "cost": 800, "difficulty": "medium"},
    {"description": "Купить только лаваш в шаверме", "cost": 1500, "difficulty": "hard"}
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
    points = db.Column(db.Integer, default=500)    # По умолчанию 500 очков
    current_task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))  # Ссылка на текущее задание

    # Другие атрибуты и отношения

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    difficulty = db.Column(db.String, nullable=False)  # 'easy', 'medium', 'hard'
    


def get_random_task_for_player():
    # Получаем все задания из базы данных
    tasks = Task.query.all()
    print(tasks)
    if tasks:
        # Выбираем случайное задание
        return random.choice(tasks)
    else:
        return None  # Возвращаем None, если нет заданий

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

    # # Сохранение изменений в базе данных
    # db.session.commit()

    return jsonify({"message": "Game created successfully!"}), 201

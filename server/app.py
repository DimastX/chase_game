import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from models import create_game, db, Game, Player, Task, get_random_task_for_player  # Импортируем db и Game из models.py
import random
import logging

app = Flask(__name__)
CORS(app)

# Настройка SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///games.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)  # Инициализируем db

# Создание базы данных
with app.app_context():
    db.create_all()

# Эндпоинты

@app.route('/api/game', methods=['GET'])
def welcome():
    return jsonify({"message": "Добро пожаловать в API игры!"})


@app.route('/create-game', methods=['POST'])
def create_game_route():
    data = request.get_json()
    password = data['password']
    player_names = data['playerNames']

    if len(player_names) != 3:
        return jsonify({'error': 'Необходимо ввести имена для 3 игроков'}), 400

    # Используем вашу функцию для создания игры и игроков
    create_game(password, player_names)

    return jsonify({'message': 'Игра успешно создана!'}), 201

@app.route('/api/runner_data', methods=['GET'])
def get_runner_data():
    print(request.args)  
    player_id = request.args.get('player_id')  # Получите player_id из параметров запроса
    print(player_id)
    logging.debug(f"Получен player_id: {player_id}")

    if player_id is None:
        return jsonify({'error': 'player_id не передан', 'error2': 'player_id не передан'}), 400  # Ошибка 400 если player_id не передан
    
    player = Player.query.get(player_id)
    
    if player is None:
        return jsonify({'error': 'Игрок не найден'}), 404
    
    
    print("Наименование задания", player.current_task_id)
    current_task = Task.query.get(player.current_task_id)
    print(current_task)
    return jsonify({
        'points': player.points,
        'refuseTime': player.refuse_time,
        'currentTask': {
            'id': current_task.id,
            'description': current_task.description,
        } if current_task else None
    })



@app.route('/api/complete_task', methods=['POST'])
def complete_task():
    data = request.get_json()
    task_id = data.get('task_id')

    # Ищем игрока по ID
    player = Player.query.get(data.get('player_id'))
    if not player:
        return jsonify({'error': 'Игрок не найден'}), 404

    # Ищем задание по ID
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Задание не найдено'}), 404

    # Начисляем очки игроку
    player.points += task.cost
    db.session.commit()

    # Удаляем задание из формы игрока
    player.current_task_id = None
    db.session.commit()

    return jsonify({
        'message': 'Задание выполнено!',
        'points': player.points,
        'task_cost': task.cost,
    }), 200

@app.route('/api/refuse_task', methods=['POST'])
def refuse_task():
    data = request.get_json()
    task_id = data.get('task_id')

    # Ищем игрока по ID
    player = Player.query.get(data.get('player_id'))
    if not player:
        return jsonify({'error': 'Игрок не найден'}), 404

    # Ищем задание по ID
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Задание не найдено'}), 404

    # Запускаем таймер на 10 минут
    player.refuse_time = datetime.datetime.now() + datetime.timedelta(minutes=task.refuse_time_minutes)
    db.session.commit()

    # Удаляем задание из формы игрока   
    player.current_task_id = None
    db.session.commit()

    return jsonify({
        'message': 'Вы отказались от задания.',
        'refuse_time': player.refuse_time,
    }), 200

@app.route('/api/get_new_task', methods=['POST'])
def get_new_task():
    print("new_task")
    data = request.get_json()
    player_id = data.get('player_id')
    # Ищем игрока по ID
    player = Player.query.get(player_id)
    print(player)
    if not player:
        return jsonify({'error': 'Игрок не найден'}), 404

    # Выбираем случайное задание из базы данных заданий
    task = get_random_task_for_player()
    print("task2",task)
    if task:
        # Присваиваем игроку новое задание
        player.current_task_id = task.id
        db.session.commit()
        print(player.current_task_id)
        return jsonify({
            'points': player.points,
            'currentTask': {
                'id': task.id,
                'description': task.description,
                'task_cost': task.cost,
            }
        }), 200
    else:
        return jsonify({'error': 'Нет доступных заданий'}), 404



@app.route('/games', methods=['GET'])
def get_games():
    games = Game.query.all()
    games_list = []

    for game in games:
        games_list.append({
            "id": game.id,
            "players": [game.player1_name, game.player2_name, game.player3_name],
            "status": "Нужно добавить логику статуса",  # Вы можете добавить логику для статуса игры
        })

    return jsonify(games_list)

@app.route('/join-game', methods=['POST'])
def join_game():
    try:
        data = request.get_json()
        game_id = data.get('gameNumber')
        player_name = data.get('playerName')
        password = data.get('password')

        if not game_id or not player_name or not password:
            return jsonify({'error': 'Все поля обязательны для заполнения'}), 400

        # Ищем игру по ID
        game = Game.query.filter_by(id=game_id).first()

        if not game:
            return jsonify({'error': 'Игра не найдена'}), 404

        # Проверка пароля игры
        if game.password != password:
            return jsonify({'error': 'Неверный пароль'}), 403

        # Ищем игрока по имени в этой игре
        player = Player.query.filter_by(game_id=game_id, name=player_name).first()
        if not player:
            return jsonify({'error': 'Игрок не найден в этой игре'}), 404

        # Возвращаем статус игрока (runner или chaser)
        return jsonify({
            'status': player.status,
            'gameNumber': game_id,
            'playerNumber': int(player.id),
            'points': player.points,
            'currentTask': player.current_task_id
        }), 200

    except Exception as e:
        # Логируем ошибку для отладки
        print(f"Ошибка при подключении к игре: {e}")
        return jsonify({'error': 'Произошла ошибка на сервере'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

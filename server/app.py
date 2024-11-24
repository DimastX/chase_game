import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
import socket
import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from models import create_game, db, Game, Player, Task, Transport,get_random_task_for_player  # Импортируем db и Game из models.py
import random
import logging

app = Flask(__name__)
CORS(app)

# Настройка SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///games.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)  # Инициализируем db

logging.basicConfig(filename='app.log', level=logging.INFO, encoding='utf-8')
logging.getLogger().setLevel(logging.INFO)

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
    player_id = request.args.get('player_id')  # Получите player_id из параметров запроса
    logging.debug(f"Получен player_id: {player_id}")

    if player_id is None:
        return jsonify({'error': 'player_id не передан', 'error2': 'player_id не передан'}), 400  # Ошибка 400 если player_id не передан
    
    player = Player.query.get(player_id)
    
    if player is None:
        return jsonify({'error': 'Игрок не найден'}), 404
    
    current_task = Task.query.get(player.current_task_id)
    return jsonify({
        'points': player.points,
        'refuseTime': player.refuse_time,
        'currentTask': {
            'id': current_task.id,
            'description': current_task.description,
            'task_cost': current_task.cost
        } if current_task else None
    })



@app.route('/api/complete_task', methods=['POST'])
def complete_task():
    data = request.get_json()
    task_id = data.get('task_id')

    # Ищем игрока по ID
    player = Player.query.get(data.get('player_id'))
    if not player:
        logging.error('Игрок не найден')
        return jsonify({'error': 'Игрок не найден'}), 404

    # Ищем задание по ID
    task = Task.query.get(task_id)
    if not task:
        logging.error('Задание не найдено')
        return jsonify({'error': 'Задание не найдено'}), 404

    # Начисляем очки игроку
    player.points += task.cost
    logging.info('Пользователь {} получил {} очков за задание {}'.format(player.name, task.cost, task.description))
    db.session.commit()

    # Удаляем задание из формы игрока
    player.current_task_id = None
    db.session.commit()

    return jsonify({
        'message': 'Задание выполнено!',
        'points': player.points,
        'task_cost': task.cost,
    }), 200

@app.route('/api/get_task_by_difficulty', methods=['POST'])
def get_task_by_difficulty():
  data = request.get_json()
  player_id = data.get('player_id')
  difficulty = data.get('difficulty')

  # Получаем задания из базы данных в зависимости от выбранной категории
  tasks = Task.query.filter_by(difficulty=difficulty).all()

  # Выбираем три случайных задания
  tasks = random.sample(tasks, 3)

  logging.info('Пользователь {} получил 3 задания на выбор с уровнем сложности {}'.format(player_id, difficulty))


  return jsonify([{'id': task.id, 'description': task.description, 'task_cost': task.cost} for task in tasks])

@app.route('/api/choose_task', methods=['POST'])
def choose_task():
  data = request.get_json()
  player_id = data.get('player_id')
  task_id = data.get('task_id')

  # Выбираем задание
  task = Task.query.get(task_id)

  # Присваиваем игроку новое задание
  player = Player.query.get(player_id)
  player.current_task_id = task.id
  db.session.commit()

  return jsonify({'points': player.points, 'currentTask': {'id': task.id, 'description': task.description, 'task_cost': task.cost}})

@app.route('/api/refuse_task', methods=['POST'])
def refuse_task():
    data = request.get_json()
    task_id = data.get('task_id')

    # Ищем игрока по ID
    player = Player.query.get(data.get('player_id'))
    if not player:
        logging.error('Игрок не найден при отказе от задания')
        return jsonify({'error': 'Игрок не найден'}), 404

    # Ищем задание по ID
    task = Task.query.get(task_id)
    if not task:
        logging.error('Задание не найдено при отказе от него')
        return jsonify({'error': 'Задание не найдено'}), 404

    # Запускаем таймер на 10 минут
    player.refuse_time = datetime.datetime.now() + datetime.timedelta(minutes=task.refuse_time_minutes)
    db.session.commit()

    # Удаляем задание из формы игрока   
    player.current_task_id = None
    logging.info('Пользователь {} отказался от задания {}'.format(player.name, task.description))
    db.session.commit()

    return jsonify({
        'message': 'Вы отказались от задания.',
        'refuse_time': player.refuse_time,
    }), 200

@app.route('/api/get_new_task', methods=['POST'])
def get_new_task():
    data = request.get_json()
    player_id = data.get('player_id')
    # Ищем игрока по ID
    player = Player.query.get(player_id)
    if not player:
        return jsonify({'error': 'Игрок не найден'}), 404

    # Выбираем случайное задание из базы данных заданий
    task = get_random_task_for_player()
    if task:
        # Присваиваем игроку новое задание
        player.current_task_id = task.id
        db.session.commit()
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

@app.route('/api/runner_transport', methods=['POST'])
def runner_transport():
    data = request.get_json()
    runner_id = data['runner_id']
    transport_id = data['transport_id']
    stops = data['stops']
    print('runner_id:', runner_id, 'transport_id:', transport_id, 'stops:', stops)
    runner = Player.query.get(runner_id)
    if runner:
        if runner.deduct_transport_cost(transport_id, stops):
            logging.info('Пользователь {} списал транспортный расход на {} очков за {} остановок'.format(runner.name, runner.deduct_transport_cost(transport_id, stops), stops))
            print('Транспортный расход успешно списан!')
            return jsonify({'message': 'Транспортный расход успешно списан!'}), 200
        else:
            logging.info('Пользователю {} не хватило очков для списания транспортного расхода на {} остановок'.format(runner.name, stops))
            print('Недостаточно очков!')
            return jsonify({'error': 'Недостаточно очков!'}), 400
    else:
        logging.error('Игрок не найден при списании транспорта')
        print('Игрок не найден!')
        return jsonify({'error': 'Игрок не найден!'}), 404
    
@app.route('/api/transports', methods=['GET'])
def get_transports():
    transports = Transport.query.all()
    return jsonify([{'id': t.id, 'type': t.type, 'cost': t.cost} for t in transports])


@app.route('/catch', methods=['POST'])
def catch():
    player_id = request.json['player_id']
    player = Player.query.get(player_id)
    game_id = player.game_id
    players = Player.query.filter_by(game_id=game_id).order_by(Player.order_number.asc()).all()
    statuses = [player.status for player in players]
    statuses = statuses[-1:] + statuses[:-1]  # сместить статусы на одну по кругу
    for i, player in enumerate(players):
        player.status = statuses[i]
    db.session.commit()
    return jsonify({'message': 'Роли игроков изменены'})


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
        print(player.name)
        print(player.id)
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
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ssl_context = (
    os.path.join(BASE_DIR, 'ssl', 'server.crt'),
    os.path.join(BASE_DIR, 'ssl', 'server.key')
)
    app.run(host="0.0.0.0", port=5000, ssl_context=ssl_context, debug=True)
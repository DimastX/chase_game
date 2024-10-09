import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { joinGame } from '../services/api'; // Изменяем импорт на именованный

const JoinGamePage = () => {
    const [gameNumber, setGameNumber] = useState('');
    const [playerName, setPlayerName] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleJoinGame = async () => {
        try {
            const response = await joinGame(gameNumber, playerName, password); // Используем joinGame
            const { status } = response.data;

            // Сохраняем имя игрока и номер игры в localStorage
            localStorage.setItem('playerName', playerName);
            localStorage.setItem('gameNumber', gameNumber);

            if (status === 'runner') {
                navigate(`/runner/${gameNumber}`);
            } else if (status === 'chaser') {
                navigate(`/chaser/${gameNumber}`);
            }
        } catch (error) {
            console.error('Ошибка при подключении к игре:', error);
        }
    };

    return (
        <div>
            <h2>Присоединиться к игре</h2>
            <input
                type="text"
                placeholder="Номер игры"
                value={gameNumber}
                onChange={(e) => setGameNumber(e.target.value)}
                required
            />
            <input
                type="text"
                placeholder="Ваше имя"
                value={playerName}
                onChange={(e) => setPlayerName(e.target.value)}
                required
            />
            <input
                type="password"
                placeholder="Пароль"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
            />
            <button onClick={handleJoinGame}>Присоединиться</button>
        </div>
    );
};

export default JoinGamePage;

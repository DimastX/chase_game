import axios from 'axios';

const API_URL = 'http://localhost:5000';


export const getWelcomeMessage = async () => {
    const response = await fetch(`${API_URL}/game`);
    return response.json();
};

// src/services/api.js
export const createGame = async (gameData) => {
    const response = await fetch('http://localhost:5000/create-game', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(gameData),
    });

    if (!response.ok) {
        throw new Error('Ошибка при создании игры');
    }

    return await response.json();
};

export const getGames = async () => {
    const response = await fetch(`${API_URL}/games`); // Проверить правильность пути
    if (!response.ok) {
        throw new Error('Ошибка при загрузке игр');
    }
    return response.json();
};

export const joinGame = async (gameNumber, playerName, password) => {
    try {
        const response = await axios.post(`${API_URL}/join-game`, {
            gameNumber,
            playerName,
            password,
        });
        return response;
    } catch (error) {
        // Обработка ошибок
        if (error.response) {
            // Сервер ответил с кодом состояния, отличным от 2xx
            console.error('Ошибка при подключении к игре:', error.response.data);
            throw new Error(`Ошибка: ${error.response.data.message || error.message}`);
        } else if (error.request) {
            // Запрос был сделан, но ответ не был получен
            console.error('Запрос был сделан, но ответ не был получен');
            throw new Error('Ошибка: сервер не ответил');
        } else {
            // Произошла ошибка при настройке запроса
            console.error('Ошибка:', error.message);
            throw new Error(`Ошибка: ${error.message}`);
        }
    }
};


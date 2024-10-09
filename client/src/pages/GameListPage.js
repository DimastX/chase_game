import React, { useEffect, useState } from 'react';
import { getGames } from '../services/api'; // Импортируем функцию для получения игр

const GameListPage = () => {
    const [games, setGames] = useState([]);
    const [loading, setLoading] = useState(true); // Состояние загрузки
    const [error, setError] = useState(''); // Состояние для ошибки

    useEffect(() => {
        fetchGames(); // Вызов функции для загрузки игр при рендере компонента
    }, []);

    const fetchGames = async () => {
        try {
            console.log('Загрузка игр...'); // Лог для отслеживания начала загрузки
            const data = await getGames(); // Получаем данные об играх
            console.log('Получены данные:', data); // Логируем полученные данные
            setGames(data); // Обновляем состояние списка игр
        } catch (error) {
            console.error('Ошибка при загрузке игр:', error); // Логируем ошибку
            setError('Не удалось загрузить список игр.'); // Устанавливаем сообщение об ошибке
        } finally {
            setLoading(false); // Завершаем загрузку
        }
    };

    if (loading) {
        return <div>Загрузка...</div>; // Отображаем индикатор загрузки
    }

    if (error) {
        return <div>{error}</div>; // Отображаем сообщение об ошибке, если есть
    }

    return (
        <div>
            <h2>Список игр:</h2>
            <ul style={{ listStyleType: 'none', padding: 0 }}>
                {games.length > 0 ? (
                    games.map(game => (
                        <li key={game.id} style={{ margin: '10px 0' }}>
                            {/* Логируем структуру игры для проверки */}
                            {console.log('Игра:', game)}
                            {`Игра ${game.id}: Игроки: ${game.players.join(', ')}, Статус: ${game.status || 'неизвестен'}`}
                        </li>
                    ))
                ) : (
                    <li>Нет игр для отображения.</li> // Если игр нет, отображаем это сообщение
                )}
            </ul>
        </div>
    );
};

export default GameListPage;

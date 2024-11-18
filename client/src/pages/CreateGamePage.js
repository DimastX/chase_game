import React, { useState } from 'react';
import { createGame } from '../services/api'; // Импортируем функцию создания игры

const CreateGamePage = () => {
    const [password, setPassword] = useState('');
    const [playerNames, setPlayerNames] = useState(['', '', '']);
    const [error, setError] = useState('');
    const [successMessage, setSuccessMessage] = useState('');

    const handleCreateGame = async () => {
        setError('');
        setSuccessMessage('');

        if (playerNames.some(name => name.trim() === '')) {
            setError('Все игроки должны иметь имя.');
            return;
        }

        const gameData = {
            password,
            playerNames,
        };

        console.log('Отправка данных:', gameData); // Логируем данные для отладки

        try {
            const result = await createGame(gameData);
            console.log('Результат создания игры:', result);
            setSuccessMessage('Игра успешно создана!');
        } catch (error) {
            console.error('Ошибка при создании игры:', error);
            setError(`Ошибка при создании игры: ${error.message}`);
        }
    };

    const handlePlayerNameChange = (index, value) => {
        const updatedNames = [...playerNames];
        updatedNames[index] = value;
        setPlayerNames(updatedNames);
    };

    return (
        <div>
            <h2>Создать новую игру</h2>

            {error && <div style={{ color: 'red' }}>{error}</div>}
            {successMessage && <div style={{ color: 'green' }}>{successMessage}</div>}

            <div>
                <div className="form-group">
                    <label>Пароль игры:<input type="password" className="form-control" value={password} onChange={e => setPassword(e.target.value)} /> </label>
                </div>
            </div>

            <div>
                <h4>Имена игроков:</h4>
                {playerNames.map((name, index) => (
                    <div className="form-group row" key={index}>
                        <label htmlFor={`playerName${index}`}>Игрок {index + 1}: </label>
                        <div className="col-sm-10">
                            <input 
                                className="form-control"
                                type="text"
                                id = {`playerName${index}`}
                                value={name} 
                                onChange={(e) => handlePlayerNameChange(index, e.target.value)} 
                            />
                        </div>
                    </div>
                ))}
            </div>

            <button className="btn btn-primary" onClick={handleCreateGame}>Создать игру</button>
        </div>
    );
};

export default CreateGamePage;

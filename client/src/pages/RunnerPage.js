import React, { useEffect, useState } from 'react';
import axios from 'axios';

const RunnerPage = () => {
    const [runnerData, setRunnerData] = useState({ points: 500, currentTask: null });
    const [message, setMessage] = useState('');
    const [taskId, setTaskId] = useState(null);

    const fetchRunnerData = async () => {
        try {
            const response = await axios.get('/api/runner_data'); // Получаем данные убегающего
            console.log('Runner data:', response.data); // Добавляем лог для проверки
            setRunnerData(response.data);
        } catch (error) {
            setMessage('Ошибка при получении данных!');
        }
    };
    

    const handleCompleteTask = async () => {
        try {
            await axios.post('/api/complete_task', { task_id: taskId });
            fetchRunnerData(); // Обновляем данные после выполнения задания
            setMessage('Задание выполнено!');
        } catch (error) {
            setMessage('Ошибка при выполнении задания!');
        }
    };

    const handleRefuseTask = async () => {
        try {
            await axios.post('/api/refuse_task', { task_id: taskId });
            fetchRunnerData(); // Обновляем данные после отказа от задания
            setMessage('Вы отказались от задания.');
        } catch (error) {
            setMessage('Ошибка при отказе от задания!');
        }
    };

    const handleGetNewTask = async () => {
        try {
            console.log('Player ID:', runnerData.id); // Проверяем, что player_id передается корректно
            const response = await axios.post('http://localhost:5000/api/get_new_task', { player_id: runnerData.id });
            setTaskId(response.data.task_id);
            fetchRunnerData(); // Обновляем данные после получения нового задания
            setMessage('Новое задание получено!');
        } catch (error) {
            console.error('Ошибка при получении нового задания:', error);
            setMessage('Ошибка при получении нового задания!');
        }
    };
    

    useEffect(() => {
        fetchRunnerData();
    }, []);

    return (
        <div>
            <h1>Интерфейс убегающего</h1>
            <p>Ваши баллы: {runnerData.points}</p>
            <p>Текущее задание: {runnerData.currentTask?.description || 'Нет задания'}</p>
            {runnerData.currentTask && (
                <>
                    <button onClick={handleCompleteTask}>Задание выполнено</button>
                    <button onClick={handleRefuseTask}>Отказаться от задания</button>
                </>
            )}
            {!runnerData.currentTask && (
                <button onClick={handleGetNewTask}>Получить новое задание</button>
            )}
            {message && <p>{message}</p>}
        </div>
    );
};

export default RunnerPage;

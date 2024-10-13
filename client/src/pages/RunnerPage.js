import React, { useEffect, useState } from 'react';
import axios from 'axios';
const API_URL = 'http://localhost:5000';


const RunnerPage = () => {
    const [runnerData, setRunnerData] = useState({ points: 500, currentTask: null, refuseTime: null });
    const [message, setMessage] = useState('');
    const [taskId, setTaskId] = useState(null);

    const fetchRunnerData = async () => {
        try {
            const gameNumber = localStorage.getItem('gameNumber');
            const response = await axios.get(`${API_URL}/api/runner_data?player_id=${localStorage.getItem('playerName')}&game_number=${gameNumber}`);
            console.log('Runner cite:', `${API_URL}/api/runner_data?player_id=${localStorage.getItem('playerName')}&game_number=${gameNumber}`);
            console.log('Runner data:', response.data);
            setRunnerData({
                points: response.data.points,
                currentTask: response.data.currentTask,
            });
            console.log('Runner data:', response.data);
        } catch (error) {
            setMessage('Ошибка при получении данных!');
        }
    };
    

    const handleCompleteTask = async () => {
        try {
          await axios.post(`${API_URL}/api/complete_task`, { task_id: runnerData.currentTask.id, player_id: localStorage.getItem('playerName') });
          fetchRunnerData(); // Обновляем данные игрока после выполнения задания
          setMessage('Задание выполнено!');
        } catch (error) {
          setMessage('Ошибка при выполнении задания!');
        }
      };
      
      const handleRefuseTask = async () => {
        try {
          await axios.post(`${API_URL}/api/refuse_task`, { task_id: runnerData.currentTask.id, player_id: localStorage.getItem('playerName') });
          const refuseTime = new Date().getTime() + 10 * 60 * 1000; // 10 минут в миллисекундах
          setRunnerData({ ...runnerData, refuseTime });
          fetchRunnerData(); // Обновляем данные игрока после отказа от задания
          setMessage('Вы отказались от задания.');
          setTimeout(() => {
            setRunnerData({ ...runnerData, refuseTime: null });
          }, 10 * 60 * 1000); // 10 минут в миллисекундах
        } catch (error) {
          setMessage('Ошибка при отказе от задания!');
        }
      };

    const handleGetNewTask = async () => {
        if (runnerData && runnerData.refuseTime && new Date().getTime() < runnerData.refuseTime) {
          setMessage('Вы не можете взять новое задание, пока не прошло 10 минут с момента отказа от выполнения задания.');
          return;
        }
        try {
          const playerId = localStorage.getItem('playerName');
          const response = await axios.post(`${API_URL}/api/get_new_task`, { player_id: playerId });
          console.log('Новое задание:', response.data);
          setRunnerData({
            points: response.data.points,
            currentTask: response.data.currentTask,
          });
        } catch (error) {
          console.error('Ошибка при получении нового задания:', error);
        }
      };
    

    useEffect(() => {
        fetchRunnerData();
    }, []);

    return (
        <div>
            <h1>Интерфейс убегающего</h1>
            <p>Ваши баллы: {runnerData.points}</p>
            {runnerData.currentTask && (
                <>
                    <p>Текущее задание: {runnerData.currentTask?.description}, {runnerData.currentTask?.task_cost} очков</p>
                    <button onClick={handleCompleteTask}>Задание выполнено</button>
                    <button onClick={handleRefuseTask}>Отказаться от задания</button>
                </>
            )}
        {runnerData ? (
        runnerData.currentTask ? null : (
            <button onClick={handleGetNewTask}>Получить новое задание</button>
        )
        ) : (
        <button onClick={handleGetNewTask}>Получить новое задание</button>
        )}
            {message && <p>{message}</p>}
        </div>
    );
};

export default RunnerPage;

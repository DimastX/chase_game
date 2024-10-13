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
                refuseTime: response.data.refuseTime,
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
          fetchRunnerData(); // Обновляем данные игрока после отказа от задания
          setMessage('Вы отказались от задания.');
        } catch (error) {
          setMessage('Ошибка при отказе от задания!');
        }
      };

    const handleGetNewTask = async () => {
        const timeDifference = getTimeDifference();
        if (timeDifference) {
            setMessage(timeDifference);
            return;
        }
        try {
          const playerId = localStorage.getItem('playerName');
          const response = await axios.post(`${API_URL}/api/get_new_task`, { player_id: playerId });
          console.log('Новое задание:', response.data);
          setRunnerData({
            points: response.data.points,
            currentTask: response.data.currentTask,
            refuseTime: response.data.refuseTime,
          });
        } catch (error) {
          console.error('Ошибка при получении нового задания:', error);
        }
      };
    

    useEffect(() => {
        fetchRunnerData();
    }, []);

    const getTimeDifference = () => {
        const currentTime = new Date().getTime() + (3 * 60 * 60 * 1000);
        const refuseTime = runnerData.refuseTime ? Date.parse(runnerData.refuseTime) : 0;
        const diff = refuseTime - currentTime;
        if (diff > 0) {
            const minutes = Math.floor(diff / 60000);
            const seconds = Math.floor((diff % 60000) / 1000);
            return <p>Вы не можете взять новое задание, пока не пройдет {`${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`} минут. До {runnerData.refuseTime}</p>;
        }
        return null;
    };

    return (
        
        <div>
            {console.log('refuseTime перед сообщением:', runnerData.refuseTime)}
            {console.log('new Date() перед сообщением:', new Date())}
            <h1>Интерфейс убегающего</h1>
            <p>Ваши баллы: {runnerData.points}</p>
            {getTimeDifference()}
            {console.log('refuseTime после сообщения:', runnerData.refuseTime)}
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

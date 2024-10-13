import React, { useEffect, useState } from 'react';
import axios from 'axios';
const API_URL = 'http://localhost:5000';

const fetchTransports = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/transports`);
      return response.data;
    } catch (error) {
      console.error(error);
    }
  };


const RunnerPage = () => {
    const [runnerData, setRunnerData] = useState({ points: null, currentTask: null, refuseTime: null });
    const [message, setMessage] = useState('');
    const [taskId, setTaskId] = useState(null);
    const [transportId, setTransportId] = useState(null);
    const [stops, setStops] = useState(0);
    const [transports, setTransports] = useState([]);


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

    const handleTransportCostDeduction = async (e) => {
        e.preventDefault();
        const timeDifference = getTimeDifference();
        if (timeDifference) {
            fetchRunnerData();
            return;
        }
        try {
          console.log('Запрос на списание транспортного расхода отправлен');
          const response = await axios.post(`${API_URL}/api/runner_transport`, {
            runner_id: localStorage.getItem('playerName'),
            transport_id: transportId,
            stops: stops,
          });
          console.log('Ответ от сервера:', response.data);
          setMessage('Транспортный расход успешно списан!');
          fetchRunnerData();
        } catch (error) {
          console.log('Ошибка при списании транспортного расхода:', error);
          setMessage('Ошибка списания транспорта!');
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

      const handleCatch = async () => {
        try {
          const response = await axios.post(`${API_URL}/catch`, {
            player_id: localStorage.getItem('playerName'),
          });
          console.log(response.data);
        } catch (error) {
          console.error(error);
        }
      };

    useEffect(() => {
        fetchRunnerData();
        fetchTransports().then((data) => setTransports(data));
    }, []);
    const getTimeDifference = () => {
        const currentTime = new Date().getTime() + (3 * 60 * 60 * 1000);
        const refuseTime = runnerData.refuseTime ? Date.parse(runnerData.refuseTime) : 0;
        const diff = refuseTime - currentTime;
        if (diff > 0) {
            const minutes = Math.floor(diff / 60000);
            const seconds = Math.floor((diff % 60000) / 1000);
            return <p>Вы не можете взять новое задание и поехать на транспорте, пока не пройдет {`${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`}. До {runnerData.refuseTime}</p>;
        }
        return null;
    };

    return (
        
        <div>
            <h1>Интерфейс убегающего</h1>
            <p>Ваши баллы: {runnerData.points}</p>
            {getTimeDifference()}
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
        <form>
                <label>Транспорт:</label>
                <select value={transportId} onChange={(e) => setTransportId(e.target.value)}>
                    {transports.map((transport) => (
                        <option key={transport.id} value={transport.id}>{transport.type}</option>
                    ))}
                </select>
                <br />
                <label>Количество остановок:</label>
                <input type="number" value={stops} onChange={(e) => setStops(e.target.value)} />
                <br />
                <button onClick={(e) => handleTransportCostDeduction(e)}>
                    Списать транспортный расход
                </button>
            </form>
            {message && <p>{message}</p>}
            <button onClick={handleCatch}>Меня поймали</button>
        </div>
    );
};

export default RunnerPage;

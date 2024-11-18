import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import HomePage from './pages/HomePage';
import CreateGamePage from './pages/CreateGamePage';
import GameListPage from './pages/GameListPage';
import JoinGamePage from './pages/JoinGamePage';  // Импортируем страницу для подключения к игре
import RunnerPage from './pages/RunnerPage';      // Импортируем страницу убегающего
import ChaserPage from './pages/ChaserPage';      // Импортируем страницу догоняющего

const App = () => {
    console.log('Запуск приложения...');
    return (
        <Router>
            <div style={{ padding: '20px', textAlign: 'center' }}>
                <h1>Добро пожаловать в игру!</h1>
                <nav>
                    <Link to="/" style={{ margin: '10px' }}>Главная</Link>
                    <Link to="/create-game" style={{ margin: '10px' }}>Создать игру</Link>
                    <Link to="/game-list" style={{ margin: '10px' }}>Список игр</Link>
                    <Link to="/join-game" style={{ margin: '10px' }}>Присоединиться к игре</Link> {/* Ссылка на страницу подключения */}
                </nav>
                <Routes>
                    <Route path="/" element={<HomePage />} />
                    <Route path="/create-game" element={<CreateGamePage />} />
                    <Route path="/game-list" element={<GameListPage />} />
                    <Route path="/join-game" element={<JoinGamePage />} />  {/* Новый маршрут */}
                    <Route path="/runner/:gameNumber" element={<RunnerPage />} /> {/* Маршрут для убегающего с параметром gameNumber */}
                    <Route path="/chaser/:gameNumber" element={<ChaserPage />} /> {/* Маршрут для догоняющего с параметром gameNumber */}
                </Routes>
            </div>
        </Router>
    );
};

export default App;

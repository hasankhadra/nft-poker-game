import React from "react";
import './App.css';

import {
    BrowserRouter,
    Route,
    Routes,
    Navigate
} from "react-router-dom";
import {SocketContext, socket} from './contexts/socket';

import Home  from './pages/home'
import Lobby from './pages/lobby';
import Register from './pages/register';
import Game from './pages/game';
import Scoreboard from './pages/scoreboard';

function App() {
    return (
        <BrowserRouter>
            <SocketContext.Provider value={socket}>
                <Routes>
                    <Route path="/" element={<Navigate to="/home"/>}/>
                    <Route path="/home" element={<Home/>}/>
                    <Route path="/scoreboard" element={<Scoreboard/>}/>
                    <Route path="/lobby" element={<Lobby />}/>
                    <Route path="/register" element={<Register />}/>
                    <Route path="/game/:id" element={<Game />}/>
                    <Route path="*" element={<div>Empty</div>} />
                </Routes>
            </SocketContext.Provider>
        </BrowserRouter>
    );
}

export default App;
import React from "react";
import './App.css';

import {
    BrowserRouter,
    Route,
    Routes,
    Navigate
} from "react-router-dom";
import { SocketContext, socket } from './contexts/socket';

import Home from './pages/home'
import Lobby from './pages/lobby';
import Register from './pages/registration/register';
import Game from './pages/game';
import Leaderboard from './pages/leaderboard';
import GameGuide from './pages/gameGuide.js'
import Layout from "./components/layout";

function App() {
    return (
        <BrowserRouter>
            <Layout>
                <SocketContext.Provider value={socket}>
                    <Routes>
                        <Route path="/" element={<Navigate to="/home" />} />
                        <Route path="/home" element={<Home />} />
                        <Route path="/leaderboard" element={<Leaderboard />} />
                        <Route path="/lobby" element={<Lobby />} />
                        <Route path="/register" element={<Register />} />
                        <Route path="/game-guide" element={<GameGuide />} />
                        <Route path="/game/:gameId" element={<Game />} />
                        <Route path="*" element={
                            <main style={{ padding: "1rem" }}>
                                <p>There's nothing here!</p>
                            </main>} />
                    </Routes>
                </SocketContext.Provider>
            </Layout>

        </BrowserRouter>
    );
}

export default App;
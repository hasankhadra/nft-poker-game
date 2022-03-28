import socketio from "socket.io-client";
import React from "react";

const SOCKET_URL = 'http://54.183.235.87';

const io = require('socket.io-client')(SOCKET_URL, {
    cors: {
        origin : "*"
    }
});

export const socket = io(SOCKET_URL)
export const SocketContext = React.createContext();

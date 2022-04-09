import socketIOClient from "socket.io-client";

import React from "react";

const SOCKET_URL = 'http://54.183.235.87';
const LOCAL_SOCKET_URL = "http://localhost:5000"

export const socket = socketIOClient(SOCKET_URL);
export const SocketContext = React.createContext();

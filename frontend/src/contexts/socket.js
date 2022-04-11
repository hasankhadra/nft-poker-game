import socketIOClient from "socket.io-client";

import React from "react";

const SOCKET_URL = 'https://api.cappedrange.gg';
const LOCAL_SOCKET_URL = "http://localhost:5000";

export const socket = socketIOClient(SOCKET_URL);
export const SocketContext = React.createContext();

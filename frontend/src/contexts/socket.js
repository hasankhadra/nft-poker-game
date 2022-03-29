import socketIOClient from "socket.io-client";

import React from "react";

const SOCKET_URL = 'http://54.183.235.87';

export const socket = socketIOClient(SOCKET_URL);
export const SocketContext = React.createContext();

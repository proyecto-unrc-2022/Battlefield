import React from 'react';
import io from 'socket.io-client';
        
const SOCKET_ADDR = 'http://localhost:5000';
        
export const socket = io(SOCKET_ADDR);
        
export const SocketContext = React.createContext();
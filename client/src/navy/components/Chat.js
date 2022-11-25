import React from 'react'
import { useState,useEffect, } from 'react'
import io from 'socket.io-client';
/* import css */
import './Chat.css'
const socket = io('http://localhost:5000');
const Chat = ({  user, game}) => {
    /* useContext */
    const [message, setMessage] = useState('');
    const [messages, setMessages] = useState([
        {
            "body": "Welcome to the chat!",
            "user": "Navy",
        }
    ]);
    const [joinedRoom, setJoinedRoom] = useState(false);
    
    useEffect(() => {
        
        const receivedMessage = (message) => {
            console.log(messages)
            setMessages([...messages, message])
        }
        if(!joinedRoom){
        const chat_room = {
            "room": game.id
        }
        socket.emit('join', chat_room)
        setJoinedRoom(true);

    };
        socket.on('message', receivedMessage);
        return () => {
            socket.off('message',receivedMessage)   
        }
    }, [messages]);

  return (
    <div className="chat">
       <div className="chat__header">
            <h3>Navy Chat</h3>
        </div>

        <form
            onSubmit={(e) => {
                e.preventDefault();
                const new_message = {
                    "room": game.id,
                    "body": message,
                    "user": user
                }
                socket.emit('message', new_message);
                setMessage('');
            }}
        >
            <input
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Type message here..."
                className='chat-input'
            />
        </form>

        <div className="chat-messages">
            {messages.map((message, i) => (
                <div key={i}>{
                    message.user}: {message.body} 
                    </div>
            ))}
        </div>
    </div>
    );
}

export default Chat;
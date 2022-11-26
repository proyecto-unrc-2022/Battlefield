import React from 'react'
import { useState,useEffect, } from 'react'
import io from 'socket.io-client';
/* import css */
import './Chat.css'
import './ActionCard.css'
import NavyTitle from './NavyTitle'
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

    const sendMessage = (event) => {
        event.preventDefault();
        if (message) {
            const chat_message = {
                "body": message,
                "user": user,
                "room": game.id
            }
            socket.emit('message', chat_message);
            setMessage('');
        }
    }

    const bodyMessageClass = (message) => {
        console.log(message)
        if(message.user === "Navy"){
            return "message-body-navy"
        }else if(message.user === user){
            return "message-body-me"
        }else{
            return "message-body-enemy"
        }
    }

  return (
    <div className='card action-card p-2' style={{height: "100%",width: '75%'}}>
        <div className='card-header text-center'>
           <NavyTitle text='Navy Chat' />
        </div>
        <div className='card-body scroll-control'>
            <div className='messages'>
                {messages.map((message, index) => (
                    <div key={index} className='message'>
                        
                        <div className='message-user'>
                            
                            {message.user === user ? 'Me' : message.user}:
                            
                            </div>

                            <div className={bodyMessageClass(message)}>
                                <span className="ml-1">
                                    {message.body}
                                </span>
                                </div>

                    </div>
                ))}
            </div>
           
        </div>
        <div className='justify-content-between message-form '>
                <input  
                    style={{width: '84%'}}
                    type='text'
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    placeholder='Write your message...'
                    onKeyPress={(e) => e.key === 'Enter' ? sendMessage(e) : null}
                />

                <button onClick={(e) => sendMessage(e)} 
                className="ml-1"
                >
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" 
                className="bi bi-send-fill" viewBox="0 0 16 16">
  <path d="M15.964.686a.5.5 0 0 0-.65-.65L.767 5.855H.766l-.452.18a.5.5 0 0 0-.082.887l.41.26.001.002 4.995 3.178 3.178 4.995.002.002.26.41a.5.5 0 0 0 .886-.083l6-15Zm-1.833 1.89L6.637 10.07l-.215-.338a.5.5 0 0 0-.154-.154l-.338-.215 7.494-7.494 1.178-.471-.47 1.178Z"/>


</svg>


                </button>
                </div>
    </div>
    );

        

}

export default Chat;
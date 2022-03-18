

import { useEffect, useState, useCallback, useContext } from "react";
import { getAddress } from '../utils/metamaskAuth';
import { SocketContext } from '../contexts/socket';
import './register.css';


function Register() {
    const socket = useContext(SocketContext);
    const [hasMetaMask, setHasMetaMask] = useState(false);
    const [username, setUsername] = useState('');
    const [usernameError, setUsernameError] = useState('');

    useEffect(() => {
        socket.on('register', registerListener);

        return () => {
            socket.off('register', registerListener);
        }
    }, [socket]);

    useEffect(() => {
        if (typeof window.ethereum !== "undefined") {
            setHasMetaMask(true);
        }
    });

    const registerListener = useCallback((registerResponse) => {
        if (registerResponse.response === 'OK') {
            alert("You've successfully registered!");
        }
        else {
            setUsernameError(registerResponse);
        }
    }, []);

    const onSubmit = useCallback(async (e) => {
        e.preventDefault();
        const address = await getAddress();
        console.log(username);
        if (username === "") {
            setUsernameError("Username can't be empty!");
            return;
        }
        const payload = {
            public_address: address,
            username: username
        }
        socket.emit("register", payload);
    }, []);

    return (
        <div className="App">
            {hasMetaMask ?
                <div class="container">
                    <form onSubmit={onSubmit}>
                        <label><b>Username</b></label>
                        <input
                            type="text"
                            placeholder="A unique username"
                            name="username"
                            value={username}
                            onChange={e => setUsername(e.target.value.trim())}
                        />
                        <span style={{ color: "red" }}>{usernameError}</span>
                        <hr/>
                        <button type="submit" class="registerbtn"> Register </button>
                    </form>
                </div>
                : "Please install MetaMask"}
        </div>
    );

}

export { Register };



import { useEffect, useState, useCallback, useContext } from "react";
import { useNavigate } from "react-router-dom";

import { getAddress } from '../../utils/metamaskAuth';
import { SocketContext } from '../../contexts/socket';

import './register.css';

import backgroundImg from '../../assets/backgrounds/background.png';
import Header from "../../components/header";
import Footer from "../../components/footer";


function Register() {
    const socket = useContext(SocketContext);
    const [hasMetaMask, setHasMetaMask] = useState(false);
    const [username, setUsername] = useState('');
    const [usernameError, setUsernameError] = useState('');
    const [registered, setRegistered] = useState(false);

    let navigate = useNavigate();

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
        console.log()
        if (registerResponse.response === 'OK') {
            alert("You've successfully registered!");
            setRegistered(true);
        }
        else {
            setUsernameError(registerResponse.response);
        }
    }, []);

    const onSubmit = useCallback(async (e) => {
        e.preventDefault();
        const address = await getAddress();
        if (username === "") {
            setUsernameError("Username can't be empty!");
            return;
        }
        setUsernameError('')
        const payload = {
            public_address: address,
            username: username
        }
        socket.emit("register", payload);
    }, [username, usernameError]);

    return (
        <div style={{height:'100vh', backgroundColor: "#25262A", display: "flex", flexDirection: "column"}}>
            <Header />
            <div style={{
                backgroundImage: `url(${backgroundImg})`,
                height: "80%",
                marginLeft: "10%",
                // marginBottom: "10%",
                backgroundColor: "#25262A",
                // backgroundColor: "white",
                backgroundSize: 'cover',
                backgroundRepeat: 'no-repeat',
                width: "80%",
                display: "flex",
                flexDirection: "row"
            }}>

                {hasMetaMask ?
                    <div class="container">
                        <form onSubmit={onSubmit}>
                            <label><b>Nickname</b></label>
                            <input
                                type="text"
                                placeholder="A unique nickname"
                                name="username"
                                value={username}
                                onChange={e => setUsername(e.target.value.trim())}
                            />
                            <span style={{ color: "red" }}>{usernameError}</span>
                            <hr />
                            <button type="submit" className="registerbtn"> Register </button>
                        </form>
                    </div>
                    : "Please install MetaMask"}
            </div>
            <Footer />
        </div>
    );

}

export default Register;

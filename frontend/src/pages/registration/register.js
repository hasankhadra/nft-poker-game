

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
    const [hasMetaMask, setHasMetaMask] = useState(typeof window.ethereum !== "undefined");
    const [username, setUsername] = useState('');
    const [usernameError, setUsernameError] = useState('');
    const [registeredMetamask, setRegisteredMetamask] = useState(false);
    const [registered, setRegistered] = useState(false);

    let navigate = useNavigate();

    useEffect(() => {
        socket.on('register', registerListener);

        return () => {
            socket.off('register', registerListener);
        }
    }, [socket]);

    useEffect(async () => {
        if (registeredMetamask) {
            await window.ethereum.enable().then(() => { }).catch(() => { window.alert("You need to allow MetaMask."); setRegisteredMetamask(false); })
        }
        if (typeof window.ethereum !== "undefined") {
            setHasMetaMask(true);
        }
    });

    const registerListener = useCallback((registerResponse) => {
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

        // // TESTING FRONTEND
        // setRegistered(true);
        // return;
        // // TESTING FRONTEND

        const payload = {
            public_address: address,
            username: username
        }
        socket.emit("register", payload);
    }, [username, usernameError]);

    const handleClick = async (e) => {
        e.preventDefault();
        await window.ethereum.enable().then(() => { setRegisteredMetamask(true) }).catch(() => { window.alert("You need to allow MetaMask.") })
    };

    return (
        <div style={{ height: '100vh', backgroundColor: "#25262A", display: "flex", flexDirection: "column" }}>
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
                {!hasMetaMask ? alert("Please install MetaMask!") :
                    registered ?
                        <div className="mid-page"> <h5>Congratulation!</h5> <h6 style={{ color: "#FFC728" }}>Here's your Game NFT</h6>
                            <p className="body-large">
                                You have successfully registered to Capped Range Poker Game! You can log into your account anytime to 
                                see leaderboard and upcoming round. The first round will take place on <span style={{ color: "#FFC728" }}>July 12th, 2022</span>.
                            </p>
                            <button onClick={() => navigate('/lobby')}>Go to Lobby</button>
                        </div>

                        : registeredMetamask ?
                            <div className="mid-page">
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
                            :
                            <div className="mid-page">
                                <h5 style={{color: "white"}}>Game registeration</h5>
                                <button onClick={handleClick}>Register with Metamask</button>
                            </div>
                }
            </div>
            <Footer />
        </div>
    );

}

export default Register;



import { useEffect, useState, useCallback, useContext } from "react";
import { useNavigate } from "react-router-dom";

import { getAddress } from '../../utils/metamaskAuth';
import { SocketContext } from '../../contexts/socket';

import './registerMetamask.css';

import backgroundImg from '../../assets/backgrounds/background.png';
import Header from "../../components/header";
import Footer from "../../components/footer";


function RegisterMetamask() {
    const socket = useContext(SocketContext);
    const [hasMetaMask, setHasMetaMask] = useState(false);
    let navigate = useNavigate();

    useEffect(async () => {
        if (typeof window.ethereum !== "undefined") {
            setHasMetaMask(true);
        }
    });

    const handleClick = async (e) => {
        e.preventDefault();
        await window.ethereum.enable().then(() => {navigate("/register")}).catch(() => {window.alert("You need to allow MetaMask.")})
    };
    
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
                <div>
                    Game registeration
                    <button onClick={handleClick}>Register with Metamask</button>
                </div>
            </div>
            <Footer />
        </div>
    );

}

export default RegisterMetamask;

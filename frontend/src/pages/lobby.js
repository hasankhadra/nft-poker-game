import io from 'socket.io-client';
import { useEffect, useState } from "react";
import {getAddress} from '../utils/metamaskAuth';


function Lobby(){

    const [socket, setSocket] = useState(null);
    const [hasMetaMask, setHasMetaMask] = useState(false);

    useEffect(() => {

        return () => {
        }
    }, [socket]);

    useEffect(() => {
        if (typeof window.ethereum !== "undefined") {
            setHasMetaMask(true);
        }
    });

    return (
        <div>
            players table
            <hr/>
            <hr/>
            A list of nfts.
        </div>
    )
}

export {Lobby};

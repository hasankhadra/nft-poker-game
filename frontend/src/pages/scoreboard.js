
import { useEffect, useState, useCallback, useContext } from "react";

import { getAddress } from '../utils/metamaskAuth';
import { SocketContext } from '../contexts/socket';
import {PlayersTable} from '../components/playersTable'

function Scoreboard() {

    const socket = useContext(SocketContext);
    const [hasMetaMask, setHasMetaMask] = useState(false);
    const [players, setPlayers] = useState([]);

    // useEffect(() => {
    //     socket.on('get_players', getPlayersListener);

    //     return () => {
    //         socket.off('get_players', getPlayersListener);
    //     }
    // }, [socket]);

    useEffect(() => {
        if (typeof window.ethereum !== "undefined") {
            setHasMetaMask(true);
        }
    });


    useEffect(() => {
        // socket.emit("get_players");
        const newPlayers = [
            {id: 1, username: "hasan", bounty: 10},
            {id: 2, username: "hash", bounty: 100},
            {id: 3, username: "igor", bounty: 35}
        ]
        setPlayers(newPlayers);
    }, []);

    const comparePlayers = (player1, player2) => {
        return 0;
    }

    const getPlayersListener = useCallback(async (response) => {
        response.players.sort(comparePlayers);
        setPlayers(response.players)
    }, [players]);

    return (
        <div>
            Scoreboard
            <PlayersTable players={players}/>
        </div>
    )
}

export default Scoreboard ;

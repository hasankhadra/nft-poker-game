
import React from "react";
import { useEffect, useState, useCallback, useContext } from "react";
import { useParams } from "react-router-dom";
import { SocketContext } from '../contexts/socket';
import { Helmet } from "react-helmet";

import PlayerCard from '../components/playerCard';
import Table from '../components/table';


function Game() {
    let { gameId } = useParams();
    const socket = useContext(SocketContext);

    const [winner, setWinner] = useState(-1);
    const [myHand, setMyHand] = useState([])

    useEffect(() => {
        socket.on('play_game', receiveGameResults);

        return () => {
            socket.off('play_game', receiveGameResults);
        }
    }, [socket]);

    const receiveGameResults = useCallback(async (response) => {

    }, [winner,])

    useEffect(() => {
        const payload = {

        }
        socket.emit("join_room", payload);
    }, []);

    const opponent = {
        username: "james_perterss"
    }

    const username = "makelew_sasa342";

    return (
        <React.Fragment>
            <Helmet>
                <title>Game</title>
            </Helmet>
            <div className="container">
                <PlayerCard type="OPPONENT" name={opponent.username} />
                <Table topCards={[]} />
                <PlayerCard type="YOU" name={username} />
            </div>
        </React.Fragment>
    )
}

export default Game;

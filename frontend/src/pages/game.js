
import React from "react";
import './game.css'
import { useEffect, useState, useCallback, useContext, useMemo } from "react";
import { useParams } from "react-router-dom";
import { SocketContext } from '../contexts/socket';
import { Helmet } from "react-helmet";

import PlayerCard from '../components/playerCard';
import PokerTable from '../components/pokerTable';
import CountdownTimer from '../components/countdownTimer'

import player1Image from '../assets/nfts/nft1.png'
import player2Image from '../assets/nfts/nft2.png'

import backgroundImg from '../assets/backgrounds/background.png';

import { getAddress } from '../utils/metamaskAuth';
import { VoidSigner } from "ethers";

function Game() {
    // This is to be used in the join game event.
    let { gameId } = useParams();

    const socket = useContext(SocketContext);

    // Update when the game is over.
    const [winner, setWinner] = useState(-1);

    // Update this to a list of empty strings (the important thing is to have 2 as the length of the hand, 5 as the flops length)
    // This will make the cards face-down.
    const [myHand, setMyHand] = useState(["", ""]);
    const [opponentHand, setOpponentHand] = useState(["", ""]);

    const [opponentHandName, setOpponentHandName] = useState("");
    const [myHandName, setMyHandName] = useState("");

    const [flops, setFlops] = useState(["", "", "", "", ""]);
    
    const [playerId, setPlayerId] = useState(0);
    const [opponentId, setOpponentId] = useState(0);
    
    // Change initial values to empty and get them from the calls.
    const [opponentUsername, setOpponentUsername] = useState('')
    const [myUsername, setMyUsername] = useState('')

    // Update them as soon as the time for the round to finish is received.
    const [minutes, setMinutes] = useState(5);
    const [seconds, setSeconds] = useState(0);

    useEffect(() => {
        socket.on('play_game', receiveGameResults);
        socket.on('draw_combo', drawComboListener);
        socket.on('join_room', joinRoomListener)
        return () => {
            socket.off('play_game', receiveGameResults);
            socket.off('draw_combo', drawComboListener);
            socket.off('join_room', joinRoomListener);
        }
    }, [socket]);


    const joinRoomListener = (response) => {
        console.log(response.player_id, " ", response.username, " ", response.opponent_id, " ", response.opponent_username);
        setPlayerId(response.player_id);
        setMyUsername(response.username);

        setOpponentId(response.opponent_id);
        setOpponentUsername(response.opponent_username);
    }

    const drawComboListener = (response) => {
        setMyHand(response.player_combo);
    }

    const receiveGameResults = useCallback((response) => {
        let results = response.results
        console.log("Game Results " + playerId)
        if(results[playerId].winner)
            setWinner(1);
        else setWinner(2);

        setFlops(results.flops);
        setOpponentHand(results[opponentId].best_hand);
        setOpponentHandName(results[opponentId].best_hand_name);

        setMyHandName(results[playerId].best_hand_name);

    }, [playerId, opponentId, winner])

    // This should listen to the event where the game starts and ends etc.
    useEffect(async () => {
        const payload = {
            public_address: await getAddress(),
            game_id: gameId,
            room: "room_" + gameId
        }
        socket.emit("join_room", payload);
        // socket.emit("draw_combo", {public_address: await getAddress(), game_id: gameId})
    }, []);

    // This should just emit the draw hand event.
    const handleDrawHand = async (e) => {
        e.preventDefault();
        console.log("Draw hand " + playerId);
        const payload = {
            public_address: await getAddress(),
            game_id: gameId
        }

        socket.emit("draw_combo", payload);
    }

    // This should route to the next game.
    // This is done by emitting the event getNextGame.
    const handleNextGame = () => {

    }

    return (
        <div style={{ backgroundImage: `url(${backgroundImg})`, backgroundColor: "#1A1A1C" }}>
            <Helmet>
                <title>Game</title>
            </Helmet>
            <CountdownTimer seconds={seconds} minutes={minutes} />
            <div className="game-container">
                <PlayerCard type="OPPONENT" name={opponentUsername} profileImage={player1Image} />
                <PokerTable opponentHand={opponentHand} myHand={myHand} flops={flops} />
                <PlayerCard type="YOU" name={myUsername} profileImage={player2Image} />
            </div>
            <div className="buttons">
                <button className="draw-hand" onClick={handleDrawHand}>
                    Draw Hand
                </button>
                {winner === -1 ?
                    <button className="next-game" disabled onClick={handleNextGame}>
                        Next Game &#8594;
                    </button> :
                    <button className="next-game" onClick={handleNextGame}>
                        Next Game &#8594;
                    </button>
                }
            </div>
        </div>
    )
}

export default Game;

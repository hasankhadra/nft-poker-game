
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

function Game() {
    // This is to be used in the join game event.
    let { gameId } = useParams();

    const socket = useContext(SocketContext);

    // Update when the game is over.
    const [winner, setWinner] = useState(-1);

    // Update this to a list of empty strings (the important thing is to have 2 as the length of the hand, 5 as the flops length)
    // This will make the cards face-down.
    const [myHand, setMyHand] = useState(["4C", "1"]);
    const [opponentHand, setOpponentHand] = useState(["2D", "KS"]);
    const [flops, setFlops] = useState(["2D", "KS", "TC", '8S', '6H']);

    // Change initial values to empty and get them from the calls.
    const [opponentUsername, setOpponentUsername] = useState('james_perterss')
    const [myUsername, setMyUsername] = useState('makelew_sasa342')

    // Update them as soon as the time for the round to finish is received.
    const [minutes, setMinutes] = useState(5);
    const [seconds, setSeconds] = useState(0);

    useEffect(() => {
        socket.on('play_game', receiveGameResults);

        return () => {
            socket.off('play_game', receiveGameResults);
        }
    }, [socket]);

    const receiveGameResults = useCallback(async (response) => {

    }, [winner,])

    // This should listen to the event where the game starts and ends etc.
    useEffect(() => {
        const payload = {

        }
        socket.emit("join_room", payload);
    }, []);

    const drawHandListener = (data) => {
        console.log(data)
        // update my hand.
    }

    // When both player drew their hands.
    const gameOverListener = (data) => {
        console.log(data)
        // update winner.
    }

    // This should just emit the draw hand event.
    const handleDrawHand = () => {

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


import React from "react";
import './game.css'
import { useEffect, useState, useCallback, useContext, useMemo } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { SocketContext } from '../contexts/socket';

import PlayerCard from '../components/playerCard';
import PokerTable from '../components/pokerTable';
import CountdownTimer from '../components/countdownTimer'

import player1Image from '../assets/nfts/nft1.png'
import player2Image from '../assets/nfts/nft2.png'

import backgroundImg from '../assets/backgrounds/background.png';

import { getAddress } from '../utils/metamaskAuth';
import { VoidSigner } from "ethers";
import { Helmet, HelmetProvider } from 'react-helmet-async';

function Game() {
    // This is to be used in the join game event.
    let { gameId } = useParams();

    const socket = useContext(SocketContext);
    let navigate = useNavigate();

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

    const [nextRoom, setNextRoom] = useState('');

    useEffect(() => {
        socket.on('play_game', receiveGameResults);
        socket.on('draw_combo', drawComboListener);
        socket.on('join_room', joinRoomListener);
        socket.on("get_next_room", getNextRoomListener);
        return () => {
            socket.off('play_game', receiveGameResults);
            socket.off('draw_combo', drawComboListener);
            socket.off('join_room', joinRoomListener);
            socket.off("get_next_room", getNextRoomListener);
        }
    }, [socket]);


    const joinRoomListener = (response) => {
        if(myUsername !== "")
            return;
        setPlayerId(response.player_id);
        setMyUsername(response.username);

        setOpponentId(response.opponent_id);
        setOpponentUsername(response.opponent_username);
    }

    const drawComboListener = (response) => {
        setMyHand(response.player_combo);
    }

    const receiveGameResults = (response) => {
        let results = response.results
        let myId = results.player_id
        let otherId = results.opponent_id

        if (results[myId].winner){
            alert("YOU WON THIS GAME!")
            setWinner(1);
        }
        else {
            alert("YOU LOST THIS GAME!")
            setWinner(2);
        }
        setFlops(results.flops);
        setOpponentHand(results.opponent_combo);
        setOpponentHandName(results[otherId].best_hand_name);
        setMyHandName(results[myId].best_hand_name);
    }

    // This should listen to the event where the game starts and ends etc.
    useEffect(async () => {
        const payload = {
            public_address: await getAddress(),
            game_id: gameId,
            room: "room_" + gameId
        }
        socket.emit("join_room", payload);

        socket.emit("get_next_room", 
        {  
            public_address: await getAddress(),
            game_id: gameId
        });
    }, []);

    // This should just emit the draw hand event.
    const handleDrawHand = async (e) => {
        e.preventDefault();
        const payload = {
            public_address: await getAddress(),
            game_id: gameId,
            player_id: playerId
        }
        socket.emit("draw_combo", payload);
    }

    // This should route to the next game.
    // This is done by emitting the event getNextGame.
    const handleNextGame = async (e) => {
        e.preventDefault();
        navigate(`/game/${nextRoom}`);
    }

    const getNextRoomListener = (response) => {
        setNextRoom(response.room);
    }

    return (
        <HelmetProvider>

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
                    {(winner === -1 || nextRoom === "NO NEXT GAME") ?
                        (<button className="next-game" disabled onClick={handleNextGame}>
                            Next Game &#8594;
                        </button>) :
                        (<button className="next-game" onClick={handleNextGame}>
                            Next Game &#8594;
                        </button>)
                    }
                </div>
            </div>

        </HelmetProvider>
    )
}

export default Game;

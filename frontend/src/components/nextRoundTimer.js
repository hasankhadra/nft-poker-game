
import React, { useEffect, useState } from "react";

import './nextRoundTimer.css'
import pokerCardsImg from '../assets/profileInfoIcons/pokerCards.png'

import SingleTimeItem from "./singleTimeItem";


function NextRoundTimer(props) {
    const [days, setDays] = useState(props.days ?? 0);
    const [hours, setHours] = useState(props.hours ?? 0);
    const [minutes, setMinutes] = useState(props.minutes ?? 0);
    const [seconds, setSeconds] = useState(props.seconds ?? 0);

    useEffect(() => {
        let myInterval = setInterval(() => {
            if (seconds <= 0) {
                if (minutes <= 0) {
                    if (hours <= 0) {
                        if (days <= 0) {

                        }
                        else {
                            setDays(days - 1)
                            setHours(23);
                            setMinutes(59);
                            setSeconds(59);
                        }
                    }
                    else {
                        setHours(hours - 1);
                        setMinutes(59);
                        setSeconds(59);
                    }
                } else {
                    setMinutes(minutes - 1);
                    setSeconds(59);
                }
            }
            else {
                setSeconds(seconds - 1);
            }
        }, 1000)
        return () => {
            clearInterval(myInterval);
        };
    }, [seconds, minutes, hours, days]);

    useEffect(() => {
        setSeconds(props.seconds)
        setMinutes(props.minutes)
        setHours(props.hours)
        setDays(props.days)
    }, [props.seconds, props.minutes, props.hours, props.days])

    const getOrder = (number) => {
        if (number % 100 >= 11 && number % 100 <= 13) {
            return 'th'
        }
        if (number % 10 === 1) {
            return 'st'
        }
        if (number % 10 === 2) {
            return 'nd'
        }
        if (number % 10 === 3) {
            return 'rd'
        }
        return 'th'
    }

    if (!(seconds || minutes || hours || days) && props.isActive) {
        return (
            <div className="next-round-timer">
                <div className="next-round-header">
                    <img src={pokerCardsImg} />
                    <p>
                        <span className="yellow bigger">{props.roundNum}{getOrder(props.roundNum)}</span> is already taking place. <span className="yellow">Join</span> the game now!
                    </p>
                </div>
                <p>
                    Before you start a round, you need to Stake some of your NFTs or all of them to be able to play.
                    Please read the Game Guide for more information on how the game goes.
                </p>
                <div className="stake-start-buttons">
                    <button className="stake-all-button" onClick={props.handleStakeAllNFTs}>
                        Stake All NFT's
                    </button>
                    <button className="start-button" onClick={props.handleStartGame}>
                        Start game
                    </button>
                </div>
            </div>
        )
    }
    else if (!(seconds || minutes || hours || days)) {
        return (
            <div className="next-game-timer">
                <div className="next-game-header">
                    <img src={pokerCardsImg} />
                    <span className="yellow">{props.roundNum}{getOrder(props.roundNum)}</span> is already taking place. Unfortunately, all your NFT's lost the game.
                </div>
                <p>
                    Before you start a round, you need to Stake some of your NFTs or all of them to be able to play.
                    Please read the Game Guide for more information on how the game goes.
                </p>
            </div>
        )
    }
    return (
        <div className="next-game-timer">
            <div className="next-game-header">
                <img src={pokerCardsImg} />
                <span className="yellow">{props.roundNum}{getOrder(props.roundNum)}</span> will take place on <span className="yellow">{props.startTimeString}</span>
                <SingleTimeItem type="Days" number={days} />
                <SingleTimeItem type="Hours" number={hours} />
                <SingleTimeItem type="Mins" number={minutes} />
                <SingleTimeItem type="Secs" number={seconds} />
            </div>
        </div>
    )
}

export default NextRoundTimer;

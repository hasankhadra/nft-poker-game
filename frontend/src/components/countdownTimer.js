import React, { useEffect, useState } from "react";

import './countdownTimer.css'

const SingleTimeItem = (props) => {
    return (
        <div className="single-count-item">
            <div className="upper-number-box">
                {props.number}
            </div>
            <div className="lower-type-box">
                {props.type}
            </div>
        </div>
    )
}

function CountdownTimer(props) {
    const [minutes, setMinutes] = useState(props.minutes);
    const [seconds, setSeconds] = useState(props.seconds);
    useEffect(() => {
        let myInterval = setInterval(() => {
            if (seconds > 0) {
                setSeconds(seconds - 1);
            }
            if (seconds === 0) {
                if (minutes === 0) {
                    // clearInterval(myInterval)
                } else {
                    setMinutes(minutes - 1);
                    setSeconds(59);
                }
            }
        }, 1000)
        return () => {
            clearInterval(myInterval);
        };
    }, [seconds, minutes]);

    useEffect(() => {
        setSeconds(props.seconds)
        setMinutes(props.minutes)
    }, [props.seconds, props.minutes])

    return (
        <div className="timer-wrapper">
            <span className="white">Remainging Time</span>
            <div className="time-boxes">
                <SingleTimeItem type="Mins" number={minutes} />
                <span className="yellow">:</span>
                <SingleTimeItem type="Secs" number={seconds} />
            </div>
        </div>
    )
}

export default CountdownTimer;


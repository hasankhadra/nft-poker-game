
import React from 'react';

import './header.css'

import logoImg from '../assets/icons/logo.png';
import instagramLogo from '../assets/icons/instagram.png';
import facebookLogo from '../assets/icons/facebook.png';
import twitterLogo from '../assets/icons/twitter.png';
import linkedinLogo from '../assets/icons/linkedin.png';

import { Link, useNavigate, useLocation } from "react-router-dom";

const showLoginRegisterList = ["/home", "/leaderboard"];

function Header() {
    let location = useLocation();
    let navigate = useNavigate();

    const showLoginRegister = () => {
        return showLoginRegisterList.includes(location.pathname);
    }

    return (
        <header className="header">
            <Link to="/home"><img className='logo' src={logoImg} alt="logo" /></Link>

            <div className='navigate'>
                <Link className={location.pathname === '/leaderboard' ? "body-large focused" : "body-large"} to="/leaderboard">Leaderboard</Link>
                <Link className={location.pathname === '/game-guide' ? "body-large focused" : "body-large"} to="/game-guide">Game Guide</Link>
            </div>

            <div className='header-right'>

                {showLoginRegister() &&
                    <React.Fragment>
                        <button className="body-large header-loginbtn" onClick={() => { }}>Login</button>
                        <button className="body-large header-registerbtn" onClick={() => navigate('/register')}>Register</button>
                    </React.Fragment>
                }
                
                <div className='other-links'>

                    <a href='#'><img src={instagramLogo} alt="instagramLogo" /></a>
                    <a href='#'><img src={facebookLogo} alt="facebookLogo" /></a>
                    <a href='#'><img src={twitterLogo} alt="twitterLogo" /></a>
                    <a href='#'><img src={linkedinLogo} alt="linkedinLogo" /></a>
                </div>
            </div>
        </header>
    );
}

export default Header;


import './header.css'

import logoImg from '../assets/logo.png';
import instagramLogo from '../assets/instagram.png';
import facebookLogo from '../assets/facebook.png';
import twitterLogo from '../assets/twitter.png';
import linkedinLogo from '../assets/linkedin.png';

import { Link, useNavigate} from "react-router-dom";
function Header(props){

    let navigate = useNavigate();

    return (
        <div className="header">
            <img className='logo' src={logoImg} alt="logo"/>
            { props.showLoginRegister ? "a" : ""}

            <div className='navigate'>
                <Link className={props.pageName === 'leaderboard' ? "body-large focused" : "body-large"} to="/leaderboard">Leaderboard</Link>
                <Link className={props.pageName === 'game-guide' ? "body-large focused" : "body-large"} to="/game-guide">Game Guide</Link>
            </div>

            <button className="body-large loginbtn" onClick={() => {}}>Login</button>
            <button className="body-large registerbtn" onClick={() => navigate('register')}>Register</button> 
            
            <div className='other-links'>

                <a href='#'><img src={instagramLogo} alt="instagramLogo"/></a>
                <a href='#'><img src={facebookLogo} alt="facebookLogo"/></a> 
                <a href='#'><img src={twitterLogo} alt="twitterLogo"/></a>
                <a href='#'><img src={linkedinLogo} alt="linkedinLogo"/></a>
            </div>
        </div>
    );
}

export default Header;


import './header.css'

import logoImg from '../assets/icons/logo.png';
import instagramLogo from '../assets/icons/instagram.png';
import facebookLogo from '../assets/icons/facebook.png';
import twitterLogo from '../assets/icons/twitter.png';
import linkedinLogo from '../assets/icons/linkedin.png';

import { Link, useNavigate} from "react-router-dom";
function Header(props){

    let navigate = useNavigate();

    return (
        <div className="header">
            <Link to="/home"><img className='logo' src={logoImg} alt="logo"/></Link>

            <div className='navigate'>
                <Link className={props.pageName === 'leaderboard' ? "body-large focused" : "body-large"} to="/leaderboard">Leaderboard</Link>
                <Link className={props.pageName === 'game-guide' ? "body-large focused" : "body-large"} to="/game-guide">Game Guide</Link>
            </div>

            <div className='header-right'>


                {props.showLoginRegister ? <button className="body-large header-loginbtn" onClick={() => {}}>Login</button> : ""}
                {props.showLoginRegister ? <button className="body-large header-registerbtn" onClick={() => navigate('/register')}>Register</button> : ""}
                
                <div className='other-links'>

                    <a href='#'><img src={instagramLogo} alt="instagramLogo"/></a>
                    <a href='#'><img src={facebookLogo} alt="facebookLogo"/></a> 
                    <a href='#'><img src={twitterLogo} alt="twitterLogo"/></a>
                    <a href='#'><img src={linkedinLogo} alt="linkedinLogo"/></a>
                </div>
            </div>
        </div>
    );
}

export default Header;

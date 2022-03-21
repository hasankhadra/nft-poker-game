
import './header.css'

import logoImg from '../assets/logo.png';
import instagramLogo from '../assets/instagram.png';
import facebookLogo from '../assets/facebook.png';
import twitterLogo from '../assets/twitter.png';
import linkedinLogo from '../assets/linkedin.png';

function Header(props){
    return (
        <div className="header">
            <img className='logo' src={logoImg} alt="logo"/>
            { props.showLoginRegister ? "a" : ""}
            <div className='other-links'>
                <img src={instagramLogo} alt="instagramLogo"/>
                <img src={facebookLogo} alt="facebookLogo"/>
                <img src={twitterLogo} alt="twitterLogo"/>
                <img src={linkedinLogo} alt="linkedinLogo"/>
            </div>
        </div>
    );
}

export default Header;


import './home.css'

import Footer from '../components/footer';
import Header from '../components/header';

import backgroundImg from '../assets/background.png';
import backgroundImg2 from '../assets/background2.png';
import cardsImg from '../assets/nftCards.png'


function Home() {
    return (
        <div style={{height:'100vh', backgroundColor: "#25262A"}}>
            <Header/>
            <div style={{
                backgroundImage: `url(${backgroundImg2})`,
                height: "80%",
                marginLeft: "10%",
                backgroundColor: "#25262A",
                // backgroundColor: "white",
                backgroundSize: 'cover',
                backgroundRepeat: 'no-repeat',
                width: "80%",
                display: "flex", 
                flexDirection: "row"
            }}>
                <div className="text-box" style={{width: "45%"}}>
                    <h3>
                        Make your NFT worth more through <span style={{color: '#FFC728'}}>Poker Game</span>
                    </h3>
                    <p style={{color: '#FFFFFF'}}>
                    Capped Range NFT is an NFT gaming project in which holders will use their NFT asset to play in a heads-up single-elimination poker tournament consisting of 14 rounds. Each round, a holder will battle against another holder. Each holder’s specific NFT will have an assigned poker hand range attached to it.
                    </p>

                </div>
                <img className="nft-cards" src={cardsImg} alt="cards image" style={{right: 0}}></img>
            </div>
            <Footer/>
        </div>
    )
}

export default Home;


import './home.css'


import backgroundImg from '../assets/backgrounds/background.png';
import backgroundImg2 from '../assets/backgrounds/background2.png';
import cardsImg from '../assets/backgrounds/images/nftCards.png'

import {Helmet} from "react-helmet";

function Home() {
    return (
        <div>
            <Helmet>
                <title>Capped Range</title>
            </Helmet>
            <div style={{
                backgroundImage: `url(${backgroundImg2})`,
                height: "80%",
                marginLeft: "10%",
                backgroundSize: 'cover',
                backgroundRepeat: 'no-repeat',
                // width: "80%",
                display: "flex", 
                flexDirection: "row",
                flexWrap: "wrap",
                marginTop: "5rem"
            }}>
                <div className="text-box flex-item-left">
                    <h3 className='white'>
                        Make your NFT worth more through <span className='yellow'>Poker Game</span>
                    </h3>
                    <p className='white'>
                    Capped Range NFT is an NFT gaming project in which holders will use their NFT asset to play in a heads-up single-elimination poker tournament consisting of 14 rounds. Each round, a holder will battle against another holder. Each holder’s specific NFT will have an assigned poker hand range attached to it.
                    </p>

                </div>
                <img className="nft-cards flex-item-right" src={cardsImg} alt="cards image"></img>
            </div>
        </div>
    )
}

export default Home;

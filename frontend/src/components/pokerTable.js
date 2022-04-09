
import "./pokerTable.css";

import tableImg from '../assets/table.png';

function importAll(r) {
    let images = {};
    r.keys().forEach(item => { images[item.replace('./', '').replace('.png', '')] = r(item); });
    return images;
}

const cardsImages = importAll(require.context('../assets/cards', false, /\.png$/));

function PokerTable(props) {

    const cardsToImages = (cardsNames) => {
        return cardsNames.map((item, index) => <img key={index} className="card" src={cardsImages[item] || cardsImages["BACK"]} />)
    }

    return (
        <div className="play-table" style={{
            backgroundImage: `url(${tableImg})`,
            backgroundSize: 'cover',
            backgroundRepeat: 'no-repeat',
            backgroundSize: '100% 100%',
        }}>
            <div className="hand-cards opponent-hand">
                {cardsToImages(props.opponentHand)}
            </div>

            <div className="flops-cards">
                {cardsToImages(props.flops)}
            </div>

            <div className="hand-cards my-hand">
                {cardsToImages(props.myHand)}
            </div>
        </div>
    )
}

export default PokerTable;
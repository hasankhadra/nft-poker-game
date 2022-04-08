
import './playerCard.css'

function PlayerCard(props) {
    const ProfileImage = props.profileImage;
    return (
        <div className='player-card-wrapper'>
            <img src={props.profileImage}/>
            <div className="player-card-text-box">
                <span className='yellow'>{props.type}</span> <br /> <span className='white'>{props.name}</span>
            </div>
        </div>
    )
}

export default PlayerCard;
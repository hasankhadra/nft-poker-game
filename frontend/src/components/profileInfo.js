import "./profileInfo.css"

import profileImg from '../assets/profileInfoIcons/profile.png';
import totalBountiesImg from '../assets/profileInfoIcons/totalBounties.png';
import totalNftsImg from '../assets/profileInfoIcons/totalNfts.png';
import totalRoundsImg from '../assets/profileInfoIcons/totalRounds.png';
import { useMemo } from "react";

const InfoCard = (props) => {
    return (
        <div className="info-card">
            <img src={props.icon} />
            <div>
                <div className="card-upper-text">
                    {props.upperText}
                </div>
                <div className="card-lower-text">
                    {props.lowerText}
                </div>
            </div>
        </div>
    )
}

function ProfileInfo(props) {

    const totalBounties = useMemo(() => {
        let total = ''
        if (props.totalBounties > 1000000){
            total = Math.floor(props.totalBounties / 1000000).toString() + 'M';
        }
        else if (props.totalBounties > 1000){
            total = Math.floor(props.totalBounties / 1000).toString() + 'K';
        }
        else{
            total = props.totalBounties.toString()
        }
        return '$' + total;
    }, [props.totalBounties])
    
    return (
        <div className="profile-info-cards">
            <InfoCard icon={profileImg} upperText={props.username ?? 'username'} lowerText={props.isActive ? 'Active' : 'Lost'}/>
            <InfoCard icon={totalNftsImg} upperText="Total NFTs" lowerText={props.numNfts ?? 0}/>
            <InfoCard icon={totalRoundsImg} upperText="Total Rounds" lowerText={props.totalRounds ?? 12}/>
            <InfoCard icon={totalBountiesImg} upperText="Total Bounties" lowerText={totalBounties ?? 0}/>
        </div>
    )
}

export default ProfileInfo;
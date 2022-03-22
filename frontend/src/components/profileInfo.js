import "./profileInfo.css"

function ProfileInfo(props){

    return (
        <div className="profile-info">
            <div className="block">
                Total {props.numNfts} {props.numNfts > 1 ? "NFTs" : "NFT"}
            </div>
            <div className="block">
                Total {props.numGames} {props.numGames == 1 ? "Game" : "Games"}
            </div>
            <div className="block">
                Total ${props.totalBounties} Bounty
            </div>
        </div>
    )
}

export default ProfileInfo;
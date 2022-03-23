
import { useEffect, useState, useCallback, useContext } from "react";

import Footer from '../components/footer';
import Header from '../components/header';

import backgroundImg from '../assets/backgrounds/background.png';

import { getAddress } from '../utils/metamaskAuth';
import { SocketContext } from '../contexts/socket';
import { PlayersTable } from '../components/playersTable'

import './leaderboard.css'

function Leaderboard() {

    const socket = useContext(SocketContext);
    const [hasMetaMask, setHasMetaMask] = useState(false);
    const [players, setPlayers] = useState([]);
    const [paginate, setPaginate] = useState(30);

    useEffect(() => {
        socket.on('get_players', getPlayersListener);

        return () => {
            socket.off('get_players', getPlayersListener);
        }
    }, [socket]);

    useEffect(() => {
        if (typeof window.ethereum !== "undefined") {
            setHasMetaMask(true);
        }
    });


    useEffect(() => {
        socket.emit("get_players");
        // const newPlayers = [
        //     {id: 1, username: "hasan", bounty: 10, Round_number: 2},
        //     {id: 2, username: "hash", bounty: 100, Round_number: 1},
        //     {id: 3, username: "igor", bounty: 35, Round_number: 3}
        // ]

        // setPlayers(newPlayers);
    }, []);

    const comparePlayers = (player1, player2) => {
        if (player2.round_num === player1.round_num)
            return player2.bounty - player1.bounty;
        return player2.round_num - player1.round_num;
    }

    const getPlayersListener = useCallback(async (response) => {
        response.players.sort(comparePlayers);
        console.log(response.players);
        response.players.map((player, index) => player.page = Math.ceil((index + 1) / paginate));
        response.players.map((player, index) => player.rank = index + 1);
        setPlayers(response.players);
    }, [players]);

    const getMyNFTs = async () => {
        const myAddress = await getAddress();
        let myNfts = players.filter(player => player.public_address === myAddress)
        myNfts.map((player, index) => player.page = Math.ceil((index + 1) / paginate));
        return myNfts
    }

    return (
        <div style={{ height: '100vh', backgroundColor: "#25262A", display: "flex", flexDirection: "column" }}>
            <Header pageName={'leaderboard'} />
            <div style={{
                backgroundImage: `url(${backgroundImg})`,
                height: "80%",
                marginLeft: "10%",
                // marginBottom: "10%",
                backgroundColor: "#25262A",
                // backgroundColor: "white",
                backgroundSize: 'cover',
                backgroundRepeat: 'no-repeat',
                width: "80%",
                display: "flex",
                flexDirection: "column"
            }}>
                <h4 style={{color: "white", margin: "1% 1%", height: "10%"}}>Game Leaderboard</h4>
                <p style={{color: "white",  margin: "2% 1%", height: "10%"}}>
                This leaderboard includes the <span className="yellow">1st Round</span> of the game that took place on <span className="yellow">July 21st, 2022</span>.
                 All the participants were given bounties according to the description in the <span className="yellow">Game Guide </span>
                 page. All players who participated are shown regardless of their win/lost status.
                </p>
                <PlayersTable players={players} paginate={paginate} />
            </div>

            <Footer />
        </div>
    )
}

export default Leaderboard;

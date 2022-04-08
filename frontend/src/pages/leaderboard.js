
import { useEffect, useState, useCallback, useContext } from "react";
import {Helmet} from "react-helmet";

import backgroundImg from '../assets/backgrounds/background.png';

import { getAddress } from '../utils/metamaskAuth';
import { SocketContext } from '../contexts/socket';
import { PlayersTable } from '../components/playersTable'

import './leaderboard.css'

function Leaderboard() {

    const socket = useContext(SocketContext);
    const [hasMetaMask, setHasMetaMask] = useState(false);
    const [players, setPlayers] = useState([]);
    const [paginate, setPaginate] = useState(10);

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
        // // TESTING FRONTEND

        // const newPlayers = [
        //     {id: 1, username: "user1", bounty: 10, round_num: 2},
        //     {id: 2, username: "user2", bounty: 32.4, round_num: 1},
        //     {id: 3, username: "user3", bounty: 5, round_num: 1},
        //     {id: 4, username: "user4", bounty: 23.4, round_num: 3},
        //     {id: 5, username: "user5", bounty: 5.1, round_num: 2},
        //     {id: 6, username: "user6", bounty: 2, round_num: 3},
        //     {id: 7, username: "user7", bounty: 35, round_num: 3},
        //     {id: 8, username: "user8", bounty: 10, round_num: 2},
        //     {id: 9, username: "user9", bounty: 32.4, round_num: 3},
        //     {id: 10, username: "user10", bounty: 5, round_num: 1},
        //     {id: 11, username: "user11", bounty: 23.4, round_num: 3},
        //     {id: 12, username: "user12", bounty: 5.1, round_num: 2},
        //     {id: 13, username: "user13", bounty: 10, round_num: 2},
        // ]
        
        // newPlayers.sort(comparePlayers);
        // newPlayers.map((player, index) => player.page = Math.ceil((index + 1) / paginate));
        // newPlayers.map((player, index) => player.rank = index + 1);
        // setPlayers(newPlayers);
        // return;
        // // TESTING FRONTEND

        
        socket.emit("get_players");
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
            <Helmet>
                <title>Leaderboard</title>
            </Helmet>
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
        </div>
    )
}

export default Leaderboard;

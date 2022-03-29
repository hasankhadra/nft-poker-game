import io from 'socket.io-client';
import { useEffect, useState, useCallback, useContext } from "react";
import { getAddress } from '../utils/metamaskAuth';
import ProfileInfo from '../components/profileInfo';
import NftList from '../components/nftList';
import { SocketContext } from '../contexts/socket';

import Footer from '../components/footer';
import Header from '../components/header';

import backgroundImg from '../assets/backgrounds/background.png';



function Lobby() {

    const socket = useContext(SocketContext);
    const [hasMetaMask, setHasMetaMask] = useState(false);
    const [nfts, setNfts] = useState([]);
    const [paginate, setPaginate] = useState(10);

    useEffect(() => {
        socket.on('get_nfts_info', getNftsListener);

        return () => {
            socket.off('get_nfts_info', getNftsListener);
        }
    }, [socket]);

    useEffect(() => {
        if (typeof window.ethereum !== "undefined") {
            setHasMetaMask(true);
        }
    });

    useEffect(async () => {

        // // TESTING FRONTEND

        // const newNfts = [
        //     { nft_id: 1, username: "user1", bounty: 10, round_num: 2, staked: true},
        //     { nft_id: 2, username: "user2", bounty: 32.4, round_num: 1, staked: true  },
        //     { nft_id: 3, username: "user3", bounty: 5, round_num: 1, staked: true },
        //     { nft_id: 4, username: "user4", bounty: 23.4, round_num: 3, staked: false  },
        //     { nft_id: 5, username: "user5", bounty: 5.1, round_num: 2, staked: true },
        //     { nft_id: 6, username: "user6", bounty: 2, round_num: 3, staked: true },
        //     { nft_id: 7, username: "user7", bounty: 35, round_num: 3, staked: false  },
        //     { nft_id: 8, username: "user8", bounty: 10, round_num: 2, staked: true },
        //     { nft_id: 9, username: "user9", bounty: 32.4, round_num: 3, staked: false  },
        //     { nft_id: 10, username: "user10", bounty: 5, round_num: 1, staked: true },
        //     { nft_id: 11, username: "user11", bounty: 23.4, round_num: 3, staked: true  },
        //     { nft_id: 12, username: "user12", bounty: 5.1, round_num: 2, staked: true },
        //     { nft_id: 13, username: "user13", bounty: 10, round_num: 2, staked: false },
        // ]
        // newNfts.sort(compareNfts);
        // newNfts.map((player, index) => player.page = Math.ceil((index + 1) / paginate));
        // newNfts.map((player, index) => player.rank = index + 1);
        // setNfts(newNfts);
        // return;
        // // TESTING FRONTEND


        let public_address = await getAddress()
        console.log(public_address)
        const payload = {
            public_address: public_address
        }
        socket.emit("get_nfts_info", payload);
    }, []);

    const compareNfts = (nft1, nft2) => {
        if (nft2.round_num === nft1.round_num)
            return nft2.bounty - nft1.bounty;
        return nft2.round_num - nft1.round_num;
    }

    const getNftsListener = useCallback(async (response) => {
        console.log(response.nfts);
        response.nfts.sort(compareNfts);
        response.nfts.map((nft, index) => nft.page = Math.ceil((index + 1) / paginate));
        response.nfts.map((nft, index) => nft.rank = index + 1);
        setNfts(response.nfts);
    }, [nfts]);

    const getGamesNum = () => {
        let total_games = 0;
        for (let i = 0; i < nfts.length; i++)
            total_games += nfts[i].round_num - 1;

        return total_games;
    }

    const getTotalBounties = () => {
        let total_bounties = 0.0;
        for (let i = 0; i < nfts.length; i++)
            total_bounties += nfts[i].bounty;

        return total_bounties;
    }

    return (

        <div style={{ height: '100vh', backgroundColor: "#25262A", display: "flex", flexDirection: "column" }}>
            <Header />
            <div style={{
                backgroundImage: `url(${backgroundImg})`,
                height: "88%",
                marginLeft: "10%",
                backgroundColor: "#25262A",
                // backgroundColor: "white",
                backgroundSize: 'cover',
                backgroundRepeat: 'no-repeat',
                width: "80%",
                display: "flex",
                flexDirection: "column"
            }}>

                <ProfileInfo numNfts={nfts.length} numGames={getGamesNum()} totalBounties={getTotalBounties()} />
                <h5>Next Round: It will start in (put timer here)</h5>
                <NftList nfts={nfts} paginate={paginate} />
            </div>

            <Footer />
        </div>
    )
}

export default Lobby;

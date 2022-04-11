
import { useEffect, useState, useCallback, useContext } from "react";
import io from 'socket.io-client';
import { Helmet, HelmetProvider } from 'react-helmet-async';

import { getAddress } from '../utils/metamaskAuth';

import ProfileInfo from '../components/profileInfo';
import NftList from '../components/nftList';

import { SocketContext } from '../contexts/socket';

import backgroundImg from '../assets/backgrounds/background.png';

import NextRoundTimer from '../components/nextRoundTimer'


function Lobby() {

    const socket = useContext(SocketContext);
    const [hasMetaMask, setHasMetaMask] = useState(false);
    const [nfts, setNfts] = useState([]);
    const [paginate, setPaginate] = useState(10);
    const [roundInfo, setRoundInfo] = useState({})
    const [receivedNfts, setReceivedNfts] = useState(false);
    const [receivedRound, setReceivedRound] = useState(false);

    useEffect(() => {
        socket.on('get_nfts_info', getNftsListener);
        socket.on('round_info', getCurrentRoundListener);
        return () => {
            socket.off('get_nfts_info', getNftsListener);
            socket.off('round_info', getCurrentRoundListener);
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
        const payload = {
            public_address: public_address
        }
        socket.emit("get_nfts_info", payload);
        socket.emit("round_info");
    }, []);

    const compareNfts = (nft1, nft2) => {
        if (nft2.round_num === nft1.round_num)
            return nft2.bounty - nft1.bounty;
        return nft2.round_num - nft1.round_num;
    }

    const getNftsListener = useCallback(async (response) => {
        response.nfts.sort(compareNfts);
        response.nfts.map((nft, index) => nft.page = Math.ceil((index + 1) / paginate));
        response.nfts.map((nft, index) => nft.rank = index + 1);
        setNfts(response.nfts);
        setReceivedNfts(true)
    }, [nfts, receivedNfts]);

    const getCurrentRoundListener = useCallback(async (response) => {
        setRoundInfo({
            startTime: response.start_time,
            endTime: response.end_time,
            roundNum: response.round_num
        });
        setReceivedRound(true);
    }, [roundInfo, receivedRound]);

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

    const getIsActive = () => {
        return nfts.some(x => !x.is_rail)
    }

    const updateNfts = (nftId, key, value) => {
        let newNfts = nfts.map(nft => {
            if (nft.nft_id === nftId){
                return {
                    ...nft,
                    [key]: value
                }
            }
            else 
                return {
                    ...nft
                }
        })
        setNfts(newNfts)
    }

    // if (!receivedNfts || !receivedRound){
    //     return ""
    // }

    return (
        <div style={{
            height: '90vh', width: "100vw", backgroundImage: `url(${backgroundImg})`,
            backgroundSize: 'cover', backgroundRepeat: 'repeat', backgroundColor: "#1A1A1C",
            display: "flex", flexDirection: "column", alignItems: "center",
            justifyContent: "center", paddingTop: ".1rem"
        }}>
            <HelmetProvider>
                <Helmet>
                    <title>Lobby</title>
                </Helmet>
                <ProfileInfo isActive={getIsActive()} numNfts={nfts.length} totalRounds={getGamesNum()} totalBounties={getTotalBounties()} />
                <NextRoundTimer roundNum={roundInfo.roundNum} isActive startTime1={roundInfo.startTime ?? ''} startTime="2022-05-08 06:00:00" />
                <NftList nfts={nfts} paginate={paginate} stakeNft={(nftId) => updateNfts(nftId, 'staked', 1)} unstakeNft={(nftId) => updateNfts(nftId, 'staked', 0)}/>
            </HelmetProvider>
        </div>
    )
}

export default Lobby;

import io from 'socket.io-client';
import { useEffect, useState, useCallback, useContext } from "react";
import {getAddress} from '../utils/metamaskAuth';
import ProfileInfo from '../components/profileInfo';
import NftList from '../components/nftList';
import { SocketContext } from '../contexts/socket';

import Footer from '../components/footer';
import Header from '../components/header';

import backgroundImg from '../assets/background.png';



function Lobby(){

    const socket = useContext(SocketContext);
    const [hasMetaMask, setHasMetaMask] = useState(false);
    const [nfts, setNfts] = useState([]);
    const [paginate, setPaginate] = useState(3);

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

    useEffect(() => {
        let public_address = "add1" // getAddress()
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


    return (

        <div style={{height:'100vh', backgroundColor: "#25262A"}}>
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
                flexDirection: "column"}}>

                <ProfileInfo />
                <div>Next Round: It will start in (put timer here)</div>
                <NftList nfts={nfts} paginate={paginate}/>
            </div>

            <Footer />
        </div>
    )
}

export default Lobby;

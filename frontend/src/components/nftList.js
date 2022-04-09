
import './nftList.css'

import { useEffect, useState, useCallback, useContext, useMemo } from "react";

import arrowLeft from '../assets/arrows/vector-l.png'
import arrowRight from '../assets/arrows/vector-r.png'


function NftList(props) {

    const [curPage, setCurPage] = useState(1);

    const maxPage = useMemo(() => {
        return Math.max(Math.ceil(props.nfts.length / props.paginate), 1);
    }, [props.paginate, props.nfts]);

    return (

        <div style={{ width: "80%", height: "100%" }}>
            <div className="nfts-table">
                <table style={{ width: "100%" }}>
                    <tr>
                        <th className='body-large'>#</th>
                        <th className='body-large'>NFT</th>
                        <th className='body-large'>Username</th>
                        <th className='body-large'>Linked Tier</th>
                        <th className='body-large'>Total Bounty (USDT)</th>
                        <th className='body-large'>Round</th>
                        <th className='body-large'>Stake</th>
                    </tr>
                    {
                        props.nfts.map((element, index) => {
                            if (curPage === element.page)
                                return (
                                    <tr key={element.id}>
                                        <td className='body-large'>{index}</td>
                                        <td className='body-large'>{element.nft_id}</td>
                                        <td className='body-large'>{element.username}</td>
                                        <td className='body-large'>{ }</td>
                                        <td className='body-large'>${element.bounty}</td>
                                        <td className='body-large'>{element.round_num}</td>
                                        <td className='body-large'>{element.staked ? "Staked" : "Unstaked"}</td>
                                    </tr>
                                )
                            return "";
                        })
                    }
                </table>
            </div>
            <div className="pagination">

                <p className='all-pages'>{Math.min(props.nfts.length, (curPage - 1) * props.paginate + 1)} - {Math.min(curPage * props.paginate, props.nfts.length)} of {props.nfts.length}</p>

                <p className='decrement' onClick={() => setCurPage(prev => Math.max(1, prev - 1))}><img src={arrowLeft} alt="left-arrow" /></p>

                {curPage <= 3 ? null : <p onClick={() => setCurPage(1)}>1</p>}
                {curPage <= 4 ? null : <p className='dots'>...</p>}

                {curPage <= 2 ? null : <p onClick={() => setCurPage(prev => Math.max(1, prev - 2))}> {curPage - 2}</p>}
                {curPage === 1 ? null : <p onClick={() => setCurPage(prev => Math.max(1, prev - 1))}> {curPage - 1}</p>}

                {<p style={{ background: "#4C4F58" }} onClick={() => { }}> {curPage}</p>}

                {curPage >= maxPage ? null : <p onClick={() => setCurPage(prev => Math.min(maxPage, prev + 1))}> {curPage + 1}</p>}
                {curPage >= maxPage - 1 ? null : <p onClick={() => setCurPage(prev => Math.min(maxPage, prev + 2))}> {curPage + 2}</p>}

                {curPage >= maxPage - 3 ? null : <p className='dots'>...</p>}
                {curPage >= maxPage - 2 ? null : <p onClick={() => setCurPage(maxPage)}>{maxPage}</p>}

                <p className='increment' onClick={() => setCurPage(prev => Math.min(maxPage, prev + 1))}><img src={arrowRight} alt="right-arrow" /></p>
            </div>
        </div>
    )
}

export default NftList;

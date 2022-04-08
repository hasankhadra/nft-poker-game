import Footer from "../../components/footer";
import backgroundImg from '../../assets/backgrounds/background.png';
import { useState, useContext, useCallback } from "react";
import { SocketContext } from '../../contexts/socket';
import {getAddress} from '../../utils/metamaskAuth';


function AdminPanel() {
    const [startTime, setStartTime] = useState('');
    const [endTime, setEndTime] = useState('');
    const socket = useContext(SocketContext);

    const onSubmit = async (e) => {
        e.preventDefault();
        await window.ethereum.enable();
        let payload = {
            start_time: startTime,
            end_time: endTime,
            public_address: await getAddress()
        }
        socket.emit("add_round", payload);
    };

    return (
        <div style={{ height: '100vh', backgroundColor: "#25262A", display: "flex", flexDirection: "column" }}>
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
                flexDirection: "row"
            }}>
                <div className="mid-page">
                    <form onSubmit={onSubmit}>
                        <label><b>Round start time</b></label>
                        <input
                            type="text"
                            placeholder="YYYY-MM-DD HH:MM:SS"
                            name="start_time"
                            value={startTime}
                            onChange={e => setStartTime(e.target.value)}
                        />
                        <label><b>Round end time</b></label>
                        <input
                            type="text"
                            placeholder="YYYY-MM-DD HH:MM:SS"
                            name="end_time"
                            required
                            value={endTime}
                            onChange={e => setEndTime(e.target.value)}
                        />
                        <button type="submit" className="addroundbtn">Add a new round</button>
                    </form>
                </div>
            </div>
            <Footer />
        </div>
    )

}

export default AdminPanel;
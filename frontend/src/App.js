
import './App.css';
import { ethers } from "ethers";
import io from 'socket.io-client';
import { useEffect, useState } from "react";

function App() {

  const [socket, setSocket] = useState(null);
  const [hasMetaMask, setHasMetaMask] = useState(false);
  const [username, setUsername] = useState('');

  useEffect(() => {
    const newSocket = io('http://localhost:5000');
    setSocket(newSocket);
    return () => newSocket.close();
  }, []);

  useEffect(() => {
    
    return () => {
      
    }
  }, [socket]);

  useEffect(() => {
    if (typeof window.ethereum !== "undefined") {
      setHasMetaMask(true);
    }
  });

  const getAddress = async () => {
    const provider = new ethers.providers.Web3Provider(window.ethereum, "any");
    await provider.send("eth_requestAccounts", []);
    const signer = provider.getSigner();
    const address = await signer.getAddress();
    return address;
}

  const onSubmit = async (e) => {
    e.preventDefault();
    const address = await getAddress();
    const payload = {
      public_address: address,
      username: username
    }
    socket.emit("register", payload);
  }

  return (
    <div className="App">
      {hasMetaMask ? <div>
        <form onSubmit={onSubmit}>
        <label>
            Username: 
            <input
                type="text"
                placeholder="A unique username"
                name="username"
                value={username}
                onChange={e => setUsername(e.target.value.trim())}
            />
          </label>
          <button type="submit"> Register </button>
        </form>
      </div>
        : "Please install MetaMask"}
    </div>
  );
}

export default App;

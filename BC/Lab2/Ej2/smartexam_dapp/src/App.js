import React, { useCallback, useEffect, useState } from "react";
import './App.css';
import { create } from 'kubo-rpc-client'
import { ethers } from "ethers"
import { Buffer } from "buffer"
import logo from "./municsLogo.png"
import { addresses, abis } from "./contracts"

const ZERO_ADDRESS = "0x0000000000000000000000000000000000000000000000000000000000000000";
let client

const defaultProvider = new ethers.providers.Web3Provider(window.ethereum);
// version 6
//const defaultProvider = new ethers.BrowserProvider(window.ethereum);

const ipfsContract = new ethers.Contract(
  addresses.ipfs,
  abis.ipfs,
  defaultProvider
);

//contract = new ethers.Contract(address, abi, defaultProvider);

async function readCurrentExam() {
  const result = await ipfsContract.exams(
    defaultProvider.getSigner().getAddress()
  );
  console.log({ result });
  return result;
}

function App() {

  // Also used to print the hash in the UI
  const [ipfsHash, setIpfsHash] = useState(""); 

  useEffect(() => {
    window.ethereum.enable();
  }, []);

  let [connected, setConnected] = useState(false);

  const [file, setFile] = useState(null);

  useEffect(() => {
    async function readFile() {
      const file = await readCurrentExam();

      if (file !== ZERO_ADDRESS) setIpfsHash(file);
    }
    readFile();
  }, []);

  /*************************************************************************/
  /********************** - Upload a file to IPFS & - **********************/
  /*************** - Store its hash in the smart-contract - ****************/
  /*************************************************************************/
  async function setExamIPFS(hash) {
    const ipfsWithSigner = ipfsContract.connect(defaultProvider.getSigner());
    console.log("TX contract");
    const tx = await ipfsWithSigner.setExamIPFS(hash);
    console.log({ tx });
    setIpfsHash(hash);
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      console.log(file)
      // conectar a la instancia en local de ipfs
      const client = await create('/ip4/127.0.0.1/tcp/5001')
      // añadir le archivo a ipfs
      const result = await client.add(file)
      // añadir al fs del nodo ipfs en local para poder visualizarlo en el dashboard
      await client.files.cp(`/ipfs/${result.cid}`, `/${result.cid}`)
      console.log(result.cid)
      // añadir el CID de ipfs a ethereum a traves del smart contract
      await setExamIPFS(result.cid.toString());
    } catch (error) {
      console.log(error.message);
    }
  };

  const retrieveFile = (e) => {
    const data = e.target.files[0];
    const reader = new window.FileReader();
    reader.readAsArrayBuffer(data);
    console.log(data);
    reader.onloadend = () => {
    console.log("Buffer data: ", Buffer(reader.result));
      setFile(Buffer(reader.result));
    }
    e.preventDefault();
  }
  /*************************************************************************/


  /*************************************************************************/
  /********************** - Check if an exam exsits - **********************/
  /*************************************************************************/
  const [checkText, setCheckText] = useState('');

  async function checkSubmited(hash) {
    const ipfsWithSigner = ipfsContract.connect(defaultProvider.getSigner());
    console.log("Cheking exam hash:")
    const check = await ipfsWithSigner.checkSubmited(hash);
    console.log(check)
    if (check) {
      setCheckText("Exam was submitted!");
    } else {
      setCheckText("Exam WAS NOT submitted!");
    }    
  }

  const handleCheck = async (event) => {
    event.preventDefault();
    try {
      const examHash = event.target.elements.texto.value;
      await checkSubmited(examHash)
    } catch (error) {
      console.log(error.message);
    }
  }
  /*************************************************************************/


  return (
    <div className="App">
      <header className="App-header">
        <h1></h1>
        <img src={logo} className="App-logo" alt="logo" />
        <h1></h1>
        <div class="form-container">
          <form id="upload-file" class="inline-form" onSubmit={handleSubmit}>
            <h3>Upload a file to IPFS</h3>
            <input type="file" name="data" onChange={retrieveFile} />
            <button type="submit" className="btn">Upload</button>
            {ipfsHash && (
              <div>
                <p>{ipfsHash}</p>
              </div>
            )}
          </form>
          <form id="check-file" class="inline-form" onSubmit={handleCheck}>
            <h3>Check exam submitted</h3>
            <input type="text" id="texto" name="texto" />
            <button type="submit" className="btn">Check</button>
            {checkText && (
              <div>
                <p>{checkText}</p>
              </div>
            )}
          </form>
          
        </div>     
      </header>
    </div>
    );
}

export default App;
//http://0.0.0.0:5001/ipfs/bafybeibozpulxtpv5nhfa2ue3dcjx23ndh3gwr5vwllk7ptoyfwnfjjr4q/#/files



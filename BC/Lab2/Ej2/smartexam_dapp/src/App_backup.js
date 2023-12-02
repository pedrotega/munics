import React, { useCallback, useEffect, useState } from "react";
import './App.css';
import { create } from 'kubo-rpc-client'
import { ethers } from "ethers"
import { Buffer } from "buffer"
import logo from "./municsLogo.png"
import { addresses, abis } from "./contracts"



const ZERO_ADDRESS = "0x0000000000000000000000000000000000000000000000000000000000000000";
const ZERO_ADDRESS_STUDENT = "0x0000000000000000000000000000000000000000" /**************************************/ 
let client
let return_value

const defaultProvider = new ethers.providers.Web3Provider(window.ethereum);
// version 6
//const defaultProvider = new ethers.BrowserProvider(window.ethereum);

const smartExam = new ethers.Contract(
  addresses.ipfs,
  abis.ipfs,
  defaultProvider
);

const smartExamSigner = smartExam.connect(defaultProvider.getSigner());

let hexValue = await smartExamSigner.getEnrollingPrice();
let price = parseInt(hexValue).toString();
const ENROLLING_PRICE = price + " wei"

//contract = new ethers.Contract(address, abi, defaultProvider);

// async function readCurrentExam() {
//   const result = await smartExam.getExams();
//   //   defaultProvider.getSigner().getAddress()
//   // );
//   console.log({ result });
//   return result;
// }

function App() {

  const [ipfsHash, setIpfsHash] = useState(""); 

  useEffect(() => {
    window.ethereum.enable();
  }, []);

  let [connected, setConnected] = useState(false);

  const [file, setFile] = useState(null);

  // useEffect(() => {
  //   async function readFile() {
  //     const file = await readCurrentExam();

  //     if (file !== ZERO_ADDRESS) setIpfsHash(file);
  //   }
  //   readFile();
  // }, []);
  

  /*************************************************************************/
  /********************** - Upload a file to IPFS & - **********************/
  /*************** - Store its hash in the smart-contract - ****************/
  /*************************************************************************/
  const [examHash, setExamHash] = useState(""); 

  async function setExamIPFS(hash) {
    const ipfsWithSigner = smartExam.connect(defaultProvider.getSigner());
    console.log("TX contract");
    const tx = await ipfsWithSigner.setExamIPFS(hash);
    console.log({ tx });
    setIpfsHash(hash);
    setExamHash(hash)
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      console.log("file", file)
      //let encryptedFile = await encryptFile(publicKeyFile, file)
      //console.log(encryptedFile)
      //conectar a la instancia en local de ipfs
      const client = await create('/ip4/127.0.0.1/tcp/5001')
      // añadir el archivo a ipfs
      const result = await client.add(file)
      // añadir al fs del nodo ipfs en local para poder visualizarlo en el dashboard
      await client.files.cp(`/ipfs/${result.cid}`, `/${result.cid}`)
      console.log(result.cid)
      // añadir el CID de ipfs a ethereum a traves del smart contract
      // await setExamIPFS(result.cid.toString());
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
    const ipfsWithSigner = smartExam.connect(defaultProvider.getSigner());
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

  /*************************************************************************/
  /******************** - Get student from hash exam - *********************/
  /*************************************************************************/
  // const [studentAddress, setStudentAddress] = useState('');

  // async function getStudentAddress(hash) {
  //   const ipfsWithSigner = smartExam.connect(defaultProvider.getSigner());
  //   console.log("Student address:")
  //   const studentAdd = await ipfsWithSigner.getStudent(hash);
  //   console.log(studentAdd)
  //   if (studentAdd === ZERO_ADDRESS_STUDENT){
  //     setStudentAddress("Exam DOES NOT exist!");
  //   } else {
  //     setStudentAddress(studentAdd)
  //   }
  // }

  // const handleGetStudent = async (event) => {
  //   event.preventDefault();
  //   try {
  //     const studentAdd = event.target.elements.texto.value;
  //     await getStudentAddress(studentAdd)
  //   } catch (error) {
  //     console.log(error.message);
  //   }
  // }
  /*************************************************************************/

  /*************************************************************************/
  /************************* - Get exam from IPFS - ************************/
  /*************************************************************************/
  const handleGetExam = async (event) => {
    event.preventDefault();
    try {
      const cid = event.target.elements.texto.value;
      // conectar a la instancia en local de ipfs
      const client = await create('/ip4/127.0.0.1/tcp/5001')
      
      const result = client.cat(cid)
      const chunks = []
      for await (let res of result) {
        chunks.push(res)
      }
      const buffer = Buffer.concat(chunks)
      const blob = new Blob([buffer], { type: 'image/jpeg' }); // Adjust the type based on your image format
  
      // Create an object URL
      const objectURL = URL.createObjectURL(blob);
      // Display the image in an <img> element (optional)
      const examImg = new Image();
      examImg.src = objectURL;
      const imageExamContainer = document.getElementById('imageExamContainer');
      if (imageExamContainer) {
        imageExamContainer.appendChild(examImg); // Agrega la imagen al div con el ID "imageContainer"
      }
      // document.body.appendChild(
      //   <div>
      //     examImg
      //   </div>); // Append the image to the body
    
      // To download the image file, create a link element and trigger the download
      const link = document.createElement('a');
      link.href = objectURL;
      link.download = 'image.jpg'; // Set the desired file name here
      link.click();

      // createImageFile(exam)
      // console.log(typeof exam)
      // console.log(exam)
      // console.log('hola')
    } catch (error) {
      console.log(error.message);
    }
  };
  /*************************************************************************/

  /*#######################################################################*/
  /*########################## - OWNERS'S LOGIC - #########################*/
  /*#######################################################################*/
  const handleAddProfessor = async (event) => {
    event.preventDefault();
    try{
      const addProf = event.target.elements.texto.value;
      const rsp = await smartExamSigner.registerProfessor(addProf);
      console.log("Response register professor:", rsp);
    } catch (error) {
      console.log(error.message);
    }
  }
  /*#######################################################################*/

  /*#######################################################################*/
  /*######################## - PROFESSOR'S LOGIC - ########################*/
  /*#######################################################################*/

  /********************** - Get exams from contract - **********************/
  const [examHashes, setExamHashes] = useState("");

  const handleGetExams = async (event) => {
    event.preventDefault();
    try {
      const _examHashes = await smartExamSigner.getExams();
      console.log("Exams:", _examHashes)
      setExamHashes(_examHashes);
    } catch (error) {
      console.log(error.message);
    }
  };
  /*************************************************************************/

  /******************** - Get corrections from contract - ******************/
  const [correctionHashes, setCorrectionHashes] = useState("");

  const handleGetCorrections = async (event) => {
    event.preventDefault();
    try {
      const _correctionHashes = await smartExamSigner.getCorrections();
      console.log("Correction hashes:", _correctionHashes)
      setCorrectionHashes(_correctionHashes);
    } catch (error) {
      console.log(error.message);
    }
  };
  /*************************************************************************/

  /******************** - Get student from hash exam - *********************/
  const [studentAddress, setStudentAddress] = useState('');

  const handleGetStudent = async (event) => {
    event.preventDefault();
    try {
      const _hash = event.target.elements.texto.value;
      const studentAdd = await smartExamSigner.getStudent(_hash)
      console.log("Student address:",studentAdd)
      setStudentAddress(studentAdd)
    } catch (error) {
      console.log(error.message);
    }
  }
  /*************************************************************************/

  /********************** - Download exam from IPFS - **********************/
  const handleDownloadExam = async (event) => {
    event.preventDefault();
    try {
      const cid = event.target.elements.texto.value;

      // Connecting to the local IPFS node.
      const client = create('/ip4/127.0.0.1/tcp/5001');
      
      // Getting the exam from IPFS.
      const result = client.cat(cid);
      const chunks = [];
      for await (let res of result) {
        chunks.push(res);
      }
      const buffer = Buffer.concat(chunks);
      // Adjust the type based on the image format.
      const blob = new Blob([buffer], { type: 'image/jpeg' }); 
  
      // Create an object URL
      const objectURL = URL.createObjectURL(blob);
      // Display the image in an <img> element.
      const examImg = new Image();
      examImg.src = objectURL;
      const imageExamContainer = document.getElementById('imageExamContainer');
      if (imageExamContainer) {
        imageExamContainer.appendChild(examImg); // Agrega la imagen al div con el ID "imageContainer"
      }
    
      // Downloading the image file, create a link element and trigger the download
      const link = document.createElement('a');
      link.href = objectURL;
      link.download = 'exam.jpg'; // Set the desired file name here
      link.click();
    } catch (error) {
      console.log(error.message);
    }
  };
  /*************************************************************************/

  /*********************** - Upload Correction IPFS - **********************/
  const [correction, setCorrection] = useState(null);
  const [correctionHash, setCorrectionHash] = useState("");

  async function setCorrectionContract(_examHash, _correctionHash) {
    const rsp = await smartExamSigner.setCorrection(_examHash, _correctionHash)
    console.log("Setting correction response:",rsp);
    setCorrectionHash(_correctionHash)
  }

  const handleUploadCorrection = async (event) => {
    event.preventDefault();
    try {
      const _examHash = event.target.elements.texto.value;
      console.log("Exam hash:", _examHash);
      const client = create('/ip4/127.0.0.1/tcp/5001');
      // Add file to IPFS.
      const result = await client.add(correction);
      // Add file to the local node file system to be able to visualize it.
      await client.files.cp(`/ipfs/${result.cid}`, `/${result.cid}`);
      console.log("Correction hash:", result.cid);
      // añadir el CID de ipfs a ethereum a traves del smart contract
      await setCorrectionContract(result.cid.toString());
    } catch (error) {
      console.log(error.message);
    }
  };

  const retrieveCorrectionFile = (e) => {
      const data = e.target.files[0];
      const reader = new window.FileReader();
      reader.readAsArrayBuffer(data);
      console.log(data);
      reader.onloadend = () => {
        console.log("Buffer data: ", Buffer(reader.result));
        setCorrection(Buffer(reader.result));
      }
    e.preventDefault();
  };
  /*************************************************************************/
  /*#######################################################################*/

  /*#######################################################################*/
  /*######################### - STUDENT'S LOGIC - #########################*/
  /*#######################################################################*/
  /*********************** - Upload Correction IPFS - **********************/

  /*#######################################################################*/

  /*#######################################################################*/
  /*########################### - PUBLIC LOGIC - ##########################*/
  /*#######################################################################*/
  const handleEnroll = async (event) => {
    event.preventDefault();
    try{
      let hexValue = await smartExamSigner.getEnrollingPrice();
      let weiValue = ethers.utils.parseUnits(parseInt(hexValue).toString(), 'wei')
      const rsp = await smartExamSigner.enroll({value: weiValue});
      console.log("Response to enroll:", rsp);
    } catch (error) {
      console.log(error.message);
    }
  }
  /*#######################################################################*/

  /*#######################################################################*/
  /*########################## - LOGIN'S LOGIC - ##########################*/
  /*#######################################################################*/
  const [showContent, setShowContent] = useState(true);
  const [html, setHtml] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      if (await smartExamSigner.isOwner()){
        return_value = 
          (        
            <div class="form-container">
              <h1>Owner's page</h1>     
              <form id="add-professor" class="inline-form" onSubmit={handleAddProfessor}>
                <h3>Register professor</h3>
                <input type="text" id="texto" name="texto" />
                <button type="submit" className="btn">Register</button>
                {examHash && (
                  <div>
                    <p>{examHash}</p>
                  </div>
                )}
              </form>         
            </div>
          )
        setHtml(return_value)
        setShowContent(false)
      } else if (await smartExamSigner.isProfessor()){
        return_value = (        
            <div>
              <h1>Professor's Page</h1>
              <div class="form-container">
                <form id="get-exams" class="inline-form" onSubmit={handleGetExams}>
                  <h3>Get exams</h3>
                  <button type="submit" className="btn">Get</button>
                  {examHashes && (
                    <div>
                      <p>{examHashes}</p>
                    </div>
                  )}
                </form> 
                <form id="get-corrections" class="inline-form" onSubmit={handleGetCorrections}>
                  <h3>Get corrections</h3>
                  <button type="submit" className="btn">Get</button>
                  {correctionHashes && (
                    <div>
                      <p>{correctionHashes}</p>
                    </div>
                  )}
                </form>        
              </div>
              <div class="form-container">
                <form id="get-student" class="inline-form" onSubmit={handleGetStudent}>
                  <h3>Get student address from exam hash</h3>
                  <input type="text" id="texto" name="texto" />
                  <button type="submit" className="btn">Get</button>
                  {studentAddress && (
                    <div>
                      <p>{studentAddress}</p>
                    </div>
                  )}
                </form> 
                <form id="check-file" class="inline-form" onSubmit={handleDownloadExam}>
                  <h3>Get exam file from student address</h3>
                  <input type="text" id="texto" name="texto" />
                  <button type="submit" className="btn">Get</button>
                </form>
                <div id="imageExamContainer"></div>           
              </div>
              <form id="upload-correction" class="inline-form" onSubmit={handleUploadCorrection}>
                  <h3>Upload correction to IPFS</h3>
                  <p>Set the hash of the exam and select the correction.</p>
                  <input type="text" id="texto" name="texto" />
                  <input type="file" name="data" onChange={retrieveCorrectionFile} />
                  <button type="submit" className="btn">Upload</button>
                  {correctionHash && (
                    <div>
                      <p>{correctionHash}</p>
                    </div>
                  )}
                </form>
                <h1> </h1>
            </div>
          )
        setHtml(return_value)
        setShowContent(false)
      } else if (await smartExamSigner.isStudentEnrolled()) {
        return_value = (        
            <div>
              <h1>Student's Page</h1>
              <div class="form-container">
                <form id="upload-file" class="inline-form" onSubmit={handleSubmit}>
                  <h3>Upload a file to IPFS</h3>
                  <input type="file" name="data" onChange={retrieveFile} />
                  <button type="submit" className="btn">Upload</button>
                  {examHash && (
                    <div>
                      <p>{examHash}</p>
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
              <div class="form-container">
                <form id="get-student" class="inline-form" onSubmit={handleGetStudent}>
                  <h3>Get student from exam</h3>
                  <input type="text" id="texto" name="texto" />
                  <button type="submit" className="btn">Get</button>
                  {studentAddress && (
                    <div>
                      <p>{studentAddress}</p>
                    </div>
                  )}
                </form>
                <form id="check-file" class="inline-form" onSubmit={handleGetExam}>
                  <h3>Get Exam</h3>
                  <input type="text" id="texto" name="texto" />
                  <button type="submit" className="btn">Get</button>
                  {checkText && (
                    <div>
                      <p>{checkText}</p>
                    </div>
                  )}
                </form>
                <div id="imageExamContainer"></div>          
              </div>
            </div>
          )
        setHtml(return_value)
        setShowContent(false)
      } else {
        return_value = 
          (        
            <div class="form-container">
              <h1>Public Page</h1>     
              <form id="enroll" class="inline-form" onSubmit={handleEnroll}>
                <h3>Enroll into exam ({ENROLLING_PRICE})</h3>
                <button type="submit" className="btn">Enroll</button>
              </form>        
            </div>
          )
        setHtml(return_value)
        setShowContent(false)
      }
    } catch (error) {
      console.log(error.message);
    }
  };                                      
  /*#######################################################################*/

  return (
    <div className="App">
      <header className="App-header">

        <img src={logo} className="App-logo" alt="logo" />
        
        {showContent ? (
          <div class="form-container">
            <form id="login-page" class="inline-form" onSubmit={handleLogin}>
              <h3>Login Form </h3>
              <button type="submit" className="btn">Log in</button>
            </form>         
          </div>
        ) : (
          <div>
            {html && (
              <div>
                {html}
              </div>
            )}
          </div>
        )}
        
      </header>
    </div>
  );
}

export default App;
//http://0.0.0.0:5001/ipfs/bafybeibozpulxtpv5nhfa2ue3dcjx23ndh3gwr5vwllk7ptoyfwnfjjr4q/#/files



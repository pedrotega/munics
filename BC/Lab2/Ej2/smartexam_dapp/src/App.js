import React, { useEffect, useState } from "react";
import './App.css';
import { ethers } from "ethers";
import { Buffer } from "buffer";
import logo from "./municsLogo.png";
import { addresses, abis } from "./contracts";
import { downloadFileIPFS, uploadFileIPFS } from "./utilsIPFS";

//import { create } from 'kubo-rpc-client'

const defaultProvider = new ethers.providers.Web3Provider(window.ethereum);

const smartExam = new ethers.Contract(
  addresses.ipfs,
  abis.ipfs,
  defaultProvider
);

const smartExamSigner = smartExam.connect(defaultProvider.getSigner());

let hexValue = await smartExamSigner.getEnrollingPrice();
let price = parseInt(hexValue).toString();
const ENROLLING_PRICE = price + " wei";


function App() {

  // This variable are going to be used to change the html in the web page.
  let return_value;

  useEffect(() => {
    window.ethereum.enable();
  }, []);
  
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
  };
  /*#######################################################################*/

  /*#######################################################################*/
  /*######################## - PROFESSOR'S LOGIC - ########################*/
  /*#######################################################################*/

  /********************** - Get exams from contract - **********************/
  const handleGetExams = async (event) => {
    event.preventDefault();
    try {
      const _examHashes = await smartExamSigner.getExams();
      console.log("Exams:", _examHashes);
      let _examHashesString = "";
      for (let i in _examHashes){
        _examHashesString = _examHashesString + _examHashes[i] + "\n";
      }
      const examHashesContainer = document.getElementById('examHashesContainer');
      examHashesContainer.textContent = _examHashesString;
    } catch (error) {
      console.log(error.message);
    }
  };
  /*************************************************************************/

  /******************** - Get corrections from contract - ******************/
  const handleGetCorrections = async (event) => {
    event.preventDefault();
    try {
      const _correctionHashes = await smartExamSigner.getCorrections();
      console.log("Correction hashes:", _correctionHashes);
      let _correctionHashesContainer = "";
      for (let i in _correctionHashes){
        _correctionHashesContainer = _correctionHashesContainer + _correctionHashes[i] + "\n";
      }
      const correctionHashesContainer = document.getElementById('correctionHashesContainer');
      correctionHashesContainer.textContent = _correctionHashesContainer;
    } catch (error) {
      console.log(error.message);
    }
  };
  /*************************************************************************/

  /******************** - Get student from hash exam - *********************/
  const handleGetStudent = async (event) => {
    event.preventDefault();
    try {
      const _hash = event.target.elements.texto.value;
      const _studentAdd = await smartExamSigner.getStudent(_hash);
      console.log("Student address:",_studentAdd);
      const studentAddressContainer = document.getElementById('studentAddressContainer');
      studentAddressContainer.textContent = _studentAdd;
    } catch (error) {
      console.log(error.message);
    }
  };
  /*************************************************************************/

  /********************** - Download exam from IPFS - **********************/
  const handleDownloadExam = async (event) => {
    event.preventDefault();
    try {
      const cid_exam = event.target.elements.texto.value;
      console.log("Exam hash:",cid_exam);
      downloadFileIPFS(cid_exam, 'imageExamContainer', 'exam');
    } catch (error) {
      console.log(error.message);
    }
  };
  /*************************************************************************/

  /*********************** - Upload Correction IPFS - **********************/
  let correction;

  async function setCorrectionContract(_examHash, _correctionHash) {
    const rsp = await smartExamSigner.setCorrection(_examHash, _correctionHash);
    console.log("Setting correction response:",rsp);
    const correctionHashContainer = document.getElementById('correctionHashContainer');
    correctionHashContainer.textContent = _correctionHash;
  }

  const handleUploadCorrection = async (event) => {
    event.preventDefault();
    try {
      const _examHash = event.target.elements.texto.value;
      console.log("Exam hash:", _examHash);
      const _correctionHash = await uploadFileIPFS(correction);
      console.log("Correction hash:", _correctionHash);
      // Add the correction to IPFS and smart-contract.
      await setCorrectionContract(_examHash, _correctionHash);
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
        correction = Buffer(reader.result);
      }
    e.preventDefault();
  };
  /*************************************************************************/
  /*#######################################################################*/

  /*#######################################################################*/
  /*######################### - STUDENT'S LOGIC - #########################*/
  /*#######################################################################*/

  /******************* - Download correction from IPFS - *******************/
  const handleDownloadMyExam = async (event) => {
    event.preventDefault();
    try {
      const cid_exam = await smartExamSigner.getExam();
      console.log("Correction hash", cid_exam);
      downloadFileIPFS(cid_exam, 'imageMyExamContainer', 'exam');
    } catch (error) {
      console.log(error.message);
    }
  };
  /*************************************************************************/

  /******************* - Download correction from IPFS - *******************/
  const handleDownloadCorrection = async (event) => {
    event.preventDefault();
    try {
      const cid_corr = await smartExamSigner.getCorrection();
      console.log("Correction hash", cid_corr);
      downloadFileIPFS(cid_corr, 'imageMyCorrectionContainer','correction');
    } catch (error) {
      console.log(error.message);
    }
  };
  /*************************************************************************/

  /************************** - Upload Exam IPFS - *************************/
  let exam;

  async function setExam(hash) {
    const rsp = await smartExamSigner.setExam(hash);
    console.log("Set exam response", rsp);
    const correctionHashContainer = document.getElementById('correctionHashContainer');
    correctionHashContainer.textContent = hash;
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Upload file to IPFS
      const cid = await uploadFileIPFS(exam);
      console.log("Exam hash:", cid);
      // Add hash to the smart-contract
      await setExam(cid);
    } catch (error) {
      console.log(error.message);
    }
  };

  const retrieveExamFile = (e) => {
      const data = e.target.files[0];
      const reader = new window.FileReader();
      reader.readAsArrayBuffer(data);
      console.log("data", data);
      reader.onloadend = () => {
        console.log("Buffer data: ", Buffer(reader.result));
        exam = Buffer(reader.result);
      }
      console.log(exam)
    e.preventDefault();
  };
  /*************************************************************************/

  /*#######################################################################*/

  /*#######################################################################*/
  /*########################### - PUBLIC LOGIC - ##########################*/
  /*#######################################################################*/
  const handleEnroll = async (event) => {
    event.preventDefault();
    try{
      let hexValue = await smartExamSigner.getEnrollingPrice();
      let weiValue = ethers.utils.parseUnits(parseInt(hexValue).toString(), 'wei');
      const rsp = await smartExamSigner.enroll({value: weiValue});
      console.log("Response to enroll:", rsp);
    } catch (error) {
      console.log(error.message);
    }
  };
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
              </form>         
            </div>
          );
        setHtml(return_value);
        setShowContent(false);
      } else if (await smartExamSigner.isProfessor()){
        return_value = (        
            <div>
              <h1>Professor's Page</h1>
              <div class="form-container">
                <form id="get-exams" class="inline-form" onSubmit={handleGetExams}>
                  <h3>Get exams</h3>
                  <button type="submit" className="btn">Get</button>
                  <p id="examHashesContainer"></p>
                </form> 
                <form id="get-corrections" class="inline-form" onSubmit={handleGetCorrections}>
                  <h3>Get corrections</h3>
                  <button type="submit" className="btn">Get</button>
                  <p id="correctionHashesContainer"></p>
                </form>        
              </div>
              <div class="form-container">
                <form id="get-student" class="inline-form" onSubmit={handleGetStudent}>
                  <h3>Get student address from exam hash</h3>
                  <input type="text" id="texto" name="texto" />
                  <button type="submit" className="btn">Get</button>
                  <p id="studentAddressContainer"></p>
                </form> 
                <form id="check-file" class="inline-form" onSubmit={handleDownloadExam}>
                  <h3>Get exam file from exam hash</h3>
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
                  <p id="correctionHashContainer"></p>
                </form>
                <h1> </h1>
            </div>
          );
        setHtml(return_value);
        setShowContent(false);
      } else if (await smartExamSigner.isStudentEnrolled()) {
        return_value = (        
            <div>
              <h1>Student's Page</h1>
              <div class="form-container">
                <form id="get-exam" class="inline-form" onSubmit={handleDownloadMyExam}>
                  <h3>Get my exam file</h3>
                  <button type="submit" className="btn">Get</button>
                </form>
                <div id="imageMyExamContainer"></div> 
                <form id="get-correction" class="inline-form" onSubmit={handleDownloadCorrection}>
                  <h3>Get my correction file</h3>
                  <button type="submit" className="btn">Get</button>
                </form>
                <div id="imageMyCorrectionContainer"></div>         
              </div>
              <div class="form-container">
                <form id="upload-file" class="inline-form" onSubmit={handleSubmit}>
                  <h3>Upload a file to IPFS</h3>
                  <input type="file" name="data" onChange={retrieveExamFile} />
                  <button type="submit" className="btn">Upload</button>
                  <p id="examHashContainer"></p>
                </form> 
                <h1> </h1>    
              </div>
            </div>
          );
        setHtml(return_value);
        setShowContent(false);
      } else {
        return_value = (        
            <div class="form-container">
              <h1>Public Page</h1>     
              <form id="enroll" class="inline-form" onSubmit={handleEnroll}>
                <h3>Enroll into exam ({ENROLLING_PRICE})</h3>
                <button type="submit" className="btn">Enroll</button>
              </form>        
            </div>
          );
        setHtml(return_value);
        setShowContent(false);
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



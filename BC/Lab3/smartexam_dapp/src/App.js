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


function App() {

  // This variable are going to be used to change the html in the web page.
  let return_value;

  useEffect(() => {
    window.ethereum.enable();
  }, []);
  
  /*#######################################################################*/
  /*########################## - OWNERS'S LOGIC - #########################*/
  /*#######################################################################*/

  /************************* - Register Professor - ************************/
  const handleRegisterProfessor = async (event) => {
      event.preventDefault();
      try {
          const addProf = event.target.elements.texto.value;
          console.log("Professor address:",addProf);
          const rsp = await smartExamSigner.registerProfessor(addProf);
          console.log("Response register professor:", rsp);
      } catch (error) {
          console.log(error.message);
      }
  };
  /*************************************************************************/

  /************************** - Delete Professor - *************************/
  const handleDeleteProfessor = async (event) => {
      event.preventDefault();
      try {
          const addProf = event.target.elements.texto.value;
          console.log("Professor address:",addProf);
          const rsp = await smartExamSigner.deleteProfessor(addProf);
          console.log("Response delete professor:", rsp);
      } catch (error) {
          console.log(error.message);
      }
  };
  /*************************************************************************/

  /************************ - Edit exam parameters - ***********************/
  const handleEditExam = async (event) => {
      event.preventDefault();
      try {
          const enrollingPrice = event.target.elements.price.value;
          console.log("Enrolling price:",enrollingPrice);
          const duration = event.target.elements.duration.value;
          console.log("Duration:",duration)
          const dateString = event.target.elements.datetime.value;
          const date = new Date(dateString)
          const unixDate = date.getTime() /1000 // Convert from miliseconds to seconds.
          console.log("Date:",unixDate)
          const rsp = await smartExamSigner.editExamParameters(unixDate, duration, enrollingPrice);
          console.log("Response edit exam:", rsp);
      } catch (error) {
          console.log(error.message);
      }
  };
  /*************************************************************************/

  /*********************** - Upload Statement IPFS - **********************/
  let statement;

  async function setStatementContract(_statementHash) {
    const rsp = await smartExamSigner.startExam( _statementHash);
    console.log("Setting statement response:",rsp);
    const statementHashContainer = document.getElementById('statementHashContainer');
    statementHashContainer.textContent = _statementHash;
  }

  const handleUploadStatement = async (event) => {
    event.preventDefault();
    try {
      const _statementHash = await uploadFileIPFS(statement);
      console.log("Statement hash:", _statementHash);
      // Add the statement to IPFS and smart-contract.
      await setStatementContract(_statementHash);
    } catch (error) {
      console.log(error.message);
    }
  };

  const retrieveStatementFile = (e) => {
      const data = e.target.files[0];
      const reader = new window.FileReader();
      reader.readAsArrayBuffer(data);
      console.log(data);
      reader.onloadend = () => {
        console.log("Buffer data: ", Buffer(reader.result));
        statement = Buffer(reader.result);
      }
    e.preventDefault();
  };
  /*************************************************************************/

  /******************* - Download statement from IPFS - *******************/
  const handleDownloadStatement = async (event) => {
    event.preventDefault();
    try {
      const cid_statement = await smartExamSigner.getStatement();
      console.log("Statement hash", cid_statement);
      downloadFileIPFS(cid_statement, 'imageStatementContainer', 'statement');
    } catch (error) {
      console.log(error.message);
    }
  };
  /*************************************************************************/

  /********************* - Check certificate student - *********************/
  const handleCertificate = async (event) => {
    event.preventDefault();
    try {
      const certificateContainer = document.getElementById('certificateContainer');
      certificateContainer.textContent = "No results";
      const studAdd = event.target.elements.studAdd.value;
      const cert = await smartExamSigner.certificateStudent(studAdd);
      console.log("Certification:", );
      if(cert) {
        certificateContainer.textContent = "Student has the certificate";
      } else {
        certificateContainer.textContent = "Student has NOT the certificate";
      }
      
    } catch (error) {
      console.log(error.message);
    }
  };
  /*************************************************************************/

  /****************************** - Widthdraw - ****************************/
  const handleWithdraw = async (event) => {
    event.preventDefault();
    try {
        const rsp = await smartExamSigner.withdraw();
        console.log("Response withdraw:", rsp);
    } catch (error) {
        console.log(error.message);
    }
};
/*************************************************************************/
  
  /*#######################################################################*/

  /*#######################################################################*/
  /*######################## - PROFESSOR'S LOGIC - ########################*/
  /*#######################################################################*/

  /******************** - Get students from contract - ******************/
  const handleGetStudents = async (event) => {
    event.preventDefault();
    try {
      const _students = await smartExamSigner.getStudents();
      console.log("Students addresses:", _students);
      let _studentsContainer = "";
      for (let i in _students){
        _studentsContainer = _studentsContainer + _students[i] + "\n";
      }
      const studentsContainer = document.getElementById('studentsContainer');
      studentsContainer.textContent = _studentsContainer;
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

  /******************* - Download submission from IPFS - *******************/
  const handleDownloadSubmission = async (event) => {
    event.preventDefault();
    try {
      const studAdd = event.target.elements.texto.value;
      const submission_cid = await smartExamSigner.getStudentSubmission(studAdd);
      console.log("Submission CID:",submission_cid);
      downloadFileIPFS(submission_cid, 'imageSubmissionContainer', 'submission');
    } catch (error) {
      console.log(error.message);
    }
  };
  /*************************************************************************/

  /*********************** - Upload Correction IPFS - **********************/
  let correction;

  async function setCorrectionContract(_studAdd, _correctionHash, _score) {
    const rsp = await smartExamSigner.setCorrection(_studAdd, _correctionHash, _score);
    console.log("Setting correction response:",rsp);
    const correctionHashContainer = document.getElementById('correctionHashContainer');
    correctionHashContainer.textContent = _correctionHash;
  }

  const handleUploadCorrection = async (event) => {
    event.preventDefault();
    try {
      const _studAdd = event.target.elements.studAdd.value;
      const _score = event.target.elements.score.value;
      console.log("Student address:", _studAdd);
      console.log("Score:", _score);
      const _correctionHash = await uploadFileIPFS(correction);
      console.log("Correction hash:", _correctionHash);
      // Add the correction to IPFS and smart-contract.
      await setCorrectionContract(_studAdd, _correctionHash, _score);
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

  /********************* - Download my exam from IPFS - ********************/
  const handleDownloadMyExam = async (event) => {
    event.preventDefault();
    try {
      const cid_exam = await smartExamSigner.getMyExam();
      console.log("Correction hash", cid_exam);
      downloadFileIPFS(cid_exam, 'imageMyExamContainer', 'exam');
    } catch (error) {
      console.log(error.message);
    }
  };
  /*************************************************************************/
  
  /******************* - Download Correction from IPFS - *******************/
  const handleDownloadCorrection = async (event) => {
    event.preventDefault();
    try {
      const cid_corr = await smartExamSigner.getMyCorrection();
      console.log("Correction hash", cid_corr);
      downloadFileIPFS(cid_corr, 'imageMyCorrectionContainer','correction');
    } catch (error) {
      console.log(error.message);
    }
  };
  /*************************************************************************/

  /**************************** - Get My Score - ***************************/
  const handleGetScore = async (event) => {
    event.preventDefault();
    try {
      const _score = await smartExamSigner.getMyScore();
      console.log("Score", _score);
      const scoreContainer = document.getElementById('scoreContainer');
      scoreContainer.textContent = "Score: " + _score;
    } catch (error) {
      console.log(error.message);
    }
  };
  /*************************************************************************/

  /************************** - Upload Exam IPFS - *************************/
  let exam;

  async function setExam(hash) {
    const rsp = await smartExamSigner.setSubmission(hash);
    console.log("Set exam response", rsp);
    const examHashContainer = document.getElementById('examHashContainer');
    examHashContainer.textContent = hash;
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
      let hexValue = await smartExamSigner.enrollingPrice();
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

    const hexPrice = await smartExamSigner.enrollingPrice();
    const price = parseInt(hexPrice).toString();
    const ENROLLING_PRICE = price + " wei";

    const hexDuration = await smartExamSigner.enrollingPrice();
    const duration = parseInt(hexDuration).toString();
    const DURATION = "Duration: " + duration + " mins";

    let dateLastUpload = await smartExamSigner.dateLastUpload();
    let timestampLastUpload = new Date(dateLastUpload*1000);
    const LAST_UPLOAD = "Last update: " + timestampLastUpload.toLocaleString(); 

    let dateExam = await smartExamSigner.dateExam();
    let timestampExam = new Date(dateExam*1000);
    const DATE_EXAM = "Date exam: " + timestampExam.toLocaleString(); 

    const INFO_EXAM = (
      <form id="info-exam" class="inline-form">
        <h3>Exam information:</h3>
        <h4>{LAST_UPLOAD}</h4>
        <h4>{DATE_EXAM}</h4>
        <h4>Enrolling price: {ENROLLING_PRICE}</h4>
        <h4>{DURATION}</h4>
      </form>
    )

    try {
      if (await smartExamSigner.isOwner()){
        return_value = 
          (        
            <div class="form-container">
                <h1>Owner's page</h1>
                {INFO_EXAM}
                <div class="form-container">
                    <form id="add-professor" class="inline-form" onSubmit={handleRegisterProfessor}>
                        <h3>Register professor</h3>
                        <input type="text" id="texto" name="texto" />
                        <br/>
                        <button type="submit" className="btn">Register</button>
                    </form>
                    <form id="delete-professor" class="inline-form" onSubmit={handleDeleteProfessor}>
                        <h3>Unregister professor</h3>
                        <input type="text" id="texto" name="texto" /><br/>
                        <button type="submit" className="btn">Unregister</button>
                    </form>
                </div>
                <div class="form-container">
                  <form id="edit-exam" class="inline-form" onSubmit={handleEditExam}>
                      <h3>Edit exam</h3>
                      <label for="number">Enrolling price (wei):</label>
                      <input type="number" id="price" name="price" required />
                      <label for="number">Duration (mins):</label>
                      <input type="number" id="duration" name="duration" required />
                      <br/>
                      <label for="datetime">Date:</label>
                      <input type="datetime-local" id="datetime" name="datetime" required /> 
                      <br/>
                      <button type="submit" className="btn">Edit</button>
                  </form>
                  <form id="upload-statement" class="inline-form" onSubmit={handleUploadStatement}>
                    <h3>Start exam</h3>
                    <label for="text">Select exam:</label>
                    <input type="file" name="data" onChange={retrieveStatementFile} />
                    <br/>
                    <button type="submit" className="btn">Upload</button>
                    <p id="statementHashContainer"></p>
                  </form>
                </div>
                <div class="form-container">
                  <form id="download-statement" class="inline-form" onSubmit={handleDownloadStatement}>
                    <h3>Get statement file from  CID</h3>
                    <button type="submit" className="btn">Get</button>
                  </form>
                  <div id="imageStatementContainer"></div> 

                  <form id="withdraw" class="inline-form" onSubmit={handleWithdraw}>
                      <h3>Withdraw revenue</h3>
                      <button type="submit" className="btn">Withdraw</button>
                  </form>
                </div>
                <form id="certificate-student" class="inline-form" onSubmit={handleCertificate}>
                    <h3>Check if student has the certificate</h3>
                    <label for="text">Student address:</label>
                    <input type="text" id="studAdd" name="studAdd"></input><br/>
                    <button type="submit" className="btn">Get</button>
                    <p id="certificateContainer"></p>
                  </form>  
                <h1> </h1>
            </div>
          );
      } else if (await smartExamSigner.isProfessor()){
        return_value = (        
            <div>
              <h1>Professor's Page</h1>
              {INFO_EXAM}
              <div class="form-container">
                <form id="get-students" class="inline-form" onSubmit={handleGetStudents}>
                  <h3>Get enrolled students</h3>
                  <button type="submit" className="btn">Get</button><br/>
                  <p id="studentsContainer"></p>
                </form>  
                <form id="get-corrections" class="inline-form" onSubmit={handleGetCorrections}>
                  <h3>Get corrections</h3>
                  <button type="submit" className="btn">Get</button><br/>
                  <p id="correctionHashesContainer"></p>
                </form>        
              </div>
              <div class="form-container">
                <form id="download-submission" class="inline-form" onSubmit={handleDownloadSubmission}>
                  <h3>Get submission from student address</h3>
                  <input type="text" id="texto" name="texto" /><br/>
                  <button type="submit" className="btn">Get</button>
                </form>
                <div id="imageSubmissionContainer"></div>     
                <form id="upload-correction" class="inline-form" onSubmit={handleUploadCorrection}>
                  <h3>Upload correction to IPFS</h3>
                  <label for="text">Student address:</label>
                  <input type="text" id="studAdd" name="studAdd" /><br/>
                  <label for="number">Score:</label>
                  <input type="number" id="score" name="score" /><br/>
                  <label for="file">Set correction:</label>
                  <input type="file" name="data" onChange={retrieveCorrectionFile} />
                  <button type="submit" className="btn">Upload</button>
                  <p id="correctionHashContainer"></p>
                </form>      
              </div>
                <h1> </h1>
            </div>
          );
      } else if (await smartExamSigner.isStudentEnrolled()) {
        return_value = (        
            <div>
              <h1>Student's Page</h1>
              {INFO_EXAM}
              <h1> </h1>
              <form id="download-statement" class="inline-form" onSubmit={handleDownloadStatement}>
                    <h3>Get statement file</h3>
                    <button type="submit" className="btn">Get</button>
                  </form>
                  <div id="imageStatementContainer"></div> 
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
                  <h3>Upload submission to IPFS</h3>
                  <input type="file" name="data" onChange={retrieveExamFile} />
                  <button type="submit" className="btn">Upload</button>
                  <p id="examHashContainer"></p>
                </form> 
                <form id="get-score" class="inline-form" onSubmit={handleGetScore}>
                  <h3>Get My Score</h3>
                  <button type="submit" className="btn">Get</button>
                  <p id="scoreContainer"></p>
                </form>                 
                <h1> </h1>    
              </div>
            </div>
          );
      } else {
        return_value = (        
            <div class="form-container">
            <h1>Public Page</h1>   
              {INFO_EXAM}  
              <h1> </h1>
              <form id="enroll" class="inline-form" onSubmit={handleEnroll}>
                <h3>Enroll into exam ({ENROLLING_PRICE})</h3>
                <button type="submit" className="btn">Enroll</button>
              </form> 
              <h1> </h1>       
            </div>
          );
      }
      setHtml(return_value);
      setShowContent(false);
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



// SPDX-License-Identifier: MIT.
pragma solidity 0.8.20;

import "./SmartExamBase.sol";

contract SmartExam is SmartExamBase{

    /********************************************************************
    /************************ - PROFESSOR - *****************************
    /********************************************************************/

    // Function used by professors to create exams.
    function createExam(
        string memory _course,
        string memory _hash,
        uint _dateExam,
        uint _duration,
        uint _enrollingPrice
    ) external onlyProfessor {
        Exam memory e = Exam(_course, countExam, _hash, "null", 
                            block.timestamp, _dateExam, _dateExam, _duration, _enrollingPrice);
        exams.push(e);
        countExam++;
    }

    // Function used by professors to create exams.
    function modifyExam(
        string memory _course,
        uint _examId,
        string memory _hash,
        uint _dateExam,
        uint _duration,
        uint _enrollingPrice
    ) external onlyProfessor {
        require(exams.length > _examId, "Exam does not exist.");
        require((block.timestamp < exams[_examId].dateExam) || 
            (keccak256(bytes(exams[_examId].url)) == keccak256(bytes("null"))), 
            "Exam cannot be modified.");
        Exam memory e = Exam(_course, _examId, _hash, "null", 
                            block.timestamp, _dateExam, _dateExam, _duration, _enrollingPrice);
        exams[_examId] = e;
    }

    // Function used by professors to start an exam. Once an exam starts, it is no longer modifiable.
    function startExam(uint _examId, string memory _url) external onlyProfessor {
        require(exams.length > _examId, "Exam does not exist.");
        require((keccak256(bytes(exams[_examId].url)) == keccak256(bytes("null"))), "Exam has already started.");
        require(block.timestamp >= exams[_examId].dateExam, "Cannot start a exam before the dateExam.");
        exams[_examId].url = _url;
        exams[_examId].dateStartExam = block.timestamp;
    }

    // Getter used to know the students whe submited an exam.
    function getSubmissions(uint _examId) external view onlyProfessor returns(address[] memory){
        require(exams.length > _examId, "Exam does not exist.");
        return examsSubmited[_examId];
    }   

    // Getter used to access to the information of a particular exam.
    function getExamSubmited(address _studAdd, uint _examId) external view onlyProfessor returns(string memory, string memory){
        require(exams.length > _examId, "Exam does not exist.");
        ExamStudent memory es = students[_studAdd].exams_done[_examId];
        require(es.studentAdd == msg.sender, "Student didn't submit this exam.");
        return (es.hash_submission, es.url_exam_submited);
    }

    // Function used to the professors to link the assesment to the exam of an student.
    function addCorrection(address _studAdd, uint _examId, string memory _hash_correction, 
                        string memory _url_exam_correction, uint _score) external {
        require(exams.length > _examId, "Exam does not exist.");
        ExamStudent memory es = students[_studAdd].exams_done[_examId];
        require(es.studentAdd == msg.sender, "Student didn't submit this exam.");
        require((keccak256(bytes(es.hash_correction)) == keccak256(bytes("null"))), "Exam was already corrected.");
        students[_studAdd].exams_done[_examId].hash_correction = _hash_correction;
        students[_studAdd].exams_done[_examId].url_exam_correction = _url_exam_correction;
        students[_studAdd].exams_done[_examId].score = _score;
    }

    /********************************************************************
    /************************ - STUDENT - *******************************
    /********************************************************************/

    // Getter ro reach the data of an exam. It has no view restrictions.
    function getExam(uint _examId) external view 
    returns(
        string memory, uint, string memory, string memory, 
        uint, uint, uint, uint, uint
    ){
        Exam memory e = exams[_examId];
        return (e.course, e.id, e.hash, e.url, e.dateLastUpload, e.dateExam,
                e.dateStartExam, e.duration, e.enrollingPrice);
    }

    // Function used to enroll into an exam.
    // We make this function payable because there are exams where you have to pay for taxes.
    function enrollIntoExam(uint _examId) external payable {
        // If a student doesn't pay the exact amount of wei to enroll in the exam, they cannot enroll into the exam.
        // We assume that is not their fault and we use the revert operation.
        if(msg.value != exams[_examId].enrollingPrice*1 wei){
            revert("Pay the exact price of enrolling in wei.");
        }
        if(exams[_examId].dateStartExam<block.timestamp){
            revert("The deadline to enroll into the exam is over.");
        }
        if(students[msg.sender].add != address(0)){
            // If student exists, we check if is not enroll in the exam an we enroll it.
            if(students[msg.sender].exams_enrolled[_examId]){
                // We assume that is not the fault of the student enroll twice in a exam.
                revert("You are already enrolled in the exam.");
            } else{
                students[msg.sender].exams_enrolled[_examId] = true;
            }
            
        } else{ 
            // If student doesn't exist we create a new one
            Student storage newStudent = students[msg.sender];
            newStudent.add = msg.sender;
            newStudent.exams_enrolled[_examId] = true;
        }
    }

    // Function used by an enrolled student to submit his/her answers file.
    function submitExam(
        uint _examId,
        string memory _hash,
        string memory _url_exam_submited
    ) external onlyStudent {
        require(exams.length>_examId, "Exam does not exist.");
        Exam memory e = exams[_examId];
        require(keccak256(abi.encodePacked(e.url)) != keccak256(abi.encodePacked("null")), "Exam has not started yet.");
        require(block.timestamp < e.dateStartExam + e.duration*60, "The exam is over, no submissions accepted.");
        require(students[msg.sender].exams_done[_examId].studentAdd == address(0), "You has already sumbited the exam.");
        ExamStudent memory es = ExamStudent(msg.sender, e, _hash, _url_exam_submited, "null", "null", 0);
        students[msg.sender].exams_done[_examId] = es;
        examsSubmited[_examId].push(msg.sender);
    } 

    // Function used by the students to view the corrections of his/her exam.
    function checkCorrection(uint _examId) external view returns(string memory, string memory, uint) {
        require(exams.length>_examId, "Exam does not exist.");
        ExamStudent memory es = students[msg.sender].exams_done[_examId];
        require(es.studentAdd == msg.sender, "Student didn't submit this exam.");
        require((keccak256(bytes(es.hash_correction)) != keccak256(bytes("null"))), "Exam was not corrected yet.");
        return (es.hash_correction, es.url_exam_correction, es.score);
    }
}
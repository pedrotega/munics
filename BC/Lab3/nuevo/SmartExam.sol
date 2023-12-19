// SPDX-License-Identifier: MIT.
pragma solidity 0.8.20;

import "./SmartExamBase.sol";

contract SmartExam is SmartExamBase{

    /********************************************************************
    /************************ - PROFESSOR - *****************************
    /********************************************************************/

    // 'setStatement' let a professor upload the statement of the exam.
    function setStatement(
        string memory _statement        
    ) external onlyProfessor {
        statement = _statement;
        dateLastUpload = block.timestamp;
    }

    // 'getStudents' let a professor to obtain the address of the enrolled students.
    function getStudents() external view onlyProfessor returns (string[] memory) {
        return _studAdds;
    }

    // 'getStudentExam' let a professor to obtain the CID exam of a student
    // from his/her address.
    function getStudentExam(
        address _studAdd
    ) external view onlyProfessor checkSubmission(_studAdd) returns (string memory) {      
        return _students[_studAdd].submission;
    }

    // 'setCorrection' let a professor add a correction for an exam.
    function setCorrection(
        address _studAdd, 
        string memory _correction, 
        uint _score
    ) external onlyProfessor checkSubmission(_studAdd) {
        _students[_studAdd].correction = _correction;
        _students[_studAdd].score = _score;
        _correctionCIDs.push(_correction);
    }

    // 'getCorrections' let a professor to obtain all the corrections.
    function getCorrections() external view onlyProfessor returns (string[] memory) {
        return _correctionCIDs;
    }    

    /********************************************************************
    /************************ - STUDENT - *******************************
    /********************************************************************/

    // 'enroll' allows an address to enroll into an exam.
    function enroll() external payable {
        require(msg.value == enrollingPrice, "Pay the exact amount of money.");
        _students.hola
        _studentsEnrolled.push(msg.sender);
    }

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
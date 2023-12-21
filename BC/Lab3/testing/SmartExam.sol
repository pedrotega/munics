// SPDX-License-Identifier: MIT.
pragma solidity 0.8.20;

import "./SmartExamBase.sol";

contract SmartExam is SmartExamBase{

    /********************************************************************
    /************************ - PROFESSOR - *****************************
    /********************************************************************/

    // 'setStatement' let a professor upload the statement of the exam.
    // function setStatement(
    //     string memory _statement        
    // ) external onlyProfessor {
    //     statement = _statement;
    //     dateLastUpload = block.timestamp;
    // }

    // 'getStudents' let a professor to obtain the address of the enrolled students.
    function getStudents() external view onlyProfessor returns (address[] memory) {
        return _studAdds;
    }

    // 'getStudentSubmission' let a professor to obtain the submission CID of a student
    // from his/her address.
    function getStudentSubmission(
        address _studAdd
    ) external view onlyProfessor checkStudent(_studAdd) checkSubmission(_studAdd) returns (string memory) {      
        return _students[_studAdd].submission;
    }

    // 'setCorrection' let a professor add a correction for an exam.
    function setCorrection(
        address _studAdd, 
        string memory _correction, 
        uint8 _score
    ) external onlyProfessor checkStudent(_studAdd) checkSubmission(_studAdd) {
        require((_score >= 0) && (_score <= 10), "The score have to be between 0 and 10");
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
        require(msg.value == enrollingPrice*1 wei, "Pay the exact amount of money.");
        Student memory s = Student("null", "null", 0);
        _students[msg.sender] = s;
        _studAdds.push(msg.sender);
    }


    // 'setSubmission' let a student stores its submission CID.  
    function setSubmission(
        string memory _submission
    ) external checkStudent(msg.sender) checkNOTSubmission(msg.sender) {
        bytes32 sub_bytes = keccak256(bytes(statement));        
        require(sub_bytes != keccak256(bytes("null")), "Exam is not available yet.");
        require(block.timestamp <= dateStartExam + duration*60, "ERROR: Submission out of date.");
        _students[msg.sender].submission = _submission;
    }

    // 'getMySubmission' getter to reach the submission CID of the student that 
    // is calling the funciton.
    function getMyExam() external view returns(string memory) {
        return _students[msg.sender].submission;
    }

    // 'getMyCorrection' getter to reach the correction CID of the student that 
    // is calling the funciton.
    function getMyCorrection() external view returns(string memory) {
        return _students[msg.sender].correction;
    }

    // 'getMyScore' getter to reach the score of the student that 
    // is calling the funciton.
    function getMyScore() external view returns(uint8) {
        return _students[msg.sender].score;
    }

    // 'certificateStudent' getter to confirm that a student pass or not.
    function certificateStudent() external view checkSubmission(msg.sender) returns(bool) {
        return (_students[msg.sender].score >= 5);
    }
}
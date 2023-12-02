// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";

contract SmartExam is Ownable {

    // The owner is the one who creates the contract.
    constructor() Ownable(msg.sender){}

    // Price that cost enroll into the exam.
    uint private constant _ENROLLING_PRICE = 1 wei;

    // '_professor' store the addresses of all professors.
    address[] private _professors;

    // '_students' store the addressed of the students that enroll into a exam.
    address[] private _studentsEnrolled;

    mapping (string => address) private _submissions; // key -> exam hash, value -> student address.

    mapping (address => string) private _exams; // key -> student address, value -> exam hash.
    string[] private _examHashes; // Store exam hashes.

    mapping (string => string) private _corrections; // key -> exam hash, value -> correction hash.
    string[] private _correctionHashes; // Store correction hashes.

    // Check if an address matches with a professor address.
    modifier checkSubmission(string memory _exam) {
        if (msg.sender != _submissions[_exam] && _submissions[_exam] != address(0)){
            revert("You cannot copy!");
        }
        require(_submissions[_exam] == address(0), "Exam already submitted.");
        _;
    }


    // Check if an address is in array _professors.
    modifier checkAddress(address _add, bool _in, bool _prof) {
        /*
            A function that call 'checkProfessor' with '_in == True' want to be sure
            that '_add' is in a array ('_professors' or '_studentsEnrolled') and viceversa.

            We check '_professors' if 'prof == true' and '_sudentsEnrolled' if 'prof == false'. 
        */
        address[] memory _adds;
        if (_prof == true) {
            _adds = _professors;
        } else {
            _adds = _studentsEnrolled;
        }

        bool _isIn = false;
        for (uint i = 0; i < _adds.length; i++) {
            if (_adds[i] == _add) {
                _isIn = true;
                // This is a trick because 'break' does not exist in solidity.
                i = _adds.length;
            }
        }

        // The address is wanted to be into the array but is not. 
        if ((_in) && !(_isIn)) {
            revert("Address is not registered.");
        // The address is wanted to not be into the array but is in.
        } else if (!(_in) && (_isIn)){
            revert("Address is alredy registered.");
        }
        _;
    }

    
    // 'addProfessor' allows admin to add the address of professor to the
    //  array _professors.
    function registerProfessor(address _addProf) external onlyOwner checkAddress(_addProf, false, true) {
        _professors.push(_addProf);
    }

    // 'enroll' allows an address to enroll into an exam.
    function enroll() external payable checkAddress(msg.sender, false, false) {
        require(msg.value == _ENROLLING_PRICE, "Pay the exact amount of money.");
        _studentsEnrolled.push(msg.sender);
    }

    // 'setExamIPFS' let an student submit its exam.  
    function setExam(string memory _exam) external checkAddress(msg.sender, true, false) checkSubmission(_exam) {
        _submissions[_exam] = msg.sender;
        _exams[msg.sender] = _exam;
        _examHashes.push(_exam);
    }

    // 'setCorrection' let a professor add a correction for an exam.
    function setCorrection(string memory _exam, string memory _correction) external checkAddress(msg.sender, true, true) {
        require(_submissions[_exam] != address(0), "Exam does not exist.");
        require(bytes(_corrections[_exam]).length == 0, "Exam was already corrected");
        _corrections[_exam] = _correction;
        _correctionHashes.push(_correction);
    }

    // 'getStudent' let a professor to obtain a student address from an exam hash.
    function getStudent(string memory _exam) external view 
            checkAddress(msg.sender, true, true) returns (address) {
        return _submissions[_exam];
    }

    // 'getCorrections' let a professor to obtain all the corrections.
    function getCorrections() external view
            checkAddress(msg.sender, true, true) returns (string[] memory) {
        return _correctionHashes;
    }

    // 'getCorrection' let a student to get the correction of his/her exam.
    function getCorrection() external view 
            checkAddress(msg.sender, true, false) returns (string memory) {
        string memory exam = _exams[msg.sender];
        require(bytes(exam).length > 0, "You did not submit the exam.");
        string memory correction = _corrections[exam];
        require(bytes(correction).length > 0, "Your exam was not corrected yet.");

        return correction;
    }

    // 'getExams' let a professor to obtain all the exams.
    function getExams() external view checkAddress(msg.sender, true, true) returns (string[] memory) {
        return _examHashes;
    }

    // 'getExam' let a student to obtain its own exam.
    function getExam() external view checkAddress(msg.sender, true, false) returns (string memory) {
        string memory exam = _exams[msg.sender];
        require(bytes(exam).length > 0, "You did not submit the exam.");
        return exam;
    }

    // 'getEnrollingPrice' let anyone to obtain the enrolling price.
    function getEnrollingPrice() pure external returns(uint){
        return _ENROLLING_PRICE;
    }

    // 'isOwner' check if sender is the owner.
    function isOwner() view external returns(bool){
        return msg.sender == owner();
    }

    // 'isProfessor' check if sender is a professor.
    function isProfessor() view external returns(bool){
        for (uint i = 0; i < _professors.length; i++) {
            if (_professors[i] == msg.sender) {
                return true;
            }
        }
        return false;
    }

    // 'isStudentEnrolled' check if sender is a student enrolled.
    function isStudentEnrolled() view external returns(bool){
        for (uint i = 0; i < _studentsEnrolled.length; i++) {
            if (_studentsEnrolled[i] == msg.sender) {
                return true;
            }
        }
        return false;
    }
}


// SPDX-License-Identifier: MIT.
pragma solidity 0.8.20;

import "./Ownable.sol";


contract SmartExamBase is Ownable {

    // The owner is the one who creates the contract.
    constructor() Ownable(msg.sender){}

    /********************* - Parameters Exam - **************************/
    // Hash of the real exam file (to avoid tamper).
    string internal statement = "null";
    // Date of the latest the statement was uploaded.
    uint public dateLastUpload = block.timestamp;
    // Exact date when the exam should take place.
    uint public dateExam = block.timestamp;
    // Real date when the exam started.
    uint public dateStartExam = block.timestamp;
    // Duration of the exam in minutes.
    uint8 public duration = 0;
    // Price to enroll into the exam.
    uint24 public enrollingPrice = 0 wei;

    struct Student {
        /**
        * exams_enrolled: Mapping to know the exams that the student have been enrolled.
        * exams_done: Mapping to get the exams done by the student.
        */
        string submission;
        string correction;
        uint8 score;
    }

    // '_professors' stores the addresses of the professors added by the owner.
    mapping(address => bool) private _professors;
    // '_students' maps the addresses of the students with his/her struct information.
    mapping(address => Student) internal _students;
    // '_studAdds' array that store the addresses of the students.
    address[] internal _studAdds;
    // '_examCIDs' stores the CIDs of the exams.
    string[] internal _examCIDs; 
    // '_correctionCIDs' stores the CIDs of the corrections.
    string[] internal _correctionCIDs; 

    // Check if an address matchs with a professor address.
    modifier onlyProfessor() {
        require(_professors[msg.sender] == true, "Only professors can access to this function.");
        _;
    }

    // Check if the student exists.
    modifier checkStudent(address _studAdd) {
        bytes32 sub_bytes = keccak256(bytes(_students[_studAdd].submission));        
        require(sub_bytes != keccak256(bytes("")), "Student is not erolled.");
        _;
    }

    // Requires a submission to exist.
    modifier checkSubmission(address _studAdd) {
        bytes32 sub_bytes = keccak256(bytes(_students[_studAdd].submission));        
        require(sub_bytes != keccak256(bytes("null")), "Submission does not exist.");
        _;
    }

    // Requires a submission to NOT exist.
    modifier checkNOTSubmission(address _studAdd) {
        bytes32 sub_bytes = keccak256(bytes(_students[_studAdd].submission));        
        require(sub_bytes == keccak256(bytes("null")), "Submission already exists.");
        _;
    }

    // 'isOwner' check if sender is the owner.
    function isOwner() public view returns(bool){
        return msg.sender == owner();
    }

    // 'isProfessor' check if sender is a professor.
    function isProfessor() public view returns(bool){
        return _professors[msg.sender];
    }

    // 'isStudentEnrolled' check if sender is a student enrolled.
    function isStudentEnrolled() public view returns(bool){
        bytes32 sub_bytes = keccak256(bytes(_students[msg.sender].submission));        
        return (sub_bytes != keccak256(bytes("")));
    }

    /********************************************************************
    /************************ - OWNER (EC) - ****************************
    /********************************************************************/

    // 'registerProfessor' function used by the owner to add professors addresses.
    function registerProfessor(address _profAdd) external onlyOwner {
        //We use the revert instead of require because it rollup the state of the contract and it does not use gas.
        require(_professors[_profAdd] == false, "Professor already added.");
        _professors[_profAdd] = true;
    } 

    // 'deleteProfessor' function used by the owner to add professor addresses.
    function deleteProfessor(address _profAdd) external onlyOwner {
        require(_professors[_profAdd] == true, "Professor does not exist.");
        _professors[_profAdd] = false;
    } 

    // 'editExamParameters' function used by owner to set and edit exams.
    function editExamParameters(
        uint _dateExam,
        uint8 _duration,
        uint24 _enrollingPrice
    ) external onlyOwner {
        dateExam = _dateExam;
        dateStartExam = _dateExam;
        duration = _duration;
        enrollingPrice = _enrollingPrice*1 wei;
        dateLastUpload = block.timestamp;
    }

    // 'startExam' unction used by the owner to start the exam adding the CID of the exam.
    function startExam(
        string memory _statement
    ) external onlyOwner {
        bytes32 sub_bytes = keccak256(bytes(statement));        
        require(sub_bytes == keccak256(bytes("null")), "Exam already started.");
        require(block.timestamp >= dateExam, "Cannot start a exam before the dateExam.");
        statement = _statement;
        dateStartExam = block.timestamp;
    }

    // 'withdraw' function used by the owner to get the ether stored in the contract address
    // from the students enrolling payments.
    function withdraw() external onlyOwner {
        payable(owner()).transfer(address(this).balance);
    }

    // 'getStatement' allows owner, professors and students to get statement CID.
    function getStatement() external view returns(string memory){
        require(isOwner() || isProfessor() || isStudentEnrolled() == true, "You cannot access to the statement");
        return statement;
    }
}
// SPDX-License-Identifier: MIT.
pragma solidity 0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";


contract SmartExamBase is Ownable {

    // The owner is the one who creates the contract.
    constructor() Ownable(msg.sender){}

    /********************* - Parameters Exam - **************************/
    // Hash of the real exam file (to avoid tamper).
    string public statement = "";
    // Date of the latest the statement was uploaded.
    uint public dateLastUpload = block.timestamp;
    // Exact date when the exam should take place.
    uint public dateExam = block.timestamp;
    // Real date when the exam started.
    uint public dateStartExam = block.timestamp;
    // Duration of the exam in minutes.
    uint public duration = 0;
    // Price to enroll into the exam.
    uint public enrollingPrice = 0;

    struct Student {
        /**
        * exams_enrolled: Mapping to know the exams that the student have been enrolled.
        * exams_done: Mapping to get the exams done by the student.
        */
        string submission;
        string correction;
        uint score;
    }

    // '_professors' stores the addresses of the professors added by the owner.
    mapping(address => bool) private _professors;
    // '_students' maps the addresses of the students with his/her struct information.
    mapping(address => Student) internal _students;
    // '_studAdds' array that store the addresses of the students.
    string[] internal _studAdds;
    // '_examCIDs' stores the CIDs of the exams.
    string[] internal _examCIDs; 
    // '_correctionCIDs' stores the CIDs of the corrections.
    string[] internal _correctionCIDs; 

    // Check if an address matchs with a professor address.
    modifier onlyProfessor() {
        require(_professors[msg.sender] == true, "Only professors can access to this function.");
        _;
    }

    // Check if an address matchs with a student address.
    modifier onlyStudent() {
        require(_students[msg.sender].score != 0, "Only students enrrolled can access to this function.");
        _;
    }

    // Check if a submission exists.
    modifier checkSubmission(address _studAdd) {
        bytes32 sub_bytes = keccak256(bytes(_students[_studAdd].submission));        
        require(sub_bytes != keccak256(bytes("")), "Submission does not exists");
        _;
    }

    /********************************************************************
    /************************ - OWNER (EC) - ****************************
    /********************************************************************/

    // Function used by the owner to add professors addresses.
    function registerProfessor(address _profAdd) external onlyOwner {
        //We use the revert instead of require because it rollup the state of the contract and it does not use gas.
        require(_professors[_profAdd] == false, "Professor already added.");
        _professors[_profAdd] = true;
    } 

    // Function used by the owner to add professor addresses.
    function deleteProfessor(address _profAdd) external onlyOwner {
        require(_professors[_profAdd] == true, "Professor does not exist.");
        _professors[_profAdd] = false;
    } 

    // Function used by owner to set and edit exams.
    function editExamParameters(
        uint _dateExam,
        uint _duration,
        uint _enrollingPrice
    ) external onlyOwner {
        dateExam = _dateExam;
        duration = _duration;
        enrollingPrice = _enrollingPrice;
        dateLastUpload = block.timestamp;
    }

    // Function used by the owner to start the exam adding the CID of the exam.
    function startExam(
        string memory _statement
    ) external onlyOwner {
        statement = _statement;
        dateStartExam = block.timestamp;
    }

    // Function used by the owner to get the ether stored in the contract address
    // from the students enrolling payments.
    function withdraw() external onlyOwner {
        payable(owner()).transfer(address(this).balance);
    }
}
// SPDX-License-Identifier: MIT.
pragma solidity 0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";

// Compute sha-256 in Windows:
// Get-FileHash '.\Examen historia.docx' | Format-list
// Compute sha-256 in Linux:
// sha256sum Examen\ historia.docx 

contract SmartExamBase is Ownable {

    // The owner is the one who creates the contract.
    constructor() Ownable(msg.sender){}

    struct Exam {
        /**
        * Struct that defines the features of an exam.
        * course: Name of the course of the exam.
        * id: Identifier to distinguish among the exams.
        * hash: Hash of the real exam file (to avoid tamper).
        * dateLastUpload: Date of the latest upload of the exam.
        * dateExam: Exact date when the exam should take place.
        * dateStartExam: Real date when the exam started.
        * duration: Duration of the exam in minutes.
        * enrollingPrice: Price to enroll in the exam (maybe taxes).
        */
        string course;
        uint id;
        string hash;
        string url;
        uint dateLastUpload;
        uint dateExam;
        uint dateStartExam;
        uint duration;
        uint enrollingPrice;
    }

    struct ExamStudent {
        /**
        * studentAdd: Address of the student who submits the exam.
        * exam: Struct of the exam that had been done.
        * hash_submision: Hash of the submission file.
        * url_exam_submited: URL to reach the submission file.
        * hash_correction: Hash of the correction file.
        * url_exam_correction: URL to reach the correction file.
        * score: Final score of the exam.
        */
        address studentAdd;
        Exam exam;
        string hash_submission;
        string url_exam_submited;
        string hash_correction;
        string url_exam_correction;
        uint score;
    }

    struct Student {
        /**
        * add: Address of the student.
        * exams_enrolled: Mapping to know the exams that the student have been enrolled.
        * exams_done: Mapping to get the exams done by the student.
        */
        address add;
        mapping(uint => bool) exams_enrolled; //key <- idExam, value <- True if it is enrolled.
        mapping(uint => ExamStudent) exams_done; //key <- idExam, value <- Student.
    }

    // Mapping used to know the registered professors.
    mapping(address => uint) profToId;
    // Counter of the exams that is also used to identify the exams.
    uint countExam = 0;
    // Array to access all the created exams.
    Exam[] exams;
    // Mapping to identify the address of a student with his/her struct information.
    mapping(address => Student) students;
    // ID exam -> Addresses of the students who submit their exams.
    mapping(uint => address[]) examsSubmited;

    // Check if an address matchs with a professor address.
    modifier onlyProfessor() {
        require(profToId[msg.sender] != 0, "Only professors can access to this function.");
        _;
    }

    // Check if an address matchs with a student address.
    modifier onlyStudent() {
        require(students[msg.sender].add != address(0), "Only students can access to this function.");
        _;
    }

    // Funciton to generate IDs
    function _generarId(address _id) private view onlyOwner returns (uint){
        return uint(keccak256(abi.encodePacked(_id)));
    }

    // Function used by the owner to add professors addresses.
    function addProfessor(address _profAdd) external onlyOwner returns(uint) {
        //We use the revert instead of require because it rollup the state of the contract.
        if(profToId[_profAdd] != 0){
            revert("Professor was already added.");
        }
        uint id = _generarId(_profAdd);
        profToId[_profAdd] = id;
        return id;
    } 

    // Function used by the owner to get the ether stored in the contract address.
    function withdraw() external onlyOwner {
        owner.transfer(this.balance);
    }
}
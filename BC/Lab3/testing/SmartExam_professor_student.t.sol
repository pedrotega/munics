// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.20;

import {Test, console2} from "forge-std/Test.sol";
import {SmartExam} from "../src/SmartExam.sol";

contract SmartExamTestProfessor is Test {
    address addOwner = address(1);
    address addProf = address(2);
    address addStud = address(3);
    address addAux = address(4);
    string student_submission = "student_submission";
    string student_correction = "student_correction";
    uint8 student_score = 10;

    SmartExam public smartexam;

    function setUp() public {        
        smartexam = new SmartExam();
        address o = smartexam.owner();
        vm.prank(o);
        smartexam.transferOwnership(addOwner);
        vm.startPrank(addOwner);

        // Editing exam.
        uint de = block.timestamp;
        uint8 dur = 1;
        uint24 p = 1;
        smartexam.editExamParameters(de, dur, p);

        // Adding professor.
        smartexam.registerProfessor(addProf);

        // Start exam.
        smartexam.startExam("_statement");

        // Adding student.
        vm.stopPrank();
        smartexam.enroll{value: 1 wei}();

        // Student submit exam.
        smartexam.setSubmission(student_submission);

        vm.startPrank(addProf);
    }

    function test_is_professor() public {
        assertEq(false, smartexam.isOwner(), "addProf should not be the prof.");
        assertEq(true, smartexam.isProfessor(), "addProf should be a professor.");
        assertEq(false, smartexam.isStudentEnrolled(), "addProf should not be a student.");
    }

    function test_get_students() public {
        address[] memory students = smartexam.getStudents();
        assertEq(address(this),students[0],"Professor should view the students");
    }

    function test_get_student_submission() public {
        address studAdd = smartexam.getStudents()[0];
        string memory stud_sub = smartexam.getStudentSubmission(studAdd);
        assertEq(student_submission, stud_sub);
    }

    function test_set_and_get_correction() public {
        address studAdd = smartexam.getStudents()[0];
        smartexam.setCorrection(studAdd, student_correction, student_score);
        string memory corr = smartexam.getCorrections()[0];
        assertEq(corr, student_correction, "Correction was not setted correctly");
    }

    function test_is_student() public{
        address studAdd = smartexam.getStudents()[0];
        vm.stopPrank();
        assertEq(true, smartexam.isStudentEnrolled(), "Student should be enrolled");
    }

    function test_get_my_exam() public {
        vm.stopPrank();
        string memory my_exam = smartexam.getMyExam();
        assertEq(my_exam, student_submission, "Student cannot get his/her exam");
    }

    // function test_get_my_correction() public {
    //     vm.stopPrank();
    //     string memory my_correction = smartexam.getMyCorrection();
    //     assertEq(my_correction, student_correction, "Student cannot get his/her correction");
    // }

    // function test_get_my_score() public {
    //     vm.stopPrank();
    //     uint8 my_score = smartexam.getMyScore();
    //     assertEq(my_score, student_score, "Student cannot get his/her score");
    // }
}
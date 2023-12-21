// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.20;

import {Test, console2} from "forge-std/Test.sol";
import {SmartExam} from "../src/SmartExam.sol";

contract SmartExamTestOwner is Test {
    address addOwner = address(1);
    address addProf = address(2);
    address addStud = address(3);
    address addAux = address(4);

    SmartExam public smartexam;

    function setUp() public {        
        smartexam = new SmartExam();
        address o = smartexam.owner();
        vm.prank(o);
        smartexam.transferOwnership(addOwner);
        vm.startPrank(addOwner);
    }

    function test_initial_owner() public {
        assertEq(addOwner, smartexam.owner(), "Initial owner is not addOwner.");
    }

    function test_is_owner() public {
        assertEq(true, smartexam.isOwner(), "addOwner should be the owner.");
        assertEq(false, smartexam.isProfessor(), "addOwner should not be a professor.");
        assertEq(false, smartexam.isStudentEnrolled(), "addOwner should not be a student.");
    }

    function test_transfer_ownership() public {
        smartexam.transferOwnership(addAux);
        assertEq(addAux, smartexam.owner(), "Owner does not change to addAux.");
        vm.startPrank(addAux);
        smartexam.transferOwnership(addOwner);
        assertEq(addOwner, smartexam.owner(), "Owner does not change to addOwner.");
    }

    function test_add_delete_professor() public {
        smartexam.registerProfessor(addProf);
        vm.startPrank(addProf);
        assertEq(true, smartexam.isProfessor(), "addProf should be a professor.");
        vm.startPrank(addOwner);
        smartexam.deleteProfessor(addProf);
        vm.startPrank(addProf);
        assertEq(false, smartexam.isProfessor(), "addProf should be a professor.");
    }

    function test_edit_exam_parameters() public {
        uint de = block.timestamp;
        uint8 dur = 1;
        uint24 p = 1;
        smartexam.editExamParameters(de, dur, p);

        assertEq(smartexam.dateExam(), de, "Exam date is not correct");
        assertEq(smartexam.duration(), dur, "Exam duration is not correct");
        assertEq(smartexam.enrollingPrice(), p, "Enrolling price is not correct");
    }

    function test_start_exam() public {
        uint de = block.timestamp;
        uint8 dur = 1;
        uint24 p = 1;
        smartexam.editExamParameters(de, dur, p);

        smartexam.startExam("_statement");
        assertEq(smartexam.getStatement(), "_statement", "Statement is not correct");
    }

    function test_withdraw() public payable{
        uint de = block.timestamp;
        uint8 dur = 1;
        uint24 p = 1;
        smartexam.editExamParameters(de, dur, p);
        
        vm.stopPrank();
        uint balanceBefore = address(smartexam).balance;
        smartexam.enroll{value: 1 wei}();
        uint balanceAfter = address(smartexam).balance;
        assertEq(balanceAfter - balanceBefore, 1 wei, "expect increase of 1 wei");
    }

    // function test_type_check_function() public {
    //     vm.startPrank(addOwner);
    //     assertEq(true, smartexam.isOwner(), "addOwner should be the owner.");
    //     assertEq(false, smartexam.isProfessor(), "addOwner should not be a professor.");
    //     assertEq(false, smartexam.isStudent(), "addOwner should not be a student.");
    //     smartexam.registerProfessor(addProf);
    //     vm.startPrank(addProf);
    //     assertEq(false, smartexam.isOwner(), "addProf should not be the prof.");
    //     assertEq(true, smartexam.isProfessor(), "addProf should be a professor.");
    //     assertEq(false, smartexam.isStudent(), "addProf should not be a student.");
    //     vm.startPrank(addStud);
    //     smartexam.enroll();
    //     assertEq(true, smartexam.isOwner(), "addOwner should not be the owner.");
    //     assertEq(false, smartexam.isProfessor(), "addOwner should not be a owner.");
    //     assertEq(false, smartexam.isStudent(), "addOwner should be a student.");
    // }

}
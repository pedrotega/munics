// SPDX-License-Identifier: Unlicenced
pragma solidity 0.8.18;

    contract TokenContract {
        address public owner;
        struct Receivers {
            string name;
            uint256 tokens;
        }

    mapping(address => Receivers) public users;

    modifier onlyOwner(){
        require(msg.sender == owner);
        _;
    }

    constructor(){
        owner = msg.sender;
        users[owner].tokens = 100;
    }

    function double(uint _value) public pure returns (uint){
        return _value*2;
    }

    function register(string memory _name) public{
        users[msg.sender].name = _name;
    }

    function giveToken(address _receiver, uint256 _amount) onlyOwner public payable {
        require(users[owner].tokens >= _amount);
        users[owner].tokens -= _amount;
        users[_receiver].tokens += _amount;
    }
 
    /*///////////////////////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////////////
    ///////////////////////////////////////////////////////////////////////////////////*/

    function buyToken(address _receiver, uint256 _amount) public payable {
        require(users[owner].tokens >= _amount, "Insuficient amount of tokens");
        require(msg.value >= _amount*5 ether, "Insuficient amount of ether sended." );
        users[owner].tokens -= _amount;
        users[_receiver].tokens += _amount;
    }

    function getContractBalance() public view returns (uint256) {
        return address(this).balance;
    }

}
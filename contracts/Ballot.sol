pragma solidity ^0.4.23;

contract Ballot {
    struct Voter {
        bool registered;
    }

    struct Candidate {
        uint votes;
    }

    address public owner;
    address public chairperson;
    mapping (address => Voter) register;
    mapping (address => Candidate) candidates;

    constructor() public {
        owner = msg.sender;
    }

    modifier isOwner() {
        require(
            msg.sender == owner,
            "Only the owner is authorized to execute this function"
        );
        _;
    }

    modifier isChairperson() {
        require(
            msg.sender == chairperson,
            "Only the chairperson is authorized to execute this function"
        );
        _;
    }

    function setChairperson(address _chairperson) public isOwner {
        chairperson = _chairperson;
        register[_chairperson].registered = true;
    }
}
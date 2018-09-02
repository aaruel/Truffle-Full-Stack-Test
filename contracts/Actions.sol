pragma solidity ^0.4.23;

import { Ballot } from "./Ballot.sol";

contract Actions is Ballot {
    modifier voterRegistered(address _voter) {
        require(
            register[_voter].registered == false,
            "voter already registered"
        );
        _;
    }

    modifier voterNotRegistered(address _voter) {
        require(
            register[_voter].registered != false,
            "voter already registered"
        );
        _;
    }

    function registerVoter(address _voter) public isChairperson voterNotRegistered(_voter) {
        register[_voter] = Voter(true);
    }

    function _vote(address _candidate, uint weight) private {
        candidates[_candidate].votes += weight;
    }

    function getVotes(address _candidate) public view returns (uint) {
        return candidates[_candidate].votes;
    }

    function vote(address _candidate) public voterRegistered(msg.sender) {
        if (msg.sender == chairperson) _vote(_candidate, 2);
        else _vote(_candidate, 1);
    }

    function getOwner() public view returns (address) {
        return owner;
    }

    function getChairperson() public view returns (address) {
        return chairperson;
    }
}
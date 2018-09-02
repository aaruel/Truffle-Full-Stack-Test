pragma solidity ^0.4.23;

import { Ballot } from "./Ballot.sol";

contract Migrations is Ballot {
    uint public last_completed_migration;

    function setCompleted(uint completed) public isOwner {
        last_completed_migration = completed;
    }

    function upgrade(address new_address) public isOwner {
        Migrations upgraded = Migrations(new_address);
        upgraded.setCompleted(last_completed_migration);
    }
}

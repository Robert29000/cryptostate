// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;

import "./StatePurchase.sol";

contract StatePurchaseFactory {

    mapping (address => address[]) public contracts;  // creator => its contracts

    function getContractsCount(address _creator) public view returns (uint){
        return contracts[_creator].length;
    }

    function createNewPurchase(address _token) public returns (address purchase) {
        purchase = address(new StatePurchase(_token, msg.sender));
        contracts[msg.sender].push(purchase);
    }
 
}


// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;

contract MultiOwnable {

    event OwnerAdded(address indexed _owner);
    event OwnerRemoved(address indexed _owner);
    event OwnerReplaced(address indexed oldOwner, address indexed newOwner);
    event RequirementChanged(uint value);
    event OperationSubmitted(uint indexed operationId);
    event OperationConfirmed(uint indexed operationId, address indexed _addr);
    event OperationRevoked(uint indexed operationId, address indexed _addr);

    uint constant public MAX_OWNER_COUNT = 10;

    mapping(uint => Operation) public operations;
    mapping(uint => mapping(address => bool)) public confirmations;
    mapping(address => bool) public isOwner;
    address[] public owners;
    uint public required;
    uint public operationCount;

    struct Operation {
        bytes32 data;
        bool executed;
    }

    modifier onlyOwner() {
        require(isOwner[msg.sender]);
        _ ;
    } 

    modifier inOwners(address _owner) {
        require(isOwner[_owner]);
        _ ;
    }

    modifier notInOwners(address _owner) {
        require(!isOwner[_owner]);
        _ ;
    }

    modifier notNull(address _addr) {
        require(_addr != address(0));
        _ ;
    }

    modifier operationExists(uint operationId) {
        require(operations[operationId].data != "");
        _ ;
    }

    modifier notConfirmed(uint operationId, address _addr) {
        require(!confirmations[operationId][_addr]);
        _ ;
    }

    modifier Confirmed(uint operationId, address _addr) {
        require(confirmations[operationId][_addr]);
        _ ;
    }

    modifier notExecuted(uint operationId) {
        require(!operations[operationId].executed);
        _ ;
    }

    modifier validRequirements(uint ownersCount, uint _required) {
        require(ownersCount <= MAX_OWNER_COUNT && _required <= ownersCount 
                && ownersCount != 0 && _required != 0);
        _ ;
    }

    constructor(address[] memory _owners, uint _required) public validRequirements(_owners.length, _required){
        for (uint i = 0; i < _owners.length; i++) {
            require(!isOwner[_owners[i]] && _owners[i] != address(0));
            isOwner[_owners[i]] = true;
        }
        owners = _owners;
        required = _required;
    }

    function addOwner(address _owner) public onlyOwner notInOwners(_owner)
                                notNull(_owner) validRequirements(owners.length + 1, required) 
    {
        isOwner[_owner] = true;    
        owners.push(_owner);

        emit OwnerAdded(_owner);
    }

    function removeOwner(address _owner) public onlyOwner inOwners(_owner) {
        isOwner[_owner] = false;
        for (uint i = 0; i < owners.length; i++) {
            if (owners[i] == _owner) {
                owners[i] = owners[owners.length - 1];
                owners.pop();
                break;
            }
        }
        
        if (required > owners.length) {
            changeRequirement(owners.length);
        }

        emit OwnerRemoved(_owner);
    }

    function replaceOwner(address oldOwner, address newOwner) public onlyOwner inOwners(oldOwner) notInOwners(newOwner) notNull(newOwner) {
        for (uint i = 0; i < owners.length; i++) {
            if (owners[i] == oldOwner) {
                owners[i] = newOwner;
            }
        }
        isOwner[oldOwner] = false;
        isOwner[newOwner] = true;

        emit OwnerReplaced(oldOwner, newOwner);
    }

    function changeRequirement(uint _required) public onlyOwner validRequirements(owners.length, _required) {
        required = _required;

        emit RequirementChanged(_required);
    }

    function submitOperation(bytes32 data) public returns (uint operationId) {
        operationId = addOperation(data);
        confirmOperation(operationId);

        emit OperationSubmitted(operationId);
    }

    function confirmOperation(uint operationId) public onlyOwner operationExists(operationId) notConfirmed(operationId, msg.sender) 
                                            returns (bool confirmed)
    {
        confirmations[operationId][msg.sender] = true;
        confirmed = isConfirmed(operationId);

        emit OperationConfirmed(operationId, msg.sender);
    }

    function revokeConfirmation(uint operationId) public onlyOwner Confirmed(operationId, msg.sender) notExecuted(operationId) {
        confirmations[operationId][msg.sender] = false;

        emit OperationRevoked(operationId, msg.sender);
    }

    function addOperation(bytes32 _data) internal returns (uint operationId){
        operationId = operationCount;
        operations[operationId] = Operation({
            data: _data,
            executed: false
        });
        operationCount += 1;
    }

    function isConfirmed(uint operationId) public view returns (bool) {
        uint count = 0;
        for (uint i = 0; i < owners.length; i++) {
            if (confirmations[operationId][owners[i]]) {
                count += 1;
            }
            if (count == required) {
                return true;
            }
        }
        return false;
    }

    function getConfirmationCount(uint operationId) public view returns (uint count) {
        for (uint i = 0; i < owners.length; i++) {
            if (confirmations[operationId][owners[i]]) {
                count += 1;
            }
        }
    }
}
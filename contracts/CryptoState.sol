// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;

import "./MultiOwnable.sol";
import "../interfaces/IERC20withKYC.sol";
import "./SafeMath.sol";

contract CryptoState is IERC20withKYC, MultiOwnable {


    event Transfer(address indexed from, address indexed to, uint value);
    event Approval(address indexed owner, address indexed spender, uint value);
    event KYCPassed(address indexed _addr);
    event Issue(uint value);
    event Redeem(uint value);

    using SafeMath for uint;

    mapping (address => bool) public kyc_addrs;
    mapping (address => uint) public balances;
    mapping (address => mapping (address => uint)) allowed;
    mapping (uint => address) public address_operations; // operationId => address
    mapping (address => bool) public wait_for_confirmations;

    string public name;
    string public symbol;
    uint public _totalSupply;
    uint public decimals;


    modifier onlyKYC(address _addr) {
        require(kyc_addrs[_addr]);
        _ ;
    }

    modifier notKYC(address _addr) {
        require(!kyc_addrs[_addr]);
        _ ;
    }

    modifier notWaiting(address _addr) {
        require(!wait_for_confirmations[_addr]);
        _ ;
    }

    modifier onlyPayloadSize(uint size) {
        require(msg.data.length >= size + 4);
        _ ;
    }

    constructor(string memory _name, string memory _symbol, uint _decimals, uint[] memory initialSupply, address[] memory _owners, uint _required)
        MultiOwnable(_owners, _required) 
    {
        require(initialSupply.length == _owners.length);
        name = _name;
        symbol = _symbol;
        decimals = _decimals;
        for (uint i = 0; i < _owners.length; i++) {
            kyc_addrs[_owners[i]] = true;
            balances[_owners[i]] = initialSupply[i];
            _totalSupply = _totalSupply.add(initialSupply[i]);
        }
    }

    function transfer(address _to, uint value) onlyKYC(msg.sender) public override onlyKYC(_to) onlyPayloadSize(2 * 32) {
        balances[msg.sender] = balances[msg.sender].sub(value);
        balances[_to] = balances[_to].add(value);

        emit Transfer(msg.sender, _to, value);
    }

    function transferFrom(address _from, address _to, uint value) public override onlyKYC(msg.sender) onlyKYC(_from) onlyKYC(_to) onlyPayloadSize(3 * 32) {
        allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(value);
        balances[_from] = balances[_from].sub(value);
        balances[_to] = balances[_to].add(value);

        emit Transfer(_from, _to, value);
    }

    function approve(address _spender, uint value) public override onlyKYC(msg.sender) onlyKYC(_spender) onlyPayloadSize(2 * 32) {
        require(allowed[msg.sender][_spender] == 0 || value == 0);
        allowed[msg.sender][_spender] = value;

        emit Approval(msg.sender, _spender, value);
    } 

    function balanceOf(address _who) onlyKYC(_who) public override view returns (uint) {
        return balances[_who];
    }

    function allowance(address _owner, address _spender) public override onlyKYC(_owner) onlyKYC(_spender) view returns (uint) {
        return allowed[_owner][_spender];
    }

    function totalSupply() public override view returns (uint) {
        return _totalSupply;
    }

    function issue(uint amount) public onlyOwner {
        require(_totalSupply + amount > _totalSupply);
        require(balances[msg.sender] + amount > balances[msg.sender]);

        balances[msg.sender] = balances[msg.sender].add(amount);
        _totalSupply = _totalSupply.add(amount);

        emit Issue(amount);
    }

    function redeem(uint amount) public onlyOwner {
        balances[msg.sender] = balances[msg.sender].sub(amount);
        _totalSupply = _totalSupply.sub(amount);

        emit Redeem(amount);
    }

    function submitAddress(address _address, bytes32 data) public onlyOwner notKYC(_address) notWaiting(_address) returns (uint id) {
        id = super.submitOperation(data);
        address_operations[id] = _address;
        wait_for_confirmations[_address] = true;
    }

    function confirmAddress(uint operationId) public onlyOwner returns (bool confirmed){
        confirmed = super.confirmOperation(operationId);
        if (confirmed) {
            address address_for_confirmation = address_operations[operationId];
            kyc_addrs[address_for_confirmation] = true;
            wait_for_confirmations[address_for_confirmation] = false;

            emit KYCPassed(address_for_confirmation);
        }
    }

    function revokeAddress(uint operationId) public onlyOwner {
        super.revokeConfirmation(operationId);
    }

    function kycPassed(address _address) public override view returns (bool) {
        return kyc_addrs[_address];
    }

    // OnlyOwner will be checked in super function

    function addStateOwner(address _owner, uint initialSupply) public onlyOwner {
        super.addOwner(_owner);
        kyc_addrs[_owner] = true;
        balances[_owner] = initialSupply;
        _totalSupply = _totalSupply.add(initialSupply);
    }

    // OnlyOwner will be checked in super function

    function removeStateOwner(address _owner) public  {
        super.removeOwner(_owner);
        kyc_addrs[_owner] = false;
        _totalSupply = _totalSupply.sub(balances[_owner]);
        balances[_owner] = 0;
    }

    // OnlyOwner will be checked in super function

    function replaceStateOwner(address oldOwner, address newOwner, uint initialSupply) public {
        super.replaceOwner(oldOwner, newOwner);
        kyc_addrs[oldOwner] = false;
        kyc_addrs[newOwner] = true;
        _totalSupply = _totalSupply.sub(balances[oldOwner]);
        _totalSupply = _totalSupply.add(initialSupply);
        balances[oldOwner] = 0;
        balances[newOwner] = initialSupply;
    }
}
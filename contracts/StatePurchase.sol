// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;

import "./SafeMath.sol";
import "../interfaces/IERC20withKYC.sol";

contract StatePurchase {

    using SafeMath for uint;

    IERC20withKYC public token;
    
    address public seller;
    address public buyer;
    uint public value;


    enum State { Constructed, Created, Locked, Released, Inactive }

    State public state;

    modifier evenValue(uint _value) {
        uint part = _value / 2;
        require(part * 2 == value);
        _ ;
    }

    modifier inState(State _state) {
        require(_state == state);
        _ ;
    }

    modifier onlyBuyer() {
        require(msg.sender == buyer);
        _ ;
    }

    modifier onlySeller() {
        require(msg.sender == seller);
        _ ;
    }

    constructor(address _token, address _seller) {
        token = IERC20withKYC(_token);
        seller = _seller;
    }

    function initialize(uint _value) public inState(State.Constructed) evenValue(_value){
        require(token.allowance(seller, address(this)) == _value);
        require(token.kycPassed(address(this)));
        value = _value / 2;
        token.transferFrom(seller, address(this), _value);
        state = State.Created;
    }

    function confirmPurchase(address _buyer, uint _value) public inState(State.Created) evenValue(_value){
        require(_value == 2 * value);
        require(token.allowance(_buyer, address(this)) == _value);
        buyer = _buyer;
        state = State.Locked;
    }

    function confirmReceived() public  onlyBuyer inState(State.Locked) {
        state = State.Released;
        token.transfer(buyer, value);
    }

    function refundSeller() public onlySeller inState(State.Released) {
        state = State.Inactive;
        token.transfer(seller, 3 * value);
    }
}
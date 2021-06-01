// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;

interface IERC20withKYC {
    function totalSupply() external view returns (uint);
    function balanceOf(address who) external view returns (uint);
    function transfer(address to, uint value) external;
    function allowance(address owner, address spender) external view returns (uint);
    function transferFrom(address from, address to, uint value) external;
    function approve(address spender, uint value) external;
    function kycPassed(address _address) external view returns (bool);
}
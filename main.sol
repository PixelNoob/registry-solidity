// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract NameIndex {
    // State variable to store a number
    mapping(address => string) public names;

    // Address of the required token contract
    address public requiredToken;

    // event everytime someone uses the function set
    event NameSet(address indexed sender, string name);

    constructor(address _requiredToken) {
        requiredToken = _requiredToken;
    }

    // Allow users to set their name by sending 1 unit of the required token
    function set(string calldata _text) public {
        // Transfer the required token from the sender's account to the contract's account
        ERC20(requiredToken).transferFrom(msg.sender, address(this), 1);

        // Set the sender's name
        names[msg.sender] = _text;

        // Transfer the received token to the Ethereum burn address
        ERC20(requiredToken).transfer(address(0x000000000000000000000000000000000000dEaD), 1);

        // Emit the NameSet event
        emit NameSet(msg.sender, _text);
    }

    // Implement the receive function to receive token transfers
    function receive() external payable {
        // Do nothing. This function is needed to receive token transfers.
    }
}

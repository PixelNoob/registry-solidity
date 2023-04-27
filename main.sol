// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

contract Registry {
    using SafeERC20 for IERC20;

    // State variable to store a number
    mapping(address => string) public names;

    // Address of the required token contract
    address public requiredToken;

    // event everytime someone uses the function set
    event NameSet(address indexed sender, string name);

    constructor(address _requiredToken) {
        // Check that the token at the given address is an ERC20 token
        require(IERC20(_requiredToken).totalSupply() > 0, "Registry: Token is not ERC20");


        requiredToken = _requiredToken;
    }

    // Allow users to set their name by sending 1 unit of the required token
    function set(string calldata _text) external  {
        // Transfer the required token from the sender's account to the contract's account
        IERC20(requiredToken).transferFrom(msg.sender, address(this), 1);

        // Set the sender's name
        names[msg.sender] = _text;

        // Transfer the received token to the Ethereum burn address
        IERC20(requiredToken).transfer(address(0x000000000000000000000000000000000000dEaD), 1);

        // Emit the NameSet event
        emit NameSet(msg.sender, _text);
    }

    // Implement the receive function to receive token transfers
    receive() external payable {
        // Do nothing. This function is needed to receive token transfers.
    }
}

# Registry Contract

This is a Solidity smart contract that allows users to set their name by sending 1 unit of a specified ERC20 token.

## Usage

### Deploying the Contract

To deploy the contract, you will need to provide the address of the ERC20 token contract that you want to use as the required token. You can do this by passing the address as an argument to the constructor when you deploy the contract.

### Setting a Name

To set a name, a user needs to call the `set` function and provide the desired name as a string argument. In addition, the user needs to send 1 unit of the required token to the contract.

### Viewing a Name

To view the name associated with an address, you can call the `names` function with the address as an argument.

## Contract Details

### State Variables

- `names`: a mapping that stores the names associated with addresses
- `requiredToken`: the address of the ERC20 token contract that is required to set a name

### Events

- `NameSet`: emitted whenever a user sets their name, contains the address of the sender and the name that was set

### Functions

- `constructor`: sets the `requiredToken` address when the contract is deployed
- `set`: allows users to set their name by sending 1 unit of the required token
- `receive`: a fallback function that allows the contract to receive token transfers
- `names`: a getter function that returns the name associated with an address

## License

This contract is licensed under the MIT License.


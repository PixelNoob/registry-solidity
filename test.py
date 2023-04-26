import pytest
from web3 import Web3
from web3.contract import Contract
from eth_account import Account
from eth_utils import to_wei

from NameIndex import abi as name_index_abi
from ChittyCoin import abi as chitty_coin_abi


@pytest.fixture(scope="module")
def web3() -> Web3:
    return Web3(Web3.HTTPProvider("http://localhost:8545"))


@pytest.fixture(scope="module")
def accounts(web3: Web3) -> list[Account]:
    return web3.eth.accounts


@pytest.fixture(scope="module")
def chitty_coin(web3: Web3, accounts: list[Account]) -> Contract:
    return web3.eth.contract(
        abi=chitty_coin_abi,
        bytecode=chitty_coin_bytecode,
        ContractFactoryClass=Contract,
    ).deploy({"from": accounts[0]})


@pytest.fixture(scope="module")
def name_index(web3: Web3, chitty_coin: Contract, accounts: list[Account]) -> Contract:
    return web3.eth.contract(
        abi=name_index_abi,
        bytecode=name_index_bytecode,
        args=[chitty_coin.address],
        ContractFactoryClass=Contract,
    ).deploy({"from": accounts[0]})


def test_set(web3: Web3, chitty_coin: Contract, name_index: Contract, accounts: list[Account]):
    # Approve the NameIndex contract to spend tokens on behalf of the user
    chitty_coin.functions.approve(name_index.address, to_wei(1, "ether")).transact({"from": accounts[1]})

    # Call the set function with a name
    name_index.functions.set("Alice").transact({"from": accounts[1]})

    # Check that the name was set correctly
    assert name_index.functions.names(accounts[1]).call() == "Alice"


def test_set_without_approval(web3: Web3, chitty_coin: Contract, name_index: Contract, accounts: list[Account]):
    # Call the set function without approval
    with pytest.raises(ValueError):
        name_index.functions.set("Bob").transact({"from": accounts[2]})


def test_set_without_balance(web3: Web3, chitty_coin: Contract, name_index: Contract, accounts: list[Account]):
    # Approve the NameIndex contract to spend tokens on behalf of the user
    chitty_coin.functions.approve(name_index.address, to_wei(1, "ether")).transact({"from": accounts[3]})

    # Transfer all tokens to another account to simulate a zero balance
    chitty_coin.functions.transfer(accounts[4], to_wei(1000000, "ether")).transact({"from": accounts[3]})

    # Call the set function with a name
    with pytest.raises(ValueError):
        name_index.functions.set("Charlie").transact({"from": accounts[3]})

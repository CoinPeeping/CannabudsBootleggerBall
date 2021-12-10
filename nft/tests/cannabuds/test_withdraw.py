from brownie import CannaBudsBootleggerBall, network, reverts
from brownie.network import contract
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.cannabuds.deploy_contract import deploy_contract

import pytest


def test_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Test only used for local testing")

    contract = deploy_contract()
    initial_amount = contract.totalSupply()
    contract.openSale()

    contract.mint(10, {"from": get_account(), "value": 10 * contract.tokenPrice()})
    assert contract.totalSupply() == 10 + initial_amount
    balance_of_contract = contract.balance()
    balance_of_account = get_account().balance()

    contract.withdraw({"from": get_account()})
    assert get_account().balance() == balance_of_account + balance_of_contract
    assert contract.balance() == 0

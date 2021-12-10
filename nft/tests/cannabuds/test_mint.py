from brownie import CannaBudsBootleggerBall, network, reverts
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.cannabuds.deploy_contract import deploy_contract

import pytest


def test_mint_closed_sale():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Test only used for local testing")

    contract = deploy_contract()

    with reverts("Sale is not active."):
        contract.mint(1, {"from": get_account()})
        assert contract.totalSupply() == 0


def test_mint_too_many_tokens():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Test only used for local testing")

    contract = deploy_contract()
    contract.openSale({"from": get_account()})

    with reverts("The amount of tokens you are trying to mint exceeds the max supply."):
        contract.mint(contract.MAX_SUPPLY() + 1, {"from": get_account()})
        assert contract.totalSupply() == 0


def test_mint_no_tokens():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Test only used for local testing")

    contract = deploy_contract()
    contract.openSale({"from": get_account()})

    with reverts("Minimum mint is 1 token"):
        contract.mint(0, {"from": get_account()})
        assert contract.totalSupply() == 0


def test_mint_more_than_max_purchaseable():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Test only used for local testing")

    contract = deploy_contract()
    contract.openSale({"from": get_account()})

    with reverts("Maximum mint is 20 tokens"):
        contract.mint(contract.MAX_PURCHASABLE() + 1, {"from": get_account()})
        assert contract.totalSupply() == 0


def test_mint_not_enough_price():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Test only used for local testing")

    contract = deploy_contract()
    contract.openSale({"from": get_account()})

    with reverts("Incorrect Ether value."):
        contract.mint(3, {"from": get_account(), "value": 1 * contract.tokenPrice()})
        assert contract.totalSupply() == 0


def test_general_mint_during_presale():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Test only used for local testing")

    contract = deploy_contract()
    contract.openSale({"from": get_account()})
    contract.openWhitelist({"from": get_account()})

    with reverts("Only whitelisted users may mint at this time"):
        contract.mint(3, {"from": get_account(), "value": 3 * contract.tokenPrice()})
        assert contract.totalSupply() == 0

from brownie import CannaBudsBootleggerBall, network, reverts
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.cannabuds.deploy_contract import deploy_contract

import pytest


def test_presale_mint_closed_sale():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Test only used for local testing")

    contract = deploy_contract()
    contract.addToWhitelist([get_account()], {"from": get_account()})

    with reverts("Sale and whitelist must be active to mint"):
        contract.presaleMint(1, {"from": get_account()})
        assert contract.totalSupply() == 0


def test_presale_mint_during_closed_whitelist():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Test only used for local testing")

    contract = deploy_contract()
    contract.openSale({"from": get_account()})
    contract.addToWhitelist([get_account()], {"from": get_account()})

    with reverts("Sale and whitelist must be active to mint"):
        contract.presaleMint(
            3, {"from": get_account(), "value": 3 * contract.tokenPrice()}
        )
        assert contract.totalSupply() == 0


def test_presale_mint_non_whitelisted_user():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Test only used for local testing")

    contract = deploy_contract()
    contract.openSale({"from": get_account()})
    contract.openWhitelist({"from": get_account()})

    with reverts("You must be on the whitelist to mint during the presale."):
        contract.presaleMint(1, {"from": get_account()})
        assert contract.totalSupply() == 0


def test_presale_mint_more_than_allowed_to_hold():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Test only used for local testing")

    contract = deploy_contract()
    contract.openSale({"from": get_account()})
    contract.openWhitelist({"from": get_account()})

    contract.addToWhitelist([get_account()], {"from": get_account()})

    with reverts("You can only mint 10 before the sale begins"):
        contract.presaleMint(
            10, {"from": get_account(), "value": 10 * contract.tokenPrice()}
        )
        contract.presaleMint(1, {"from": get_account()})
        assert contract.totalSupply() == 10


def test_presale_mint_no_tokens():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Test only used for local testing")

    contract = deploy_contract()
    contract.openSale({"from": get_account()})
    contract.openWhitelist({"from": get_account()})

    contract.addToWhitelist([get_account()], {"from": get_account()})

    with reverts("Minimum mint is 1 token"):
        contract.presaleMint(0, {"from": get_account()})
        assert contract.totalSupply() == 0


def test_presale_mint_more_than_max_purchaseable():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Test only used for local testing")

    contract = deploy_contract()
    contract.openSale({"from": get_account()})
    contract.openWhitelist({"from": get_account()})

    contract.addToWhitelist([get_account()], {"from": get_account()})

    with reverts("You can only mint 10 before the sale begins"):
        contract.presaleMint(11, {"from": get_account()})
        assert contract.totalSupply() == 0


def test_presale_mint_not_enough_price():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Test only used for local testing")

    contract = deploy_contract()
    contract.openSale({"from": get_account()})
    contract.openWhitelist({"from": get_account()})

    contract.addToWhitelist([get_account()], {"from": get_account()})

    with reverts("Incorrect Ether value."):
        contract.presaleMint(
            3, {"from": get_account(), "value": 1 * contract.tokenPrice()}
        )
        assert contract.totalSupply() == 0

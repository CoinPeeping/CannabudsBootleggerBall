from brownie import CannaBudsBootleggerBall, network, reverts

from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from scripts.cannabuds.deploy_contract import (
    BASE_URI,
    TOKEN_SYMBOL,
    TOKEN_NAME,
    deploy_contract,
)
import pytest


def test_deploy_contract():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Test only used for local testing")

    contract = CannaBudsBootleggerBall.deploy(
        TOKEN_NAME,
        TOKEN_SYMBOL,
        BASE_URI,
        {"from": get_account()},
        publish_source=False,
    )

    assert contract.name() == TOKEN_NAME
    assert contract.symbol() == TOKEN_SYMBOL
    assert contract.baseURI() == BASE_URI
    assert contract.totalSupply() == 5
    assert contract.saleIsActive() == False
    assert contract.whitelistActive() == False
    assert contract.MAX_SUPPLY() == 10420
    assert contract.MAX_PURCHASABLE() == 20


def test_deploy_and_reserve_tokens():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Test only used for local testing")

    reserve_amount = 60

    contract = deploy_contract()
    initial_amount = contract.totalSupply()
    contract.reserveTokens(reserve_amount, {"from": get_account()})

    assert contract.totalSupply() == reserve_amount + initial_amount


def test_deploy_and_reserve_too_many_tokens():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Test only used for local testing")

    contract = deploy_contract()

    reserve_amount = contract.MAX_SUPPLY() + 1
    with reverts():
        contract.reserveTokens(reserve_amount, {"from": get_account()})
        assert contract.totalSupply() == 0

from brownie import CannaBudsBootleggerBall, network
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.cannabuds.deploy_contract import deploy_contract

import pytest


def test_whitelist():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Test only used for local testing")

    contract = deploy_contract()

    assert contract.getWhitelistSize() == 0
    contract.addToWhitelist([get_account()], {"from": get_account()})
    assert contract.getWhitelistSize() == 1
    assert contract.isWhitelisted(get_account())
    contract.clearWhitelist({"from": get_account()})
    assert contract.getWhitelistSize() == 0

from brownie import CannaBudsBootleggerBall, network
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from scripts.cannabuds.deploy_contract import deploy_contract
import pytest

from web3 import Web3


def test_setting_open_close_sale():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Test only used for local testing")

    contract = deploy_contract()
    assert contract.saleIsActive() == False
    contract.openSale({"from": get_account()})
    assert contract.saleIsActive() == True
    contract.closeSale({"from": get_account()})
    assert contract.saleIsActive() == False


def test_setting_open_close_whitelist():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Test only used for local testing")

    contract = deploy_contract()
    assert contract.whitelistActive() == False
    contract.openWhitelist({"from": get_account()})
    assert contract.whitelistActive() == True
    contract.closeWhitelist({"from": get_account()})
    assert contract.whitelistActive() == False


def test_token_uri():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Test only used for local testing")

    contract = deploy_contract()
    api_url = "https://www.cannabuds.io/api/"

    contract.setBaseURI(api_url)
    token_id = 5

    assert contract.baseURI() == api_url
    assert contract.tokenURI(5) == contract.baseURI() + str(5)


def test_set_token_price():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Test only used for local testing")

    contract = deploy_contract()
    assert contract.tokenPrice() == Web3.toWei(0.042, "ether")
    contract.setTokenPrice(Web3.toWei(0.01, "ether"), {"from": get_account()})
    assert contract.tokenPrice() == Web3.toWei(0.01, "ether")

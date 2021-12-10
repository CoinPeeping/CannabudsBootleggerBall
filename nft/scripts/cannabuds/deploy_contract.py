from brownie import CannaBudsBootleggerBall, network
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS


TOKEN_NAME = "CannaBuds Bootlegger Ball"
TOKEN_SYMBOL = "CCB"
BASE_URI = "https://www.astradanft.com/api/"


def main():
    deploy_contract()


def deploy_contract():
    account = get_account()

    publish_source = network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS

    contract = CannaBudsBootleggerBall.deploy(
        TOKEN_NAME,
        TOKEN_SYMBOL,
        BASE_URI,
        {"from": account},
        publish_source=publish_source,
    )

    return contract

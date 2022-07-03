from scripts.helpful_scripts import get_account
from brownie import interface, network, config, accounts


def main():
    get_weth()


def get_weth():
    """""
    Mints WETH by depositiing ETH
    """ ""
    # ABI
    # Address

    account = accounts[0]
    weth = interface.IWeth(config["networks"][network.show_active()]["weth_token"])

    tx = weth.deposit({"from": account, "value": 0.069 * 10**18})
    tx.wait(1)
    print("<3  You successfully have your fully automated 0.1WETH  <3")
    return tx

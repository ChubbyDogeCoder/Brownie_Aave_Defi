from brownie import accounts, network, config, interface
from scripts.helpful_scripts import get_account
from scripts.get_weth import get_weth
from web3 import Web3

amount = Web3.toWei(0.021, "ether")


def main():
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]

    if network.show_active() in ["mainnet-fork"] or ["kovan"]:
        get_weth()

    lending_pool = get_lending_pool()
    print("This is the lending pool: ", lending_pool)

    # Approve sending ERC-20 Tokk
    approve_erc20(amount, lending_pool.address, erc20_address, account)

    # Deposit the token to aave

    ## Alternative boring mmethod ::<<==>>::
    # print("Depppppositing............ 👨‍💻")
    # tx = lending_pool.deposit(
    # erc20_address, amount, account.address, 0, {"from": account}
    # )
    # tx.wait(1)
    # print("DEpoisited the tokkkens like a boss 👼")

    depositing_erc20(lending_pool, erc20_address, amount, account, 0)
    erc20 = interface.IERC20(erc20_address)
    erc30 = erc20.balanceOf(account, {"from": account})
    print("-------------\n This is how much wEth: ", Web3.fromWei(erc30, "ether"))

    # So how much do we need to borrow ?
    # Now let's become a real degen and start borrowing

    Total_collateral, Borrowable_eth, total_debt = get_borrowable_data(
        lending_pool, account
    )
    print("Now let's become a real degen and start borrowing 🤴🤴🤴")
    # DAI in terms of ETH
    dai_eth_price = get_asset_price(
        config["networks"][network.show_active()]["dai_eth_price_feed"]
    )
    inWei_Borrwable_eth = Web3.toWei(Borrowable_eth, "ether")
    amount_dai_to_borrow = (1 / dai_eth_price) * (inWei_Borrwable_eth * 0.95)
    print("\n")
    print(f"we are going to be a degen with borrowing {amount_dai_to_borrow} Dai")
    print(f"dai_eth_price: {dai_eth_price}")
    print(f"amount_dai_to_borrow: {inWei_Borrwable_eth}")
    print("\n")

    print(f"Now let's borrow !!🔞🔞🔞🔞🔞☢☢☢💱💱💱")

    DAi_address = config["networks"][network.show_active()]["dai_token"]
    borrow_tx = lending_pool.borrow(
        DAi_address,
        Web3.toWei(amount_dai_to_borrow, "ether"),
        1,
        0,
        account.address,
        {"from": account},
    )
    borrow_tx.wait(1)
    print("❌❌❌ Now the game has begun!, aka,. borrowing has started... ⛔⛔⛔")

    get_borrowable_data(lending_pool, account)

    # Repay Time!!!

    # replay_all(amount, lending_pool, account)
    print("Not so fast, first you have to see your account data:\n")
    get_borrowable_data(lending_pool, account)

    # print("\n\n\n\nYou finally paid back all your sins, Well done Young Blood 🤩🤩🤩\n\n\n\n")

    ########################################----------------------------------------################################################


def get_lending_pool():
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool


def approve_erc20(amount, spender, erc20_adress, account):
    print("Approving ERC20 TOkkken")
    erc20 = interface.IERC20(erc20_adress)
    erc30 = erc20.balanceOf(account, {"from": account})
    tx = erc20.approve(spender, amount, {"from": account})

    tx.wait(1)
    print("Yay, it got approved")
    print("the amount is ", amount)
    print("The account is ", account)
    print("tha account vaue is ", account.balance())
    print("The spender is ", spender)
    print("The erc_contract address is ", erc20_adress)
    print("-------------\n This is how much wEth: ", Web3.fromWei(erc30, "ether"))

    # function deposit(address asset, uint256 amount, address onBehalfOf, uint16 referralCode)


def depositing_erc20(_lending_pool, edr, amount, acc_ad, value):
    print("Depppppositing............ 👨‍💻")

    tx = _lending_pool.deposit(edr, amount, acc_ad.address, value, {"from": acc_ad})
    tx.wait(1)
    print("DEpoisited the tokkkens like a boss 👼")
    return tx


def get_borrowable_data(lending_pool, account):
    (
        tatal_collateral_ETH,
        total_Debt_ETH,
        avaialable_borow_ETH,
        current_liquidation_threshold,
        ltv,
        health_factor,
    ) = lending_pool.getUserAccountData(account.address)
    avaialable_borow_ETH = Web3.fromWei(avaialable_borow_ETH, "ether")
    tatal_collateral_ETH = Web3.fromWei(tatal_collateral_ETH, "ether")
    total_Debt_ETH = Web3.fromWei(total_Debt_ETH, "ether")
    print(f"you have {tatal_collateral_ETH} worth of ETH deposited.")
    print(f"you have {avaialable_borow_ETH} worth of ETHto borrow")
    print(f"you have {total_Debt_ETH} worth of ETH borrowed.")

    return (
        float(tatal_collateral_ETH),
        float(avaialable_borow_ETH),
        float(total_Debt_ETH),
    )


def get_asset_price(price_feed_address):
    dai_eth_price_feed = interface.AggregatorV3Interface(price_feed_address)
    latest_price = dai_eth_price_feed.latestRoundData()[1]
    converted_latest_priice = Web3.fromWei(latest_price, "ether")
    print(f"The DAI/ETH price is {converted_latest_priice} ")
    return float(latest_price)


def replay_all(amount, pool, account):
    approve_erc20(
        Web3.toWei(amount, "ether"),
        pool,
        config["networks"][network.show_active()]["dai_token"],
        account,
    )
    repay_Tx = pool.repay(
        config["networks"][network.show_active()]["dai_token"],
        amount,
        1,
        account.address,
        {"from": account},
    )
    repay_Tx.wait(1)
    print("Debt repayment complete 🎃\n\n")

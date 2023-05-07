from web3 import Web3
from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3.auto import w3
from web3.middleware import construct_sign_and_send_raw_middleware
import math
import numpy as np
import pandas as pd
import abis

from dotenv import load_dotenv
load_dotenv()
import os


# Providers
# Arbitrum Provider (e.g. Infura)
arbiw3 = Web3(Web3.HTTPProvider(os.getenv("INFURA_ARBI")))
print( "Connected Successfully to Web 3 Provider" if arbiw3.is_connected() else  "Web3 Provider Error")

# Wallet
private_key = os.environ.get("MAIN_PK")
assert private_key is not None, "You must set MAIN_PK environment variable"
assert private_key.startswith("0x"), "Private key must start with 0x hex prefix"

account: LocalAccount = Account.from_key(private_key)
arbiw3.middleware_onion.add(construct_sign_and_send_raw_middleware(account))
arbiw3.eth.default_account = account.address
print("Your hot wallet address is " , arbiw3.eth.default_account)


# Addresses
AddressZero = "0x0000000000000000000000000000000000000000"
weth = "0x82af49447d8a07e3bd95bd0d56f35241523fbab1"
btc = "0x2f2a2543b76a4166549f7aab2e75bef0aefc5b0f"
usdc = "0xff970a61a04b1ca14834a43f5de4533ebddb5cc8"
usdt = "0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9"
gmx_vault = "0x489ee077994B6658eAfA855C308275EAd8097C4A"
gmx_router = "0xaBBc5F99639c9B6bCb58544ddf04EFA6802F4064"
gmx_reader = "0x22199a49A999c351eF7927602CFB187ec3cae489"
gmx_orderbook = "0x09f77E8A13De9a35a7231028187e9fD5DB8a2ACB"
gmx_position_router = "0x3D6bA331e3D9702C5e8A8d254e5d8a285F223aba"
chainlink_btc_addr = "0x6ce185860a4963106506C203335A2910413708e9"
chainlink_eth_addr = "0x639Fe6ab55C921f74e7fac1ee960C0B6293ba612"

# Contracts
weth_contract = arbiw3.eth.contract(address=Web3.to_checksum_address(weth.lower()), abi=abis.ERC20)
btc_contract = arbiw3.eth.contract(address=Web3.to_checksum_address(btc.lower()), abi=abis.ERC20)
usdc_contract = arbiw3.eth.contract(address=Web3.to_checksum_address(usdc.lower()), abi=abis.ERC20)
usdt_contract = arbiw3.eth.contract(address=Web3.to_checksum_address(usdt.lower()), abi=abis.ERC20)
vault_contract = arbiw3.eth.contract(address=gmx_vault, abi=abis.GMX_VAULT)
reader_contract = arbiw3.eth.contract(address=gmx_reader, abi=abis.GMX_READER)
orderbook_contract = arbiw3.eth.contract(address=gmx_orderbook, abi=abis.GMX_ORDERBOOK)
position_router_contract = arbiw3.eth.contract(address=gmx_position_router, abi=abis.GMX_POSITION_ROUTER)
chainlink_btc_contract = arbiw3.eth.contract(address=chainlink_btc_addr, abi=abis.CHAINLINK)
chainlink_eth_contract = arbiw3.eth.contract(address=chainlink_eth_addr, abi=abis.CHAINLINK)

# Chainlink datafeed to get current price of tokens
def getPrice(coin):
    if (coin == "btc"):
        latestData = chainlink_btc_contract.functions.latestRoundData().call()

    elif (coin == "eth"):
        latestData = chainlink_eth_contract.functions.latestRoundData().call()

    return latestData[1]/100000000.0

# The two functions below check the positions of the user's wallet in GMX
# Output is a 1x9 array per coin with: size, collateral, averagePrice, entryFundingRate, hasRealisedProfit, realisedPnl, lastIncreasedTime, hasProfit, delta
def lookupPositions(address, coin):
    print(address + " " + coin + " positions:")
    if (coin == "btc"):
        positions = reader_contract.functions.getPositions( Web3.to_checksum_address(gmx_vault.lower()), Web3.to_checksum_address(address.lower()), [ Web3.to_checksum_address(btc.lower()),  Web3.to_checksum_address(usdc.lower())], [Web3.to_checksum_address(btc.lower()), Web3.to_checksum_address(btc.lower())], [True, False]).call()
    elif (coin == "eth"):
        positions = reader_contract.functions.getPositions( Web3.to_checksum_address(gmx_vault.lower()), Web3.to_checksum_address(address.lower()), [ Web3.to_checksum_address(weth.lower()),  Web3.to_checksum_address(usdc.lower())], [Web3.to_checksum_address(weth.lower()), Web3.to_checksum_address(weth.lower())], [True, False]).call()
    else:
        positions = []
    print(positions)

def getPosition(address, coin, collateral, is_long):
    if (coin == "btc"):
        indexcoin = Web3.to_checksum_address(btc.lower())
    elif (coin == "eth"):
        indexcoin = Web3.to_checksum_address(weth.lower())
    if (collateral == "btc"):
        collateralcoin = Web3.to_checksum_address(btc.lower())
    elif (collateral == "weth"):
        collateralcoin = Web3.to_checksum_address(weth.lower())
    elif (collateral == "usdc"):
        collateralcoin = Web3.to_checksum_address(usdc.lower())
    elif (collateral == "usdt"):
        collateralcoin = Web3.to_checksum_address(usdt.lower())
    position = reader_contract.functions.getPositions( Web3.to_checksum_address(gmx_vault.lower()), Web3.to_checksum_address(address.lower()), [ collateralcoin ], [ indexcoin], [is_long]).call()
    return position

# Check the balance in the user's wallet
def check_balance(coin):
    if (coin == "btc"):
        balanz = btc_contract.caller().balanceOf( Web3.to_checksum_address(account.address)) / (10 ** 8)
    elif (coin == "eth"):
        balanz = arbiw3.eth.get_balance( Web3.to_checksum_address(account.address))  / (10 ** 18)
    if (coin == "weth"):
        balanz = weth_contract.caller().balanceOf( Web3.to_checksum_address(account.address)) / (10 ** 18)
    elif (coin == "usdt"):
        balanz = usdt_contract.caller().balanceOf( Web3.to_checksum_address(account.address)) / (10 ** 6)
    elif (coin == "usdc"):
        balanz = usdc_contract.caller().balanceOf( Web3.to_checksum_address(account.address)) / (10 ** 6)
    print(coin, " wallet balance: ", balanz)
    return balanz

# Retrieve current weight of coins in GMX vault (i.e. in GLP)
def retrieve_allocation():
    #eth_balance = arbiw3.eth.get_balance(Web3.to_checksum_address(gmx_vault.lower()))
    usdc_balance = usdc_contract.caller().balanceOf( Web3.to_checksum_address(gmx_vault.lower())) / (10 ** 6)
    weth_balance = weth_contract.caller().balanceOf( Web3.to_checksum_address(gmx_vault.lower())) / (10 ** 18)
    btc_balance = btc_contract.caller().balanceOf( Web3.to_checksum_address(gmx_vault.lower())) / (10 ** 8)
    usdt_balance = usdt_contract.caller().balanceOf( Web3.to_checksum_address(gmx_vault.lower())) / (10 ** 6)

    return [usdc_balance, weth_balance, btc_balance, usdt_balance]

# Retrieve balance directly from the vault contract
# It returns the same as retrieve_allocation, except we're looking at the vault contract for the token address, instead of looking at the token contract for the vault's address
def token_balances():
    balance = vault_contract.functions.tokenBalances(Web3.to_checksum_address(weth.lower())).call() / (10 ** 18)
    return balance

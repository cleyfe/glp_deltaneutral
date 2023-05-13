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
#private_key = os.environ.get("MAIN_PK")
#assert private_key is not None, "You must set MAIN_PK environment variable"
#assert private_key.startswith("0x"), "Private key must start with 0x hex prefix"

#account: LocalAccount = Account.from_key(private_key)
#arbiw3.middleware_onion.add(construct_sign_and_send_raw_middleware(account))
#arbiw3.eth.default_account = account.address
#print("Your hot wallet address is " , arbiw3.eth.default_account)


# Addresses (Used only as a reference. The contracts used are dynamically fetched using the wl_token_address function)
AddressZero = "0x0000000000000000000000000000000000000000"
weth = "0x82af49447d8a07e3bd95bd0d56f35241523fbab1"
btc = "0x2f2a2543b76a4166549f7aab2e75bef0aefc5b0f"
usdc = "0xff970a61a04b1ca14834a43f5de4533ebddb5cc8"
usdt = "0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9"
link = "0xf97f4df75117a78c1a5a0dbb814af92458539fb4"
uni = "0xfa7f8980b0f1e64a2062791cc3b0871572f1f7f0"
mim = "0xFEa7a6a0B346362BF88A9e4A88416B77a57D6c2A"
frax = "0x17FC002b466eEc40DaE837Fc4bE5c67993ddBd6F"
dai = "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1"
gmx_vault = "0x489ee077994B6658eAfA855C308275EAd8097C4A"
gmx_router = "0xaBBc5F99639c9B6bCb58544ddf04EFA6802F4064"
gmx_reader = "0x22199a49A999c351eF7927602CFB187ec3cae489"
gmx_orderbook = "0x09f77E8A13De9a35a7231028187e9fD5DB8a2ACB"
gmx_position_router = "0x3D6bA331e3D9702C5e8A8d254e5d8a285F223aba"
chainlink_btc_addr = "0x6ce185860a4963106506C203335A2910413708e9"
chainlink_eth_addr = "0x639Fe6ab55C921f74e7fac1ee960C0B6293ba612"
chainlink_link_addr = "0x86E53CF1B870786351Da77A57575e79CB55812CB"
chainlink_uni_addr = "0x9C917083fDb403ab5ADbEC26Ee294f6EcAda2720"
chainlink_dai_addr = "0xc5C8E77B397E531B8EC06BFb0048328B30E9eCfB"
chainlink_usdc_addr = "0x50834F3163758fcC1Df9973b6e91f0F0F0434aD3"
chainlink_usdt_addr = "0x3f3f5dF88dC9F13eac63DF89EC16ef6e7E25DdE7"
chainlink_mim_addr = "0x87121F6c9A9F6E90E59591E4Cf4804873f54A95b"
chainlink_frax_addr = "0x0809E3d38d1B4214958faf06D8b1B1a2b73f2ab8"


# Contracts
weth_contract = arbiw3.eth.contract(address=Web3.to_checksum_address(weth.lower()), abi=abis.ERC20)
btc_contract = arbiw3.eth.contract(address=Web3.to_checksum_address(btc.lower()), abi=abis.ERC20)
usdc_contract = arbiw3.eth.contract(address=Web3.to_checksum_address(usdc.lower()), abi=abis.ERC20)
usdt_contract = arbiw3.eth.contract(address=Web3.to_checksum_address(usdt.lower()), abi=abis.ERC20)
link_contract = arbiw3.eth.contract(address=Web3.to_checksum_address(link.lower()), abi=abis.ERC20)
uni_contract = arbiw3.eth.contract(address=Web3.to_checksum_address(uni.lower()), abi=abis.ERC20)
mim_contract = arbiw3.eth.contract(address=Web3.to_checksum_address(mim.lower()), abi=abis.ERC20)
frax_contract = arbiw3.eth.contract(address=Web3.to_checksum_address(frax.lower()), abi=abis.ERC20)
dai_contract = arbiw3.eth.contract(address=Web3.to_checksum_address(dai.lower()), abi=abis.ERC20)
vault_contract = arbiw3.eth.contract(address=gmx_vault, abi=abis.GMX_VAULT)
reader_contract = arbiw3.eth.contract(address=gmx_reader, abi=abis.GMX_READER)
orderbook_contract = arbiw3.eth.contract(address=gmx_orderbook, abi=abis.GMX_ORDERBOOK)
position_router_contract = arbiw3.eth.contract(address=gmx_position_router, abi=abis.GMX_POSITION_ROUTER)
chainlink_btc_contract = arbiw3.eth.contract(address=chainlink_btc_addr, abi=abis.CHAINLINK)
chainlink_eth_contract = arbiw3.eth.contract(address=chainlink_eth_addr, abi=abis.CHAINLINK)
chainlink_link_contract = arbiw3.eth.contract(address=chainlink_link_addr, abi=abis.CHAINLINK)
chainlink_uni_contract = arbiw3.eth.contract(address=chainlink_uni_addr, abi=abis.CHAINLINK)
chainlink_dai_contract = arbiw3.eth.contract(address=chainlink_dai_addr, abi=abis.CHAINLINK)
chainlink_usdc_contract = arbiw3.eth.contract(address=chainlink_usdc_addr, abi=abis.CHAINLINK)
chainlink_usdt_contract = arbiw3.eth.contract(address=chainlink_usdt_addr, abi=abis.CHAINLINK)
chainlink_mim_contract = arbiw3.eth.contract(address=chainlink_mim_addr, abi=abis.CHAINLINK)
chainlink_frax_contract = arbiw3.eth.contract(address=chainlink_frax_addr, abi=abis.CHAINLINK)

# Chainlink datafeed to get current price of tokens
def getPrice(coin):
    match coin:

        case "btc":
            latestData = chainlink_btc_contract.functions.latestRoundData().call()

        case "eth":
            latestData = chainlink_eth_contract.functions.latestRoundData().call()
        
        case "link":
            latestData = chainlink_link_contract.functions.latestRoundData().call()

        case "uni":
            latestData = chainlink_uni_contract.functions.latestRoundData().call()

        case "dai":
            latestData = chainlink_dai_contract.functions.latestRoundData().call()

        case "usdc":
            latestData = chainlink_usdc_contract.functions.latestRoundData().call()

        case "usdt":
            latestData = chainlink_usdt_contract.functions.latestRoundData().call()

        case "mim":
            latestData = chainlink_mim_contract.functions.latestRoundData().call()

        case "frax":
            latestData = chainlink_frax_contract.functions.latestRoundData().call()

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


## IVault contract functions
# Retrieve balance directly from the vault contract
# It returns the same as retrieve_allocation, except we're looking at the vault contract for the token address, instead of looking at the token contract for the vault's address
def token_balances():
    balance = vault_contract.functions.tokenBalances(Web3.to_checksum_address(weth.lower())).call() / (10 ** 18)
    return balance

# Returns the number of tokens whitelisted in the vault
def wl_tokens():
    nr_tokens = vault_contract.functions.allWhitelistedTokensLength().call()
    return nr_tokens

# Returns the address of the designated token and whether it is a stablecoin
def wl_token_address(i):
    token_address = vault_contract.functions.allWhitelistedTokens(i).call()
    is_stable = vault_contract.functions.stableTokens(token_address).call()
    return token_address, is_stable

# Returns the USD amount of a token in the vault
def pool_amounts(address):
    pool_amounts = vault_contract.functions.poolAmounts(address).call()
    decimals = vault_contract.functions.tokenDecimals(address).call()
    return pool_amounts / 10 ** decimals

def token_weights(address):
    token_weights = vault_contract.functions.tokenWeights(address).call()
    return token_weights / 100
    
def get_price(address):
    prices = reader_contract.functions.getPrices( Web3.to_checksum_address(gmx_reader.lower()), [ Web3.to_checksum_address(address.lower()) ] ).call()
    return prices
    
# Fetch aave borrow and lending rates and collateral ratios
from web3 import Web3
import abis
from dotenv import load_dotenv
load_dotenv()
import os

RAY = 10**27
SECONDS_PER_YEAR = 31536000

# Providers
# Arbitrum Provider (e.g. Infura)
arbiw3 = Web3(Web3.HTTPProvider(os.getenv("INFURA_ARBI")))
print( "Connected Successfully to Web 3 Provider (Aave.py)" if arbiw3.is_connected() else  "Web3 Provider Error")


# Addresses (https://docs.aave.com/developers/deployed-contracts/v3-mainnet/arbitrum)
# Fetch automatically the addresses from the registry 
aave_pool = "0x794a61358D6845594F94dc1DB02A252b5b4814aD"
aave_pool_address_provider = '0xa97684ead0e402dC232d5A977953DF7ECBaB3CDb'
aave_pool_address_provider_registry = '0x770ef9f4fe897e59daCc474EF11238303F9552b6'
aave_pool_data_provider = '0x69FA688f1Dc47d4B5d8029D5a35FB7a548310654'

# Contracts
pool_contract = arbiw3.eth.contract(address=aave_pool, abi=abis.AAVE_POOL)
data_provider = arbiw3.eth.contract(address=aave_pool_data_provider, abi=abis.AAVE_POOL_DATA_PROVIDER)


## Pool Data Provide contract functions
def reserve_tokens():
    tokens = data_provider.functions.getAllReservesTokens().call()

    reserve_config = {}
    reserve_data = {}

    for coin in tokens:
        coin_config = data_provider.functions.getReserveConfigurationData(coin[1]).call()

        reserve_config[coin[0]] = {
            "Name": coin[0],
            "Address": coin[1],
            "Decimals": coin_config[0],
            "LTV": coin_config[1] / 100,
            "Liquidation": coin_config[2] / 100,
            "Bonus": coin_config[3] / 100,
            "Reserve": coin_config[4] / 100,
            "Collateral": coin_config[5], #Boolean
            "Borrowing": coin_config[6], #Boolean
            "StableRate": coin_config[7], #Boolean
            "ReserveActive": coin_config[8], #Boolean
            "ReserveFrozen": coin_config[9], #Boolean
        }

        coin_data = data_provider.functions.getReserveData(coin[1]).call()        
        reserve_caps = data_provider.functions.getReserveCaps(coin[1]).call()

        reserve_data[coin[0]] = {
            "Name": coin[0],
            "Address": coin[1], 
            "borrowCap": reserve_caps[0], # Maximum borrow amount in units of tokens. Will always be lower than the supply caps
            "supplyCap": reserve_caps[1], # Maximum supply amount in units of tokens (e.g. 1000 BTC)
            "unbacked": coin_data[0],
            "accruedToTreasuryScaled": coin_data[1],
            "totalAToken": coin_data[2] / 10**reserve_config[coin[0]]['Decimals'], # The current amount supplied, in units of tokens (e.g. 1000 BTC)
            "totalStableDebt": coin_data[3] / 10**reserve_config[coin[0]]['Decimals'],
            "totalVariableDebt": coin_data[4] / 10**reserve_config[coin[0]]['Decimals'],
            "liquidityRate": coin_data[5] / RAY, # Supply APY
            "variableBorrowRate": coin_data[6] / RAY, # Variable borrow interest rate
            "stableBorrowRate": coin_data[7] / RAY, # Stable borrow interest rate
            "averageStableBorrowRate": coin_data[8] / RAY,
            "liquidityIndex": coin_data[9],
            "variableBorrowIndex": coin_data[10],
            "lastUpdateTimestamp": coin_data[11],
        }

        #reserve_data[coin[0]]["UtilisationRate"]: (reserve_data[coin[0]]['totalVariableDebt'] + reserve_data[coin[0]]['totalStableDebt']) / reserve_data[coin[0]]['totalATokenSupply']


        
    return reserve_config, reserve_data
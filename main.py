import gmx
import aave
import pandas as pd

# Warning: this function is not dynamic. Error would arise if GMX adds new tokens to its whitelist!!
# Warning 2: which oracle should we use? Chainlink or Gmx's or Aave's?
def match_chainlink_price(address):
    match address.lower():
        case '0x82af49447d8a07e3bd95bd0d56f35241523fbab1': #weth
            price = eth_price
            symbol = 'weth'

        case '0x2f2a2543b76a4166549f7aab2e75bef0aefc5b0f': #btc
            price = btc_price
            symbol = 'btc'

        case '0xf97f4df75117a78c1a5a0dbb814af92458539fb4': #link
            price = link_price
            symbol = 'link'

        case '0xfa7f8980b0f1e64a2062791cc3b0871572f1f7f0': #uni
            price = uni_price
            symbol = 'uni'

        case '0xda10009cbd5d07dd0cecc66161fc93d7c9000da1': #dai
            price = dai_price
            symbol = 'dai'

        case '0xff970a61a04b1ca14834a43f5de4533ebddb5cc8': #usdc
            price = usdc_price
            symbol = 'usdc'

        case '0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9': #usdt
            price = usdt_price
            symbol = 'usdt'

        case '0xfea7a6a0b346362bf88a9e4a88416b77a57d6c2a': #mim
            price = mim_price
            symbol = 'mim'

        case '0x17fc002b466eec40dae837fc4be5c67993ddbd6f': #frax
            price = frax_price
            symbol = 'frax'

        case _:
            print("ERROR: A token was not matched by a chainlink data feed")
    
    return price, symbol


#######################################################
# Get current tokens prices
#######################################################
btc_price = gmx.getPrice("btc")
eth_price = gmx.getPrice("eth")
link_price = gmx.getPrice("link")
uni_price = gmx.getPrice("uni")
dai_price = gmx.getPrice("dai")
usdc_price = gmx.getPrice("usdc")
usdt_price = gmx.getPrice("usdt")
mim_price = gmx.getPrice("mim")
frax_price = gmx.getPrice("frax")


######################################################
#Get GLP vault allocations
#######################################################
# 1) Determine the number of tokens that are whitelisted by GMX protocol
# 2) Get the address of each whitelisted token and whether it is a stablecoin
# 3) Get the quantity of the token in the GLP vault
# 4) Get the token price from Chainlink feed
# 5) Get the current weight of each token in the vault by multiplying Q*P and dividing by the total USD amount in the vault
# 6) Identify hedging needs

# 1) Determine the number of tokens that are whitelisted by GMX protocol
nr_wl_tokens = gmx.wl_tokens()

glp_data = {}

for i in range(0, nr_wl_tokens):
    # 2) Get the address of each whitelisted token and whether it is a stablecoin
    address, stable = gmx.wl_token_address(i)
    # 3) Get the quantity of the token in the GLP vault
    quantity = gmx.pool_amounts(address)
    # 4) Get the token price from Chainlink feed
    token_price, symbol = match_chainlink_price(address)
    glp_data[symbol] = {
        'Address': address,
        'Stable': stable,
        'Price': token_price,
        'Quantity': quantity,
        'TVL': quantity * token_price,
        'targetWeight': gmx.token_weights(address) / 10
    }        

# 5) Get the current weight of each token in the vault by multiplying Q*P and dividing by the total USD amount in the vault
glp_tvl = sum(coin['TVL'] for coin in glp_data.values())

for coin in glp_data.values():
    coin['Weight'] = coin['TVL'] / glp_tvl



#######################################################
# Get Aave reserve assets data
#######################################################
reserve_config, reserve_data = aave.reserve_tokens()

#######################################################
# Calculate the necessary inputs to compute final weights and orders
#######################################################
df_inputs = pd.DataFrame(columns=['gmx_weight', 'ltv', 'borrow_r', 'supply_r'])
stablecoins_percentage = 1

for coin in glp_data.values():
    asset_in_aave = False #Check if the asset is available on Aave

    # Not Stable? To be hedged --> Fetch borrow rates
    if not coin['Stable']:
        print(f"Hedge {coin['Weight']} of {coin['Address']}")
        stablecoins_percentage -= coin['Weight']
        for a in reserve_data.values():
            if a['Address'] == coin['Address']:
                print()
                asset_in_aave = True
                df_inputs.loc[coin['Address']] = [coin['Weight'],"-",a['variableBorrowRate'],"-"]


        if not asset_in_aave:
            print("Token to be hedged is not available to supply in Aave")
            df_inputs.loc[coin['Address']] = [coin['Weight'],"-","-","-"]


    # Stable? Check if available in Aave and if can be used as collateral --> Fetch supply rate and LTV
    else:
        print(f"Check if {coin['Address']} is available to supply on Aave")
        for a in reserve_config.values():
            if a['Address'] == coin['Address']:
                if a['Collateral']:
                    for b in reserve_data.values():
                        if b['Address'] == coin['Address']:
                            df_inputs.loc[coin['Address']] = [coin['Weight'],a['LTV']/100,"-",b['liquidityRate']]
                            asset_in_aave = True
                
                else:
                    df_inputs.loc[coin['Address']] = [coin['Weight'],"-","-","-"]
                    print("Stablecoin is not available as a collateral in Aave")

        if not asset_in_aave:
            df_inputs.loc[coin['Address']] = [coin['Weight'],"-","-","-"]
            print("Stablecoin is not available to supply in Aave")


print(df_inputs)
adjustment_factor = 1 / (1-stablecoins_percentage)
stable_aave_weight = df_inputs[df_inputs['ltv'] != '-']['gmx_weight'].sum()
avg_ltv = (df_inputs[df_inputs['ltv'] != '-']['gmx_weight'] * df_inputs[df_inputs['ltv'] != '-']['ltv']).sum() / stable_aave_weight
safe_ltv = 0.8 * avg_ltv
borrow_cost = (df_inputs[df_inputs['borrow_r'] != '-']['gmx_weight'] * df_inputs[df_inputs['borrow_r'] != '-']['borrow_r']).sum()
supply_profit = (df_inputs[df_inputs['supply_r'] != '-']['gmx_weight'] * df_inputs[df_inputs['supply_r'] != '-']['supply_r']).sum()  

# print('Stable %:', stablecoins_percentage)
# print('Adjustment factor:', adjustment_factor)
# print('Average LTV:', avg_ltv)
# print('Safe LTV weight:', safe_ltv)
# print('Borrow APY:', borrow_cost)
# print('Supply APY:', supply_profit)


#######################################################
# Compute weights to be allocated to GMX and Aave
#######################################################
# AuM % in Aave (aave_w) = 1 / (1 + LTV * (1/hw)); hw is the weight to be hedged away, i.e. 1 - stablecoins_percentage
# AuM % in GMX (gmx_w) = 1 - aave_w

hw = 1 - stablecoins_percentage
aave_w = 1 / (1 + safe_ltv * (1/hw))
gmx_w = 1 - aave_w

print("Aave weight:", aave_w)
print("GMX weight:", gmx_w)


#######################################################
# Prepare orders
#######################################################


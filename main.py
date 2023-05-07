import gmx

# Warning: this function is not dynamic if GMX adds new tokens to its whitelist!! (It will return an error)
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
## Easy method but not dynamic:
#glp_alloc = gmx.retrieve_allocation()
#print(glp_alloc)

## Dynamic method: 
# 1) Determine the number of tokens that are whitelisted by GMX protocol
# 2) Get the address of each whitelisted token and whether it is a stablecoin
# 3) Get the quantity of the token in the GLP vault
# 4) Get the token price from Chainlink feed
# 5) Get the current weight of each token in the vault by multiplying Q*P and dividing by the total USD amount in the vault

# 1) Determine the number of tokens that are whitelisted by GMX protocol
nr_wl_tokens = gmx.wl_tokens()

glp_data = {}

for i in range(0, nr_wl_tokens):
    # 2) Get the address of each whitelisted token and whether it is a stablecoin
    address, stable = gmx.wl_token_address(i)
    print("Token " + str(i) + ":", address)
    print("Stablecoin:", stable)
    # 3) Get the quantity of the token in the GLP vault
    quantity = gmx.pool_amounts(address)
    print("Quantity in the vault:", quantity)
    #print("Target weight:", gmx.token_weights(address), "\n")

    # 4) Get the token price from Chainlink feed
    token_price, symbol = match_chainlink_price(address)
    print("Token price:", token_price)
    print("USD amount in the vault:", quantity * token_price, "\n")
    glp_data[symbol] = {
        'Address': address,
        'Price': token_price,
        'Quantity': quantity,
        'TVL': quantity * token_price
    }        

# 5) Get the current weight of each token in the vault by multiplying Q*P and dividing by the total USD amount in the vault
glp_tvl = sum(coin['TVL'] for coin in glp_data.values())
print("Total GLP TVL:", glp_tvl)

for coin in glp_data.values():
    coin['Weight'] = coin['TVL'] / glp_tvl

print(glp_data)




#######################################################
# Get user's wallet balances
#######################################################
# btc_balance = gmx.check_balance("btc")
# print("BTC price:", btc_price, "BTC balance:", btc_balance)
# eth_balance = gmx.check_balance("eth")
# print("ETH price:", eth_price, "ETH balance:", eth_balance)
# weth_balance = gmx.check_balance("weth")
# print("WETH balance:", weth_balance)
# usdc_balance  = gmx.check_balance("usdc")
# udst_balance = gmx.check_balance("usdt")

#######################################################
# Get GLP vault user's postions
#######################################################

#gmx.lookupPositions(gmx.account.address, "btc")
#gmx.lookupPositions(gmx.account.address, "eth")

#current_pos = gmx.getPosition( gmx.account.address, "eth", "weth", True)
#print(current_pos)


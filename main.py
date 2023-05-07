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
    print("Token:", address)
    print("Stablecoin:", stable)
    # 3) Get the quantity of the token in the GLP vault
    quantity = gmx.pool_amounts(address)
    print("Quantity in the vault:", quantity)
    #print("Target weight:", gmx.token_weights(address), "\n")

    # 4) Get the token price from Chainlink feed
    if not stable:
        token_price, symbol = match_chainlink_price(address)
        print("Token price:", token_price)
        print("USD amount in the vault:", quantity * token_price, "\n")
        glp_data[symbol] = {
            'Address': address,
            'Price': token_price,
            'Quantity': quantity,
            'TVL': quantity * token_price
        }

    else:
        print("USD amount in the vault:", quantity, "\n") #stable assumed to be $1
        glp_data[symbol] = {
            'Address': address,
            'Price': 1,
            'Quantity': quantity,
            'TVL': quantity * token_price
        }
        

print(glp_data)
glp_tvl = sum(coin['TVL'] for coin in glp_data.values())

print("Total GLP TVL:", glp_tvl)





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


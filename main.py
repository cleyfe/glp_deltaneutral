import gmx

#######################################################
# Get current tokens prices
#######################################################
# btc_price = gmx.getPrice("btc")
# eth_price = gmx.getPrice("eth")

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

######################################################
#Get GLP vault allocations
#######################################################
glp_alloc = gmx.retrieve_allocation()
print(glp_alloc)


weth_balance = gmx.token_balances()
print("wETH balance in the vault:", weth_balance)
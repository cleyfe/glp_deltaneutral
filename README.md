## GLP Delta Neutral strategy
This is a WiP! Use at your own risk!

# Installation
Install depedencies with the following command: pip: -r requirements.txt

Create an API Key on infura. Don't forget to activate the Arbitrum network. Infura asks for credit card details but the service is free. Use a temporary card if you wish to.  

You must create a .env file in your local folder with two variables:
INFURA_ARBI = "YOUR_INFURA_API_KEY"
MAIN_PK = "YOUR_WALLET_PRIVATE_KEY"

# Codebase
gmx.py is a utility library for fetching data on GMX-related contracts
aave.py is a utility library for fetching data on AAVE-related contracts
main.py fetches data from both protocols and computes the necessary inputs to perform a delta-neutral strategy

# Welcomed contributions
The code requires the following adjustments:
- Oracle: should either 1) switch Chainlink to GMX or Aave Oracles, or 2) improve the match_chainlink_price function so that the function is dynamic in case GMX or Aave add/delete tokens in their whitelist. As of today, these changes would not be reflected and the function would return an error

- Aave: fetch automatically the contract addresses using the provider registry, instead of hard coding them

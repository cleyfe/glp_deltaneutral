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

main.py is an example of calls of some of the functions in the gmx.py file 

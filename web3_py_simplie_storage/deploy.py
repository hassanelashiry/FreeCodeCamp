from solcx import compile_standard, install_solc #"install_solc" to solve compile_sol error
install_solc("0.6.0") 

import json
from web3 import Web3

import os ## access evn variable using python "os.getenv("PRIVATE_KEY")"
from dotenv import load_dotenv # another way to set the environment

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()


#compile our solidity code

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*":{"*" : ["abi", " metadata","evm.bytecode", "evm.sourceMap"]}
            }
        },

    },

    solc_version ="0.6.0",
)

# print (compiled_sol) ## to print BYTE CODE
# Create comiled_code.json
"""
# get abi
with open ("compiled_code.json","w")as file:
    json.dump(compiled_sol,file) # take compiled_sol json variabe and dump it in compiled_sol.json
"""

###########################################################
# *** To deploy the contract we need bytecode and ABI *** #
###########################################################

# Get bytecode
bytecode = compiled_sol ["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]
["bytecode"]
["object"] # access object through contracts/simpleStorage.sol/Si.../object 

# Get abi
abi = compiled_sol ["contracts"]["SimpleStorage.sol"]["SimpleStorage"]
["abi"]
# print (abi)  ## TO print ABI

#*******************************************************#
    # Connect with Ganache (local blockchain network)
#*******************************************************#

# Connect with local host : http://localhost:ganache_port
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
chain_id=5777 # Add chain id = network id
# Using first address in Ganache
my_address= "0xca57a53e805dA11530b7D1aB7C01cc7F0b923E09" 
# Its private key | to import private key from python 
# you should add "0x" at the first of key becuase python ignore it
private_key = "0x7c98e3a2b7e43bf0d8ef577e0f68bc56b3b7726a7a8d5d0d022223b99365a86e"
#private_key = os.getenv("PRIVATE_KEY")
#print (private_key)

# Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi , bytecode=bytecode)
# print (SimpleStorage)

# Get the leastest transaction
nonce = w3.eth.get_transaction_count(my_address)
#print (nonce)

# To build a transaction we need 
#       1- sign the transaction
#       2- send the transaction

transaction = SimpleStorage.constructor().build_transaction(
    {"chainId": chain_id, "from":my_address, "nonce": nonce}
)
#print (transaction)

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

from brownie import accounts, config, SimpleStorage

def deploy_simple_storage():
        ## *****  use testnet account ***** ##
    # account = accounts.load("MyMetaMuskAccount")
    # print (account)

        ## ***** use local accounts from Ganache ***** ##
    # account = accounts[0]
    # print (account)  

    account= accounts.add(config["wallets"]["from_key"])
    simple_storage = SimpleStorage.deploy({"from": account}) # what is the account which deploy it
    # deploy without needing ABI, bytecode or nonce
    # tansaction or call
    stored_value = simple_storage.retrieve()
    print (stored_value)
    transaction = simple_storage.store(15, {"from": account})
    transaction.wait(1)
    print ("processing...")
    updated_store_value = simple_storage.retrieve()
    print ("updating...")
    print(updated_store_value)
    print ("updated...")




def main():
    deploy_simple_storage()
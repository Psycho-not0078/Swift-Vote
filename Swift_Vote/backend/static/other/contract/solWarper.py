import solcx
import web3
from web3.main import Web3
from web3.auto import w3

import os
from frontend.models import *

from web3 import Web3
# from eth_tester import PyEVMBackend
from solcx import compile_source

def compile_source_file(file_path):
   with open(file_path, 'r') as f:
      source = f.read()

   return compile_source(source)


def deploy_contract(w3, contract_interface):
    tx_hash = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin']).constructor().transact()

    address = w3.eth.get_transaction_receipt(tx_hash)['contractAddress']
    return address

def __init__():
    w3 = Web3("http:127.0.0.1:8545/")

    contract_source_path = 'contract.sol'
    compiled_sol = compile_source_file('/home/psych/github_related_stuff/Swift-Vote/Swift_Vote/backend/static/other/contract/contract.sol')

    contract_id, contract_interface = compiled_sol.popitem()

    # print(deploy_contract(w3, contract_interface))
    address = deploy_contract(w3, contract_interface)

    if (w3.eth.get_accounts()[0]):
        masterAccount = w3.eth.get_accounts()[0];
        temp = w3.eth.contract(bytecode=bytecode, abi=abi)
        txn = temp.constructor().buildTransaction({"from": masterAccount}); 

    else:
        masterAccount=W3.eth.account.create(os.urandom(32))
        newaccount=Accounts("official",masterAccount.address,masterAccount.privateKey)
        newaccount.save()

        


    
    
def createAccount(type):
    newAccount=W3.eth.account.create(os.urandom(32))
    accAddress=newAccount.address
    accPrivatekey=newAccount.privateKey
    accountType=type
    newaccount=Accounts(accountType,accAddress,accPrivatekey)
    newaccount.save()
    
def vote(addr, id, location, date):
    if (Accounts.objects.filter('accountAddress'==addr)["ablitytoVote"]==1):
        print("vote")#will put the appropriate function call for voting here
             
    


        
# print(out)
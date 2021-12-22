from logging import exception
import web3
from solcx import compile_source
import random

# print(w3.personal.listAccounts, len(w3.personal.listAccounts))
w3 = web3.Web3(web3.HTTPProvider("http://127.0.0.1:8545"))

def compile_source_file(file_path):
   with open(file_path, 'r') as f:
      source = f.read()

   return compile_source(source)


def deploy_contract(file_name):
    compiled_sol = compile_source_file(file_name)
    contract_id, contract_interface = compiled_sol.popitem()
    contract = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin'])

    contract_hash=contract.constructor().transact({'from': w3.personal.listAccounts[0]})
    address = w3.eth.waitForTransactionReceipt(contract_hash)['contractAddress']
    contract_handle=w3.eth.contract(address=address,abi=contract_interface['abi'])

    return contract_handle

def addUser(contract_handle, location):
    try:
        newAddress=w3.personal.newAccount("awefarw")
        hsh=contract_handle.functions.addUser(newAddress,location).transact({"from":w3.personal.listAccounts[0]})
        #print(hsh)
    except Exception as e:
        print(e)

def vote(contract_handle, addr, cid, location, date):
    try:
        hsh=contract_handle.functions.vote(cid, location, date).transact({'from':addr})
    except Exception as e:
        print(e)

def addCandidate(contract_handle, name, location):
    try:
        hsh=contract_handle.functions.addCandidate(name,location).transact({"from":w3.personal.listAccounts[0]})
    except Exception as e:
        print(e)

def listVoters(contract_handle):
    try:
        addresses=contract_handle.functions.listVoters().call()
        print(type(addresses))
        return addresses[1]
    except Exception as e:
        print(e)

contract_source_path = 'elections.sol'

contract_handle= deploy_contract(contract_source_path)
addUser(contract_handle,"fucklife")
listVoters(contract_handle)
# txinfo=w3.eth.getTransaction(contract_tester1)
# print(txinfo)
# print(f'Deployed {contract_id} to: {address}\n')





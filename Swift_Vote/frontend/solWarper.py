from logging import exception
import web3
from solcx import compile_source
import random

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
    newAddress=w3.personal.newAccount("awefarw")
    hsh=contract_handle.functions.addUser(newAddress,location).transact({"from":w3.personal.listAccounts[0]})
    print(hsh)

def vote(contract_handle, addr, cid, location, date):
    hsh=contract_handle.functions.vote(cid, location, date).transact({'from':addr})

def voteCount(contract_handle, cid):
    ret=contract_handle.functions.countVote(cid).call()
    return ret[1]

#adding start
def addCandidate(contract_handle, name, location):
    hsh=contract_handle.functions.addCandidate(name,location).transact({"from":w3.personal.listAccounts[0]})

def listVoters(contract_handle):
    addresses=contract_handle.functions.listVoters().call()
    # print(type(addresses))
    return addresses
#adding closex

def listCandidates(contract_handle, location):
    ret=contract_handle.functions.listCandidates(location).call()
    return ret

def listOfficials(contract_handle):
    ret=contract_handle.functions.listOfficials().call()
    return ret

def changeAblity(contract_handle,address,ablityType,Val):
    contract_handle.functions.changeAblity(address,ablityType,Val).transact({'from': w3.personal.listAccounts[0]})


# contract_source_path = 'elections.sol'

# contract_handle= deploy_contract(contract_source_path)
# addUser(contract_handle,"fucklife")
# addUser(contract_handle,"awdeferg")
# addUser(contract_handle,"fucklasewrgife")

# addCandidate(contract_handle,"qwerty","1")
# addCandidate(contract_handle,"qwerty2","1")

# a=listCandidates(contract_handle,"1")
# print(a)

# v1="0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
# changeAblity(contract_handle,v1,2,1)
# changeAblity(contract_handle,v1,3,1)

# a=listVoters(contract_handle)
# print(a)
# a=listOfficials(contract_handle)
# print(a)
# txinfo=w3.eth.getTransaction(contract_tester1)
# print(txinfo)
# print(f'Deployed {contract_id} to: {address}\n')





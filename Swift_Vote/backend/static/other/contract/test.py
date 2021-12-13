import sys
import time
import pprint


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


w3 = Web3("http:127.0.0.1:8545/")

contract_source_path = 'contract.sol'
compiled_sol = compile_source_file('/home/psych/github_related_stuff/Swift-Vote/Swift_Vote/backend/static/other/contract/contract.sol')

contract_id, contract_interface = compiled_sol.popitem()

# print(deploy_contract(w3, contract_interface))
address = deploy_contract(w3, contract_interface)
print(f'Deployed {contract_id} to: {address}\n')

store_var_contract = w3.eth.contract(address=address, abi=contract_interface["abi"])

gas_estimate = store_var_contract.functions.setVar(255).estimateGas()
print(f'Gas estimate to transact with setVar: {gas_estimate}')

if gas_estimate < 100000:
     print("Sending transaction to setVar(255)\n")
     tx_hash = store_var_contract.functions.setVar(255).transact()
     receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
     print("Transaction receipt mined:")
     pprint.pprint(dict(receipt))
     print("\nWas transaction successful?")
     pprint.pprint(receipt["status"])
else:
     print("Gas cost exceeds 100000")
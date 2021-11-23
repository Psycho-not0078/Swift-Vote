import solcx
import web3
from web3.main import Web3
out=solcx.compile_files(
    ["/home/psych/github_related_stuff/Swift-Vote/Swift_Vote/backend/static/other/contract/elections.sol"],
    output_values=["abi","bin"]
)
contract_id, contract_interface=out.popitem()
# print(contract_interface['bin'])
abi=contract_interface['abi']
bytecode=contract_interface['bin']
w3=Web3("http:127.0.0.1:8545/")



# class solWarper():
    
# print(out)
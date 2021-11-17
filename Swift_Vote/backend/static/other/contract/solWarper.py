import solcx
import web3
source = "./contract.sol"
file = "counter.sol"
spec = {
            "language": "Solidity",
            "sources": {
                file: {
                    "urls": [source]
                }
            },
            "settings": {
                "optimizer": {
                        "enabled": True
                    },
                "outputSelection": {
                        "*": {"*": ["metadata", "evm.bytecode", "abi"]}
                }
            }
        }
out = solcx.compile_standard(spec, allow_paths=".")

w3 = web3.Web3(web3.HTTPProvider("http://127.0.0.1:8545"))
from web3.middleware import geth_poa_middleware
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
print(w3.isConnected())


# print(out)
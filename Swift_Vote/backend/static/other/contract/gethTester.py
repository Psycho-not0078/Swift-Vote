import web3
w3 = web3.Web3(web3.HTTPProvider("http://127.0.0.1:8545"))
print(w3.isConnected())
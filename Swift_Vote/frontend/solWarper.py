from logging import exception
import web3
from web3 import Web3
import solcx
from django.conf import settings
from django.conf.urls.static import static
import os
import ast,json
w3 = web3.Web3(web3.HTTPProvider("http://127.0.0.1:8545"))

def compile_source():
    #cant use the conile files as static files are problematic in nature
    solcx.install_solc()
    source="pragma solidity >=0.7.0 <0.9.0;\
    contract Election {\
        struct vt { \
            uint256 id;\
            uint256 cid;\
            string location;\
            string date;\
        }\
        struct candidate {\
            uint256 id;\
            string name;\
            string location;\
        }\
        struct user {\
            uint256 id;\
            string tag;\
            string location;\
            uint256 ablity_to_vote;\
            uint256 ablity_to_add;\
            uint256 ablity_to_change;\
        }\
    \
        uint256 voteCount;\
        uint256 officialCount;\
        uint256 candidateCount;\
        uint256 userCount;\
        uint256 voterCount;\
    \
        mapping(uint256=>address) userAddress;\
        mapping(address=>user) users;\
        mapping(uint256=>string) candidateNames;\
        mapping(string=>candidate) candidates; \
        mapping(uint256=>vt) votes;\
    \
        constructor(){\
            init(msg.sender);\
        }\
        function init(address _ad) private{\
            userCount+=1;\
            officialCount+=1;\
            userAddress[userCount]=_ad;\
            users[_ad]=user(userCount,'admin','central',0,1,1);\
        }\
        function addUser(address _ad, string memory _location) public{\
            require(users[msg.sender].ablity_to_add==1,'the role doesnt allow it');\
            userCount+=1;\
            voterCount+=1;\
            userAddress[userCount]=_ad;\
            users[_ad]=user(userCount,'user',_location,1,0,0);\
        }\
        function addCandidate( string memory _name, string memory _location) public {\
            require(users[msg.sender].ablity_to_add==1,'the role doesnt allow it');\
            candidateCount+=1;\
            candidateNames[candidateCount]=_name;\
            candidates[candidateNames[candidateCount]]=candidate(candidateCount, _name, _location);\
        }\
        function changeAblity(address _ad, uint256 _ablityType, uint256 _value) public {\
            require(users[msg.sender].ablity_to_change==1,'the role doesnt allow it');\
            if (_ablityType==1){\
                users[_ad].ablity_to_vote=_value;\
            }\
                \
            else if(_ablityType==2){\
                    users[_ad].ablity_to_add=_value;\
                    if (_value==1){\
                        officialCount+=1;\
                    }\
                    else{\
                        officialCount-=1;\
                    }\
                }\
                    \
            else if(_ablityType==3){\
                users[_ad].ablity_to_change=_value;\
                if (_value==1){\
                    officialCount+=1;\
                }\
                else{\
                    officialCount-=1;\
                }\
            }\
        }\
        function disableVoteAblity(address _ad) private{ if (users[_ad].ablity_to_vote==1) {\
                users[_ad].ablity_to_vote=0;\
            }\
        }\
        function listVoters() public view returns (address  [] memory){\
            require(keccak256(bytes(users[msg.sender].tag))==keccak256(bytes('admin')),'the role doesnt allow it');\
            address[] memory addressesses = new address[](voterCount);\
            uint256 i=1;\
            uint256 pos=0;\
            for(i=0;i<=userCount;i++){\
                if(users[userAddress[i+1]].ablity_to_vote==1){\
                    addressesses[pos]=userAddress[i+1];\
                    pos+=1;\
                }\
            }\
            return addressesses;\
        }\
        function listOfficials() public view returns (address  [] memory){\
            require(keccak256(bytes(users[msg.sender].tag))==keccak256(bytes('admin')),'the role doesnt allow it');\
            address[] memory addressesses = new address[](officialCount);\
            uint256 i=1;\
            uint256 pos=0;\
            for(i=1;i<=userCount;i++){\
                if((users[userAddress[i]].ablity_to_add==1 || users[userAddress[i]].ablity_to_change==1) && users[userAddress[i]].ablity_to_vote==0){\
                    addressesses[pos]=userAddress[i];\
                    pos+=1;\
                }\
            }\
            return addressesses;\
        }\
        function listCandidates(string memory _location)public view returns (string[] memory name){\
            require(keccak256(bytes(users[msg.sender].tag))==keccak256(bytes('admin')),'the role doesnt allow it');\
            string[] memory names=new string[](candidateCount);\
            uint256 i=1;\
            uint256 pos=0;\
            for(i=1;i<=candidateCount;i++){\
                if(keccak256(bytes(candidates[candidateNames[i]].location))==keccak256(bytes(_location))){\
                    names[pos]=candidates[candidateNames[i]].name;\
                    pos+=1;\
                }\
            }\
            return names;\
        }\
        function vote(string memory _name, string memory _location,string memory _date) public{\
            require(users[msg.sender].ablity_to_vote==1,'the role doesnt allow it');\
            require(keccak256(bytes(users[msg.sender].tag))==keccak256(bytes('user')),'the role doesnt allow it');\
            require(keccak256(bytes(users[msg.sender].location))==keccak256(bytes(candidates[_name].location)),'error 404');\
            voteCount+=1;\
            uint256 _id=0;\
            uint256 i=1;\
            for(i=1;i<=candidateCount;i++){\
                if (keccak256(bytes(candidateNames[i]))==keccak256(bytes(_name))){\
                    _id=i;\
                }\
            }\
            votes[voteCount]=vt(voteCount, _id, _location, _date);\
            disableVoteAblity(msg.sender);\
        }\
        function countVote(string memory _name) public view returns (uint256 _count){\
            uint256 _vtcount=0;\
            uint256 i=1;\
            uint256 _id=0;\
            uint256 j=1;\
            for(j=1;j<=candidateCount;j++){\
                if (keccak256(bytes(candidateNames[j]))==keccak256(bytes(_name))){\
                    _id=j;\
                }\
            }\
            for(i=1;i<=voteCount;i++){\
                if (votes[i].cid==_id){\
                    _vtcount+=1;\
                }\
            }\
            return _vtcount;\
        }\
        function randomInt(uint256 _limits) private view returns (uint256 _count){\
            uint256 rand = uint256(keccak256(abi.encodePacked(block.difficulty, block.timestamp)));\
            return rand % _limits;\
        }\
        function randomVoter() public view returns (address _ad ){\
            address[] memory avaliableAddresses = listVoters();\
            uint256 limit=uint256(avaliableAddresses.length);\
            return avaliableAddresses[randomInt(limit)];\
        }\
    \
    }"
    return solcx.compile_source(source,output_values=['abi','bin'],solc_version='0.8.11')

def deploy_contract():
    compiled_sol = compile_source()
    contract_id, contract_interface = compiled_sol.popitem()
    contract = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin'])

    contract_hash=contract.constructor().transact({'from': w3.personal.listAccounts[0]})
    address = w3.eth.waitForTransactionReceipt(contract_hash)['contractAddress']
    contract_handle=w3.eth.contract(address=address,abi=contract_interface['abi'])

    return contract_handle

def tobeornottobe():
    # same deploy function 
    # but uses env variables to ensure that the contract isnt redeployed
    address,abi_2=settings.GETENV()
    if (address!=""):#if already deployed
        abi=ast.literal_eval(abi_2)
        try:
            handle=w3.eth.contract(address,abi)
        except exception as e:#if the said address doesnt contain the deployed contract
            print("compiling...")
            compiled_sol = compile_source()
            contract_id, contract_interface = compiled_sol.popitem()
            contract = w3.eth.contract(
                abi=contract_interface['abi'],
                bytecode=contract_interface['bin'])
            contract_hash=contract.constructor().transact({'from': w3.personal.listAccounts[0]})
            print("deployed...")
            address = w3.eth.waitForTransactionReceipt(contract_hash)['contractAddress']
            abi=contract_interface['abi']
            e=settings.SETENV(address,abi)
        print("contract found enabling handler")
    else:# if the contract isnt complied and deployed
        print("compiling...")
        compiled_sol = compile_source()
        contract_id, contract_interface = compiled_sol.popitem()
        contract = w3.eth.contract(
            abi=contract_interface['abi'],
            bytecode=contract_interface['bin'])
        contract_hash=contract.constructor().transact({'from': w3.personal.listAccounts[0]})
        print("deployed...")
        address = w3.eth.waitForTransactionReceipt(contract_hash)['contractAddress']
        abi=contract_interface['abi']
        e=settings.SETENV(address,abi)
        # contract_handle=w3.eth.contract(address=address,abi=contract_interface['abi'])
    contract_handle=w3.eth.contract(address=address,abi=abi)
    return contract_handle
    
def addUser(contract_handle, location):
    try:
        passwd='awefarw'
        newAddress=w3.personal.newAccount(passwd)
        hsh=contract_handle.functions.addUser(newAddress,location).transact({"from":w3.personal.listAccounts[0]})
        # print(w3.eth.getBalance(newAddress))
        w3.eth.sendTransaction({'from':w3.personal.listAccounts[5],'to':newAddress,'value':w3.toWei(1,'ether')})
        w3.personal.unlockAccount(newAddress,passwd)
        return newAddress 
    except Exception as e:
        print(e)

def vote(contract_handle, addr, cname, location, date):
    try:
        if (w3.eth.getBalance(addr)<=20000000000):
            w3.eth.sendTransaction({'from':w3.personal.listAccounts[5],'to':addr,'value':w3.toWei(1,'ether')})
        hsh=contract_handle.functions.vote(cname, location, date).transact({'from':addr})
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
        # print(type(addresses))
        return addresses[1]
    except Exception as e:
        print(e)

def chrandomVoter(contract_handle):
    try:
        address=contract_handle.functions.randomVoter().call()
        return address
    except Exception as e:
        print(e)

def listCandidates(contract_handle,location):
    try:
        Candidates=contract_handle.functions.listCandidates(location).call()
        # print(type(addresses))
        return Candidates
    except Exception as e:
        print(e)

def listOfficials(contract_handle):
    try:
        addresses=contract_handle.functions.listOfficials().call()
        # print(type(addresses))
        return addresses[1]
    except Exception as e:
        print(e)

def countVote(contract_handle, cname):
    try:
        hsh=contract_handle.functions.countVote(cname).call()
        return hsh
    except Exception as e:
        print(e)

def changeAblity(contract_handle, addr, type, value):
    try:
        hsh=contract_handle.functions.changeAblity(addr, type, value).transact({'from': w3.personal.listAccounts[0]})
    except Exception as e:
        print(e)

# handler=tobeornottobe()
# addUser(handler,"qwerty")
# addUser(handler,"werty")
# print(listVoters(handler))
from logging import exception
import web3
import solcx
from django.conf import settings
from django.conf.urls.static import static

# print(w3.personal.listAccounts, len(w3.personal.listAccounts))
w3 = web3.Web3(web3.HTTPProvider("http://127.0.0.1:8545"))
# solcx.install_solc()
# print(solcx.get_solcx_install_folder())

def compile_source():
    solcx.install_solc()
    source="pragma solidity >=0.7.0 <0.9.0;\
    \
    contract Election {\
        struct vt { \
            uint256 id;\
            uint256 cid;\
            string location;\
            string date;\
        }\
        \
        struct candidate {\
            uint256 id;\
            string name;\
            string location;\
        }\
    \
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
        mapping(uint256=>candidate) candidates;\
        mapping(uint256=>vt) votes;\
    \
        constructor(){\
            init(msg.sender);\
        }\
    \
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
    \
    \
        function addCandidate( string memory _name, string memory _location) public {\
            require(users[msg.sender].ablity_to_add==1,'the role doesnt allow it');\
            candidateCount+=1;\
            candidates[candidateCount]=candidate(candidateCount, _name, _location);\
        }\
    \
        function changeAblity(address _ad, uint256 _ablityType, uint256 _value) public {\
            require(users[msg.sender].ablity_to_change==1,'the role doesnt allow it');\
            if (_ablityType==1){\
                users[_ad].ablity_to_vote=_value;\
            }\
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
    \
        function disableVoteAblity(address _ad) private { \
            if (users[_ad].ablity_to_vote==1) {\
                users[_ad].ablity_to_vote=0;\
            }\
        }\
    \
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
    \
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
    \
        function listCandidates(string memory _location)public view returns (string[] memory name, uint256[] memory id){\
            require(keccak256(bytes(users[msg.sender].tag))==keccak256(bytes('user')),'the role doesnt allow it');\
            string[] memory names=new string[](candidateCount);\
            uint256[] memory ids=new uint256[](candidateCount);\
            uint256 i=1;\
            uint256 pos=0;\
            for(i=1;i<=candidateCount;i++){\
                if(keccak256(bytes(candidates[i].location))==keccak256(bytes(_location))){\
                    ids[pos]=candidates[i].id;\
                    names[pos]=candidates[i].name;\
                    pos+=1;\
                }\
            }\
            return (names,ids);\
        }\
    \
        function vote(uint256 _id, string memory _location,string memory _date) public{\
            require(users[msg.sender].ablity_to_vote==1,'the role doesnt allow it');\
            require(keccak256(bytes(users[msg.sender].tag))==keccak256(bytes('user')),'the role doesnt allow it');\
            require(keccak256(bytes(users[msg.sender].location))==keccak256(bytes(candidates[_id].location)),'error 404');\
            voteCount+=1;\
            votes[voteCount]=vt(voteCount, _id, _location, _date);\
            disableVoteAblity(msg.sender);\
        }\
    \
        function countVote(uint256 _id) public view returns (uint256 _count){\
            uint256 _vtcount=0;\
            uint256 i=1;\
            for(i=1;i<=voteCount;i++){\
                if (votes[i].cid==_id){\
                    _vtcount+=1;\
                }\
            }\
            return _vtcount;\
        }\
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

def addUser(contract_handle, location):
    try:
        newAddress=w3.personal.newAccount('awefarw')
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
        # print(type(addresses))
        return addresses[1]
    except Exception as e:
        print(e)

def listCandidates(contract_handle,location):
    try:
        addresses=contract_handle.functions.listCandidates(location).call()
        # print(type(addresses))
        return addresses[1]
    except Exception as e:
        print(e)
# contract_source_path = 'Swift_Vote/static/others/elections.sol'

#contract_handle= deploy_contract()
# addUser(contract_handle,"fucklife")
# print(listVoters(contract_handle))
# txinfo=w3.eth.getTransaction(contract_tester1)
# print(txinfo)
# print(f'Deployed {contract_id} to: {address}\n')





def listOfficials(contract_handle):
    try:
        addresses=contract_handle.functions.listOfficials().call()
        # print(type(addresses))
        return addresses[1]
    except Exception as e:
        print(e)

def countVote(contract_handle, addr, count):
    try:
        hsh=contract_handle.functions.countVote(count).transact({'from':addr})
    except Exception as e:
        print(e)

def disableVoteAblity(contract_handle, addr):
    try:
        hsh=contract_handle.functions.disableVoteAblity().transact({'from':addr})
    except Exception as e:
        print(e)

def changeAblity(contract_handle, addr, type, value):
    try:
        hsh=contract_handle.functions.changeAblity(type, value).transact({'from':addr})
    except Exception as e:
        print(e)
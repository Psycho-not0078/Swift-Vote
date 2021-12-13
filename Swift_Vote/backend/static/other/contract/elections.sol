// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;
pragma experimental ABIEncoderV2;

contract Election {
    struct vt { //maping a vote to candidate
        uint256 id;
        uint256 cid;//candidate id
        string context;
        string date;
    }
    
    struct candidate {
        uint256 id;
        string name;
        string context;
    }
    
    struct user {
        uint256 id;
        string tag;
        string context;
        uint256 ablity_to_vote;
        uint256 ablity_to_add;
        uint256 ablity_to_change; 
    }
    
    uint256 voteCount;
    uint256 candidateCount;
    uint256 userCount;
    uint256 voterCount;

    mapping(uint256=>address) userAddress;
    mapping(address=>user) users;
    mapping(uint256=>candidate) candidates; 
    mapping(uint256=>vt) votes;

    constructor(){
        init(msg.sender);
    }
    
    function init(address _ad) private{
        //adding the init user 
        userCount+=1;
        userAddress[userCount]=_ad;
        users[_ad]=user(userCount,"admin","central",0,1,1);
    }
    
    function addUser(address _ad, string memory _context) public{
        //function to add users, be it candidates or voters or officials.
        require(users[msg.sender].ablity_to_add==1,"the role doesnt allow it");
        userCount+=1;
        voterCount+=1;
        userAddress[userCount]=_ad;
        users[_ad]=user(userCount,"user",_context,0,0,0);
    }  


    function addCandidate( string memory _name, string memory _context) public {
        //function to add a candidate to the system
        require(users[msg.sender].ablity_to_add==1,"the role doesnt allow it");
        candidateCount+=1;
        candidates[candidateCount]=candidate(candidateCount, _name, _context);
    }

    function changeAblity(address _ad, uint256 _ablityType, uint256 _value) public {
        require(users[msg.sender].ablity_to_change==1,"the role doesnt allow it");
        if (_ablityType==1){
            users[_ad].ablity_to_vote=_value;
        }
        else if(_ablityType==2){
            users[_ad].ablity_to_add=_value;
        }
        else if(_ablityType==3){
            users[_ad].ablity_to_change=_value;
        }
    }

    function disableVoteAblity(address _ad) private { 
        //function to not allow a person to vote more than once.
        if (users[_ad].ablity_to_vote==1) {//will be called when vote function is called
            users[_ad].ablity_to_vote=0;
        }
        //have to write an event here
    }

    function listVoters() public view returns (address  [] memory){
        // require(keccak256(bytes(users[msg.sender].tag))==keccak256(bytes("admin")),"the role doesnt allow it");
        address[] memory addressesses = new address[](voterCount);
        uint256 i=1;
        uint256 pos=0;
        for(i=1;i<=userCount;i++){
            if(users[userAddress[i]].ablity_to_vote==1){
                addressesses[pos]=userAddress[i];
                pos+=1;
            }
        }
        return addressesses;
    }

    function listOfficials() public view returns (address  [] memory){
        require(keccak256(bytes(users[msg.sender].tag))==keccak256(bytes("admin")),"the role doesnt allow it");
        address[] memory addressesses = new address[](voterCount);
        uint256 i=1;
        uint256 pos=0;
        for(i=1;i<=userCount;i++){
            if((users[userAddress[i]].ablity_to_add==1 || users[userAddress[i]].ablity_to_change==1) && users[userAddress[i]].ablity_to_vote==0){
                addressesses[pos]=userAddress[i];
                pos+=1;
            }
        }
        return addressesses;
    }

    function listCandidates(string memory _context)public view returns (string[] memory name, uint256[] memory id){
        require(keccak256(bytes(users[msg.sender].tag))==keccak256(bytes("user")),"the role doesnt allow it");
        string[] memory names=new string[](candidateCount);
        uint256[] memory ids=new uint256[](candidateCount);
        uint256 i=1;
        uint256 pos=0;
        for(i=1;i<=candidateCount;i++){
            if(keccak256(bytes(candidates[i].context))==keccak256(bytes(_context))){
                ids[pos]=candidates[i].id;
                names[pos]=candidates[i].name;
                pos+=1;
            }
        }
        return (names,ids);
    }

    function vote(uint256 _id, string memory _context,string memory _date) public{
        require(users[msg.sender].ablity_to_vote==1,"the role doesnt allow it");
        require(keccak256(bytes(users[msg.sender].tag))==keccak256(bytes("user")),"the role doesnt allow it");
        require(keccak256(bytes(users[msg.sender].context))==keccak256(bytes(candidates[_id].context)),"error 404");
        voteCount+=1;
        votes[voteCount]=vt(voteCount, _id, _context, _date);
        disableVoteAblity(msg.sender);
    }
    
    function countVote(uint256 _id) public view returns (uint256 _count){
        uint256 _vtcount=0;
        uint256 i=1;
        for(i=1;i<=voteCount;i++){
            if (votes[i].cid==_id){
                _vtcount+=1;
            }
        }
        return _vtcount;
    }
}
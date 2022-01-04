pragma solidity >=0.7.0 <0.9.0;
    
    contract Election {
        struct vt { 
            uint256 id;
            uint256 cid;
            string location;
            string date;
        }
        
        struct candidate {
            uint256 id;
            string name;
            string location;
        }
    
        struct user {
            uint256 id;
            string tag;
            string location;
            uint256 ablity_to_vote;
            uint256 ablity_to_add;
            uint256 ablity_to_change;
        }
    
        uint256 voteCount;
        uint256 officialCount;
        uint256 candidateCount;
        uint256 userCount;
        uint256 voterCount;
    
        mapping(uint256=>address) userAddress;
        mapping(address=>user) users;
        mapping(uint256=>string) candidateNames;
        mapping(string=>candidate) candidates; 
        mapping(uint256=>vt) votes;
    
        constructor(){
            init(msg.sender);
        }
    
        function init(address _ad) private{
            userCount+=1;
            officialCount+=1;
            userAddress[userCount]=_ad;
            users[_ad]=user(userCount,"admin","central",0,1,1);
        }
        function addUser(address _ad, string memory _location) public{
            require(users[msg.sender].ablity_to_add==1,"the role doesnt allow it");
            userCount+=1;
            voterCount+=1;
            userAddress[userCount]=_ad;
            users[_ad]=user(userCount,"user",_location,1,0,0);
        }
        function addCandidate( string memory _name, string memory _location) public {
            require(users[msg.sender].ablity_to_add==1,"the role doesnt allow it");
            candidateCount+=1;
            candidateNames[candidateCount]=_name;
            candidates[candidateNames[candidateCount]]=candidate(candidateCount, _name, _location);
        }
        function changeAblity(address _ad, uint256 _ablityType, uint256 _value) public {
            require(users[msg.sender].ablity_to_change==1,"the role doesnt allow it");
            if (_ablityType==1){
                users[_ad].ablity_to_vote=_value;
            }
        else if(_ablityType==2){
                users[_ad].ablity_to_add=_value;
                if (_value==1){
                    officialCount+=1;
                }
                else{
                    officialCount-=1;
                }
            }
    
            else if(_ablityType==3){
                users[_ad].ablity_to_change=_value;
                if (_value==1){
                    officialCount+=1;
                }
                else{
                    officialCount-=1;
                }
            }
        }
    
        function disableVoteAblity(address _ad) private { 
            if (users[_ad].ablity_to_vote==1) {
                users[_ad].ablity_to_vote=0;
            }
        }
    
        function listVoters() public view returns (address  [] memory){
            require(keccak256(bytes(users[msg.sender].tag))==keccak256(bytes("admin")),"the role doesnt allow it");
            address[] memory addressesses = new address[](voterCount);
            uint256 i=1;
            uint256 pos=0;
            for(i=0;i<=userCount;i++){
                if(users[userAddress[i+1]].ablity_to_vote==1){
                    addressesses[pos]=userAddress[i+1];
                    pos+=1;
                }
            }
            return addressesses;
        }
    
        function listOfficials() public view returns (address  [] memory){
            require(keccak256(bytes(users[msg.sender].tag))==keccak256(bytes("admin")),"the role doesnt allow it");
            address[] memory addressesses = new address[](officialCount);
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
        function listCandidates(string memory _location)public view returns (string[] memory name){
            require(keccak256(bytes(users[msg.sender].tag))==keccak256(bytes("admin")),"the role doesnt allow it");
            string[] memory names=new string[](candidateCount);
            uint256 i=1;
            uint256 pos=0;
            for(i=1;i<=candidateCount;i++){
                if(keccak256(bytes(candidates[candidateNames[i]].location))==keccak256(bytes(_location))){
                    names[pos]=candidates[candidateNames[i]].name;
                    pos+=1;
                }
            }
            return names;
        }
    function vote(string memory _name, string memory _location,string memory _date) public{
        require(users[msg.sender].ablity_to_vote==1,"the role doesnt allow it");
        require(keccak256(bytes(users[msg.sender].tag))==keccak256(bytes("user")),"the role doesnt allow it");
        require(keccak256(bytes(users[msg.sender].location))==keccak256(bytes(candidates[_name].location)),"error 404");
        voteCount+=1;
        uint256 _id=0;
        uint256 i=1;
        for(i=1;i<=candidateCount;i++){
            if (keccak256(bytes(candidateNames[i]))==keccak256(bytes(_name))){
                _id=i;
            }
        }
        votes[voteCount]=vt(voteCount, _id, _location, _date);
        disableVoteAblity(msg.sender);
    }
    function countVote(string memory _name) public view returns (uint256 _count){
        uint256 _vtcount=0;
        uint256 i=1;
        uint256 _id=0;
        uint256 j=1;
        for(j=1;j<=candidateCount;j++){
            if (keccak256(bytes(candidateNames[j]))==keccak256(bytes(_name))){
                _id=j;
            }
        }
        for(i=1;i<=voteCount;i++){
            if (votes[i].cid==_id){
                _vtcount+=1;
            }
        }
        return _vtcount;
    }
    }

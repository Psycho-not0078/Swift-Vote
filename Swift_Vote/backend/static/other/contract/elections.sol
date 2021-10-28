pragma solidity >=0.7.0 <0.9.0;

contract Election {
    struct vote { //maping a vote to candidate
        uint256 id;
        uint256 cid;//candidate id
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
        uint256 ablity_to_vote;
        uint256 ablity_to_add; 
    }
    uint256 voteCount;
    uint256 candidateCount;
    uint256 userCount;
    // string[] returner;
    
    mapping(address=>uint256) userAddress;
    mapping(uint256=>user) users;
    mapping(address=>uint256) voteAddress;
    mapping(uint256=>vote) votes;
    mapping(address=>uint256) candidateAddress;
    mapping(uint256=>candidate) candidates; 
    
    constructor(){
        init(msg.sender);
    }
    
    function init(address _ad) private{
        //adding the init user 
        userCount+=1;
        userAddress[_ad]=userCount;
        users[userAddress[_ad]]=user(userCount,0,1);
    }
    
    function addUser(address _ad) public{
        //function to add users, be it candidates or voters or officials.
        require(users[userAddress[_ad]].ablity_to_add==1,"the role doesnt allow it");
        userCount+=1;
        userAddress[_ad]=userCount;
        users[userAddress[_ad]]=user(userCount,0,0);
    }
    
    function userDetails(address _ad) public view returns (user memory){
        //a tester function and for manual verification of specific user update.
        require(users[userAddress[msg.sender]].ablity_to_add==1,"the role doesnt allow it");
        return users[userAddress[_ad]];
    }

    function listCandidates() public view returns (string[] memory,string[] memory){
        // a viewer function to get the list of candidates to conduct voting
        string[] memory _names = new string[](uint256(candidateCount)); 
        string[] memory _locations = new string[](uint256(candidateCount)); 
        for (uint256 _i=0; _i<uint256(candidateCount); _i+=1){
            _names[_i]=candidates[_i+1].name;
            _locations[_i]=candidates[_i+1].location;
        }
        return (_names,_locations);
    }
    
    function listlocCandidate(string memory _location) public view returns (string[] memory) {
        //a viwer function to get list of candidates that are in a specific location
        string[] memory _names = new string[](uint256(candidateCount)); 
        for (uint256 _i=0; _i<uint256(candidateCount); _i+=1){
            if (keccak256(bytes(candidates[_i+1].location))==keccak256(bytes(_location))){//comparing the hash of strings to check if they are the same 
                _names[_i]=candidates[_i+1].name;                                         //this bcause solidity doesn have its own string related functions
            }
        }
        return _names;
    }
    
    function addCandidate( address _ad,string memory _name, string memory _location) public {
        //function to add a candidate to the system
        require(users[userAddress[_ad]].ablity_to_add==1,"the role doesnt allow it");
        candidateCount+=1;
        candidateAddress[_ad]=candidateCount;
        candidates[candidateAddress[_ad]]=candidate(candidateCount, _name, _location);
    }
    event changedUser(user u);
    function changeAblity(uint256 _id, uint256 _ablityType, uint256 _value) public {
        //function to change the add ablity or the vote ablity
        require(users[userAddress[msg.sender]].ablity_to_add==1,"the role doesnt allow it");
        if (_ablityType==1){
            users[_id].ablity_to_vote=_value;
        }
        else{
            users[_id].ablity_to_add=_value;
        }
        //have to add an event here
    }
    function DisableAblity(address _ad) private { 
        //function to not allow a person to vote more than once.
        if (users[userAddress[_ad]].ablity_to_vote==1) {//will be called when vote function is called
            users[userAddress[_ad]].ablity_to_vote=0;
        }
        //have to write an event here
    }
    function cvote(uint256 _cid,string memory _location,string memory _date) public {
        //cvote for cast vote
        require(users[userAddress[msg.sender]].ablity_to_vote==1,"error 403");
        require(_cid<=candidateCount,"error 404");
        require(keccak256(bytes(candidates[_cid].location))==keccak256(bytes(_location)),"error 404");
        DisableAblity(msg.sender);//this is to not allow a person to vote more than once
        voteCount+=1;
        votes[voteCount]=vote(voteCount,_cid,_location,_date);
    }
}pragma solidity >=0.7.0 <0.9.0;

contract Election {
    struct vote { //maping a vote to candidate
        uint256 id;
        uint256 cid;//candidate id
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
        uint256 ablity_to_vote;
        uint256 ablity_to_add; 
    }
    uint256 voteCount;
    uint256 candidateCount;
    uint256 userCount;
    // string[] returner;
    
    mapping(address=>uint256) userAddress;
    mapping(uint256=>user) users;
    mapping(address=>uint256) voteAddress;
    mapping(uint256=>vote) votes;
    mapping(address=>uint256) candidateAddress;
    mapping(uint256=>candidate) candidates; 
    
    constructor(){
        init(msg.sender);
    }
    
    function init(address _ad) private{
        //adding the init user 
        userCount+=1;
        userAddress[_ad]=userCount;
        users[userAddress[_ad]]=user(userCount,0,1);
    }
    
    function addUser(address _ad) public{
        //function to add users, be it candidates or voters or officials.
        require(users[userAddress[_ad]].ablity_to_add==1,"the role doesnt allow it");
        userCount+=1;
        userAddress[_ad]=userCount;
        users[userAddress[_ad]]=user(userCount,0,0);
    }
    
    function userDetails(address _ad) public view returns (user memory){
        //a tester function and for manual verification of specific user update.
        require(users[userAddress[msg.sender]].ablity_to_add==1,"the role doesnt allow it");
        return users[userAddress[_ad]];
    }

    function listCandidates() public view returns (string[] memory,string[] memory){
        // a viewer function to get the list of candidates to conduct voting
        string[] memory _names = new string[](uint256(candidateCount)); 
        string[] memory _locations = new string[](uint256(candidateCount)); 
        for (uint256 _i=0; _i<uint256(candidateCount); _i+=1){
            _names[_i]=candidates[_i+1].name;
            _locations[_i]=candidates[_i+1].location;
        }
        return (_names,_locations);
    }
    
    function listlocCandidate(string memory _location) public view returns (string[] memory) {
        //a viwer function to get list of candidates that are in a specific location
        string[] memory _names = new string[](uint256(candidateCount)); 
        for (uint256 _i=0; _i<uint256(candidateCount); _i+=1){
            if (keccak256(bytes(candidates[_i+1].location))==keccak256(bytes(_location))){//comparing the hash of strings to check if they are the same 
                _names[_i]=candidates[_i+1].name;                                         //this bcause solidity doesn have its own string related functions
            }
        }
        return _names;
    }
    
    function addCandidate( address _ad,string memory _name, string memory _location) public {
        //function to add a candidate to the system
        require(users[userAddress[_ad]].ablity_to_add==1,"the role doesnt allow it");
        candidateCount+=1;
        candidateAddress[_ad]=candidateCount;
        candidates[candidateAddress[_ad]]=candidate(candidateCount, _name, _location);
    }
    event changedUser(user u);
    function changeAblity(uint256 _id, uint256 _ablityType, uint256 _value) public {
        //function to change the add ablity or the vote ablity
        require(users[userAddress[msg.sender]].ablity_to_add==1,"the role doesnt allow it");
        if (_ablityType==1){
            users[_id].ablity_to_vote=_value;
        }
        else{
            users[_id].ablity_to_add=_value;
        }
        //have to add an event here
    }
    function DisableAblity(address _ad) private { 
        //function to not allow a person to vote more than once.
        if (users[userAddress[_ad]].ablity_to_vote==1) {//will be called when vote function is called
            users[userAddress[_ad]].ablity_to_vote=0;
        }
        //have to write an event here
    }
    function cvote(uint256 _cid,string memory _location,string memory _date) public {
        //cvote for cast vote
        require(users[userAddress[msg.sender]].ablity_to_vote==1,"error 403");
        require(_cid<=candidateCount,"error 404");
        require(keccak256(bytes(candidates[_cid].location))==keccak256(bytes(_location)),"error 404");
        DisableAblity(msg.sender);//this is to not allow a person to vote more than once
        voteCount+=1;
        votes[voteCount]=vote(voteCount,_cid,_location,_date);
    }
}pragma solidity >=0.7.0 <0.9.0;

contract Election {
    struct vote { //maping a vote to candidate
        uint256 id;
        uint256 cid;//candidate id
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
        uint256 ablity_to_vote;
        uint256 ablity_to_add; 
    }
    uint256 voteCount;
    uint256 candidateCount;
    uint256 userCount;
    // string[] returner;
    
    mapping(address=>uint256) userAddress;
    mapping(uint256=>user) users;
    mapping(address=>uint256) voteAddress;
    mapping(uint256=>vote) votes;
    mapping(address=>uint256) candidateAddress;
    mapping(uint256=>candidate) candidates; 
    
    constructor(){
        init(msg.sender);
    }
    
    function init(address _ad) private{
        //adding the init user 
        userCount+=1;
        userAddress[_ad]=userCount;
        users[userAddress[_ad]]=user(userCount,0,1);
    }
    
    function addUser(address _ad) public{
        //function to add users, be it candidates or voters or officials.
        require(users[userAddress[_ad]].ablity_to_add==1,"the role doesnt allow it");
        userCount+=1;
        userAddress[_ad]=userCount;
        users[userAddress[_ad]]=user(userCount,0,0);
    }
    
    function userDetails(address _ad) public view returns (user memory){
        //a tester function and for manual verification of specific user update.
        require(users[userAddress[msg.sender]].ablity_to_add==1,"the role doesnt allow it");
        return users[userAddress[_ad]];
    }

    function listCandidates() public view returns (string[] memory,string[] memory){
        // a viewer function to get the list of candidates to conduct voting
        string[] memory _names = new string[](uint256(candidateCount)); 
        string[] memory _locations = new string[](uint256(candidateCount)); 
        for (uint256 _i=0; _i<uint256(candidateCount); _i+=1){
            _names[_i]=candidates[_i+1].name;
            _locations[_i]=candidates[_i+1].location;
        }
        return (_names,_locations);
    }
    
    function listlocCandidate(string memory _location) public view returns (string[] memory) {
        //a viwer function to get list of candidates that are in a specific location
        string[] memory _names = new string[](uint256(candidateCount)); 
        for (uint256 _i=0; _i<uint256(candidateCount); _i+=1){
            if (keccak256(bytes(candidates[_i+1].location))==keccak256(bytes(_location))){//comparing the hash of strings to check if they are the same 
                _names[_i]=candidates[_i+1].name;                                         //this bcause solidity doesn have its own string related functions
            }
        }
        return _names;
    }
    
    function addCandidate( address _ad,string memory _name, string memory _location) public {
        //function to add a candidate to the system
        require(users[userAddress[_ad]].ablity_to_add==1,"the role doesnt allow it");
        candidateCount+=1;
        candidateAddress[_ad]=candidateCount;
        candidates[candidateAddress[_ad]]=candidate(candidateCount, _name, _location);
    }
    event changedUser(user u);
    function changeAblity(uint256 _id, uint256 _ablityType, uint256 _value) public {
        //function to change the add ablity or the vote ablity
        require(users[userAddress[msg.sender]].ablity_to_add==1,"the role doesnt allow it");
        if (_ablityType==1){
            users[_id].ablity_to_vote=_value;
        }
        else{
            users[_id].ablity_to_add=_value;
        }
        //have to add an event here
    }
    function DisableAblity(address _ad) private { 
        //function to not allow a person to vote more than once.
        if (users[userAddress[_ad]].ablity_to_vote==1) {//will be called when vote function is called
            users[userAddress[_ad]].ablity_to_vote=0;
        }
        //have to write an event here
    }
    function cvote(uint256 _cid,string memory _location,string memory _date) public {
        //cvote for cast vote
        require(users[userAddress[msg.sender]].ablity_to_vote==1,"error 403");
        require(_cid<=candidateCount,"error 404");
        require(keccak256(bytes(candidates[_cid].location))==keccak256(bytes(_location)),"error 404");
        DisableAblity(msg.sender);//this is to not allow a person to vote more than once
        voteCount+=1;
        votes[voteCount]=vote(voteCount,_cid,_location,_date);
    }
}
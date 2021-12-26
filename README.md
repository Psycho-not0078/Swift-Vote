# Swift-Vote
“Swift Vote” is a blockchain-based voting system specifically designed to address the legal requirements of a democratic process. A remote voting system has always been criticised for its manipulative nature but with the introduction of Blockchain technology, the goal of achieving a near-irrefutable voting process with adequate security mechanisms can be achieved. “Swift Vote” will consist of a general web application that allows for creating valid voter accounts which will be generated after being verified by an Election Officer. Once the election process is commenced and enabled by the officer, voters will be able to cast a vote and receive an email (or text message) acknowledgement. 
There will be activities restrained to different classes of web application users providing for appropriate access management. All system information needs to be maintained in a database located on a secure web server. Furthermore, Blockchain will maintain the anonymity of the voters and disallow any Election Officer to view who cast a vote to whom. Results shall be counted within the smart contract and announced, once the election is disabled.

For  running the project:
1. Run the command: docker-compose up --build
2. Open http://localhost:8001/ in browser (it will take around 5-10 minutes for it to start the first time)

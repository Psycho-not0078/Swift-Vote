from unittest import TestCase
from mock import Mock
from myproject import greet
import web3

class Test(TestCase):

    def test_should_write_hello_world(self):
        mock_stdout = Mock()

        greet(mock_stdout)

        mock_stdout.write.assert_called_with("Hello world\n")

    
        w3 = web3.Web3(web3.HTTPProvider("http://127.0.0.1:8545"))
        print(w3.isConnected())
from mockito import mock, verify
import unittest

from scripts import function1, function2

class UnitTest(unittest.TestCase):
    def test_web3(self):
        out = mock()
        function1(out)
        verify(out).write(True)

    def test_2(self):
        out = mock()
        function2(out)
        verify(out).write("Hello")
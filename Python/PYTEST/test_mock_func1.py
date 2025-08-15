from unittest.mock import MagicMock

def test_mocking1():
    magic_mock = MagicMock()
    magic_mock.any_method.ret_val = "A mock object"
    print(magic_mock.any_method())

    magic_mock.any_attribute = 100
    print(magic_mock.any_attribute)

    magic_mock.any_method.side_effect = Exception("Exception occurred")

test_mocking1()

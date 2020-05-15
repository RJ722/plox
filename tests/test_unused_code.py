import pytest
from vulture import Vulture

@pytest.fixture
def v():
    return Vulture(verbose=True)

def test_unused_code(v):
    v.scavenge(['lox'])
    v.report()
    if v.get_unused_code() != []:
        raise AssertionError

def test_unused_test(v):
    v.scavenge(['tests'])
    v.report()
    if v.get_unused_code() != []:
        raise AssertionError

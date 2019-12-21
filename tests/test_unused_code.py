import pytest
from vulture import Vulture

@pytest.fixture
def v():
    return Vulture(verbose=True)

def test_unused_code(v):
    v.scavenge(['lox'])
    v.report()
    assert v.get_unused_code() == []

def test_unused_test(v):
    v.scavenge(['tests'])
    v.report()
    assert v.get_unused_code() == []

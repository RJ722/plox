import lox
from lox import lox

import pytest


@pytest.fixture
def l():
    return lox.Lox()

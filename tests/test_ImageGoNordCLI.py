import pytest
from ImageGoNord.__main__ import ImageGoNordCLI

@pytest.fixture
def cli():
    return ImageGoNordCLI()

def test_init(cli):
    assert isinstance(cli, ImageGoNordCLI)

def test_init(cli):
    assert isinstance(cli, ImageGoNordCLI)


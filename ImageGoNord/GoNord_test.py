import pytest
from PIL import Image

from ImageGoNord import GoNord


@pytest.fixture
def image():
    return Image.open("images/test-profile.jpg")


@pytest.fixture
def go_nord():
    return GoNord()


def test_resize_image(image, go_nord: GoNord):
    resized_image = go_nord.resize_image(image, w=20, h=20)
    assert resized_image.size == (20, 20)

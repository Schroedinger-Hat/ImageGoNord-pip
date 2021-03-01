import pytest
from PIL import Image

from ImageGoNord import GoNord


@pytest.fixture
def image():
    return Image.open("images/test-profile.jpg")


@pytest.fixture
def go_nord():
    return GoNord()


@pytest.mark.skip()  # this is the "old" interface
def test_resize_image_with_w_and_h(image, go_nord: GoNord):
    resized_image = go_nord.resize_image(image, w=20, h=20)
    assert resized_image.size == (20, 20)


def test_resize_image_with_size(image, go_nord: GoNord):
    resized_image = go_nord.resize_image(image, size=(20, 20))
    assert resized_image.size == (20, 20)


def test_resize_image(image: Image, go_nord: GoNord):
    resized_image = go_nord.resize_image(image)
    w, h = image.size
    assert resized_image.size == (round(w / 2), round(h / 2))

import base64
import os
import pytest

from facial_recognition import helpers
from tests.conftest import TEST_DIR

@pytest.fixture()
def image_directory():
    return os.path.join(TEST_DIR, 'test_images')


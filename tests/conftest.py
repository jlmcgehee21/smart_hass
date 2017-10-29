import os
import sys
import pytest

TEST_DIR = os.path.dirname(os.path.realpath(__file__))
code_dir = os.path.join(TEST_DIR, '../smart_hass/')

sys.path.append(code_dir)

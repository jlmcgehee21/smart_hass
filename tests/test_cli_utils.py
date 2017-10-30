from smart_hass import cli_utils

def test_load_number_arg_none():
    result = cli_utils.load_number_arg(None)
    assert result == None

def test_load_number_arg_int():
    result = cli_utils.load_number_arg(1.0)
    assert result == 1
    assert type(result) == int

def test_load_number_arg_float():
    result = cli_utils.load_number_arg(1.1)
    assert result == 1.1
    assert type(result) == float

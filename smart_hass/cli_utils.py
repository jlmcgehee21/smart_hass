
def load_number_arg(number_arg):
    if number_arg is not None:
        if number_arg.is_integer():
            number_arg = int(number_arg)

    return number_arg

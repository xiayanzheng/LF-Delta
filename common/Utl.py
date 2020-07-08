from functools import wraps
from lfcomlib.Jessica import DaPr

DaPr = DaPr.Core()


class Entry:

    @staticmethod
    def show_status(data, show=True):
        if show:
            print(data)


def show_status(func):
    msg = '[{}]{}'
    format_i = DaPr.insert_value_to_list_and_merge([s.capitalize() for s in func.__name__.split("_")], " ")

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(msg.format(format_i, "Start"))
        func_obj = func(*args, **kwargs)
        print(msg.format(format_i, "End"))
        return func_obj

    return wrapper

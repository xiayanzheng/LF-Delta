from functools import wraps
from init.init_imports import global_config

class Entry:

    @staticmethod
    def show_status(data, show=True):
        if show:
            print(data)


def show_status():
    def decorate(func):
        msg = ''
        func_name = func.__name__
        func_name_dict = global_config.func_name_dict
        format_i = "[{}]{}"
        if func_name in list(func_name_dict.keys()):
            msg = func_name_dict[func_name]
        else:
            msg = func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            print(format_i.format(msg,"Start"))
            func_obj = func(*args, **kwargs)
            print(format_i.format(msg,"End"))
            return func_obj
        return wrapper
    return decorate

# -*- coding: UTF-8 -*-


def del_prefix(target: str, prefix: str):
    """
    If `target` starts with the `prefix` string and `prefix` is not empty,
    return string[len(prefix):].
    Otherwise, return a copy of the original string.
    """
    if (len(prefix) > 0) and (target.startswith(prefix) is True):
        try:  # python >= 3.9
            return target.removeprefix(prefix)
        except AttributeError:  # python <= 3.7
            return target[len(prefix):]
    return target

IREGEX = True

"""PYPIPR Module"""


"""PYTHON Standard Module"""


"""PYPI Module"""
import re


def regex_multiple_replace(data, regex_replacement_list):
    """
    Melakukan multiple replacement untuk setiap list.

    regex_replacement_list = [
        {"regex":r"", "replacement":""},
        {"regex":r"", "replacement":""},
        {"regex":r"", "replacement":""},
    ]
    """
    for v in regex_replacement_list:
        data = re.sub(v["regex"], v["replacement"], data)
    return data

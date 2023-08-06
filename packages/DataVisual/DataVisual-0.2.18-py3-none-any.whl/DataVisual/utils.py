import numpy as np
import re
from typing import Union



def Norm(Scalar):
    return np.sqrt(np.sum(np.abs(Scalar)**2))


def Normalize(Scalar):
    return Scalar / Norm(Scalar)

def IO(text):
    txt = '\n' + '-' * 100 + '\n'
    txt += text
    txt += '\n' + '-' * 100
    return txt


UlistLike = (list, np.ndarray, tuple)

def ToList(arg):

    if isinstance(arg, list):
        return np.asarray(arg)

    if not isinstance(arg, (list, np.ndarray, tuple)):
        return np.asarray([arg])

    else:
        return arg


def FormatStr(function):
    def wrapped(*args, **kwargs):
        args = (re.sub(r"\s+", "", arg.lower() ) if isinstance(arg, str) else arg for arg in args)

        kwargs = {k: re.sub(r"\s+", "", v.lower() ) if isinstance(v, str) else v for k, v in kwargs.items()}

        return function(*args, **kwargs)
    return wrapped


def FormatString(string):
    return re.sub(r"\s+", "", string.lower() )

# -

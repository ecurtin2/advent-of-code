from typing import Callable
from inspect import signature

import cattr

def is_option(t):
    args = getattr(t, "__args__", tuple())
    return len(args) == 2 and any(arg is type(None) for arg in args)


def is_list(t):
    return hasattr(t, "__args__") and not is_option(t)


import builtins

def parse_input(to, s: str):
    match to:
        case builtins.str:
            return s
        # Figure out how to pattern match list[x] but for now
        # just assume
        case _:
            inner_t = to.__args__[0]
            lines = s.splitlines()
            if is_list(inner_t):
                lines = [l.split() for l in lines]
            return [cattr.structure(l if l else None, inner_t) for l in lines]
    raise ValueError(f"Can't parse to type {to}")


def parse_run(f: Callable, inputs: str):
    sig = signature(f)
    input_type = list(sig.parameters.values())[0].annotation
    inputs = parse_input(input_type, inputs)
    return f(inputs)
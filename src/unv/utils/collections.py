def update_nested_dict(original: dict, from_dict: dict) -> dict:
    """Simple function to update nested dict.

    >>> d = {0: 0, 1: {1: 1}, 2: {2: {3: 3}}}
    >>> n = {0: 1, 2: {2: {4: 4}}, 5: 1}
    >>> r = update_nested_dict(d, n)
    >>> r is d
    True
    >>> r[0]
    1
    >>> r[1]
    {1: 1}
    >>> r[2][2]
    {3: 3, 4: 4}
    >>> r[5]
    1
    """
    for key, value in from_dict.items():
        if isinstance(value, dict) and key in original:
            original[key] = update_nested_dict(original.get(key, {}), value)
        else:
            original[key] = value
    return original

import collections.abc as abc


def update_nested_mapping(mapping, update_mapping):
    """Simple function to update nested dict."""
    for key, value in update_mapping.items():
        if isinstance(value, abc.Mapping) and key in mapping:
            mapping[key] = update_nested_mapping(mapping.get(key, {}), value)
        else:
            mapping[key] = value
    return mapping

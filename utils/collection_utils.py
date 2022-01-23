def get_with_default(list, idx, default_value):
    try:
        return list[idx]
    except IndexError:
        return default_value

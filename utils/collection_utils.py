def get_with_default(list, idx, default_value):
    try:
        return list[idx]
    except IndexError:
        return default_value


def get_dict_key_by_value(dict, value):
    for k, v in dict.items():
        if v == value:
            return k

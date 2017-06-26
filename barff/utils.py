def format_val(val):
    """
    Helper method that applies all formatting methods on a given val.
    :param val: raw value as string
    :return: formatted string
    """
    result = val
    result = quote_if_space(result)
    result = replace_nans(result)
    return result


def quote_if_space(val):
    """
    Adds double quotes around a string value if it contains a space.
    :param val: raw value as string
    :return: formatted string
    """
    result = val
    if ' ' in val:
        result = '"' + val + '"'
    return result


def replace_nans(val):
    """
    Replaces nan values with single question mark
    :param val: raw value as string
    :return: formatted string
    """
    # TODO: Ideally this should happen earlier, before pandas NaN is stringified and .lower()ed for safety's sake.
    result = val
    if val == 'nan':
        result = '?'
    return result

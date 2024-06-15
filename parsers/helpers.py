import re


def get_number_from_string(string: str):
    string = string.replace(' ', '').replace("\u00A0", "")
    pattern = r'[-+]?\d*\.\d+|\d+'
    matches = re.findall(pattern, string)

    if len(matches) > 0:
        if '.' in matches[0]:
            return float(matches[0])
        else:
            return int(matches[0])

    return None


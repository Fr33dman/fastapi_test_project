import re


async def is_anagram(s1: str, s2: str):
    if len(s1) != len(s2):
        return False

    list1 = sorted(s1)
    list2 = sorted(s2)

    pos = 0
    matches = True

    while pos < len(s1) and matches:
        if list1[pos] == list2[pos]:
            pos = pos + 1
        else:
            matches = False

    return matches


def is_valid_mac_address(value):
    allowed = re.compile(r"""(^([0-9A-F]{2}[-]){5}([0-9A-F]{2})$|^([0-9A-F]{2}[:]){5}([0-9A-F]{2})$)""",
                         re.VERBOSE | re.IGNORECASE)

    if allowed.match(value) is None:
        return False
    else:
        return True

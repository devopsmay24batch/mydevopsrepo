###############################################################################
# LEGALESE:   "Copyright (C) 2020-      Celestica Corp. All rights reserved." #
#                                                                             #
# This source code is confidential, proprietary, and contains trade           #
# secrets that are the sole property of Celestica Corp.                       #
# Copy and/or distribution of this source code or disassembly or reverse      #
# engineering of the resultant object code are strictly forbidden without     #
# the written consent of Celestica Corp.                                      #
#                                                                             #
###############################################################################

import re
from robot.api import logger

from robot.errors import DataError
from robot.libraries.BuiltIn import BuiltIn
from robot.utils import is_list_like, is_string


def should_match_paired_regexp_list(text, patterns: list, msg=None, values=False):
    """Fails if ``string`` does not match paired ``patterns`` list as a regular expression."""

    if not is_list_like(patterns):
        raise DataError("patterns must be list type")

    _line = str()
    _lines = str(text).splitlines()
    lines = list()
    matches = dict()

    is_found_first_pattern = False
    for _line_offset, _line in enumerate(_lines):
        res = re.search(patterns[0], _line)
        if res:
            is_found_first_pattern = True
            lines = _lines[_line_offset:]

    if is_found_first_pattern == False:
        raise AssertionError(BuiltIn()._get_string_msg(_line, patterns[0],
"""
Not found first pattern:

{pattern}

""".format(pattern=patterns[0]), values, 'does not match'))

    for index, (text, pattern) in enumerate(zip(lines, patterns)):
        res = re.search(pattern, text)
        if res is None:
            raise AssertionError(BuiltIn()._get_string_msg(text, pattern,
"""
Not matched at pattern line number {index}:

   text = {text}
pattern = {pattern}

{msg}"""
        .format(index=index + 1, text=text, pattern=pattern,
        msg=msg if msg != None else ""), values, 'does not match'))

        match = res.groupdict()
        matches.update(match)

    return matches


def should_match_ordered_regexp_list(text, patterns: list, msg=None, values=False):
    """Fails if ``string`` does not match ordered ``patterns`` list as a regular expression."""

    if not is_list_like(patterns):
        raise DataError("patterns must be list type")

    lines = str(text).splitlines()
    matches = dict()

    patterns_iter = iter(patterns)
    pattern = next(patterns_iter)
    lines_iter = iter(lines)
    while True:
        try:
            line = next(lines_iter)
        except StopIteration:
            # Not find for all pattern(s) and stop immediately if not found one of them
            raise AssertionError(BuiltIn()._get_string_msg("(too many lines to display)", pattern,
"""
Not found pattern:

{pattern}

{msg}"""
            .format(msg=msg if msg != None else "", pattern=pattern), values, 'does not match'))

        res = re.search(pattern, line)
        if res:
            match = res.groupdict()
            matches.update(match)

            try:
                pattern = next(patterns_iter)
            except StopIteration:
                break

    return matches


def should_match_one_of_regexp_list(text, patterns: list, msg=None, values=False):
    """Fails if ``text`` does not match any one of ``patterns`` list as a regular expression."""

    if not is_list_like(patterns):
        raise DataError("patterns must be list type")

    lines = str(text).splitlines()
    matches = dict()
    is_match_one_of_patterns = False

    for pattern in patterns:
        for line in lines:
            res = re.search(pattern, line)
            if res:
                match = res.groupdict()
                matches.update(match)

                is_match_one_of_patterns = True

    if is_match_one_of_patterns == False:
        raise AssertionError(BuiltIn()._get_string_msg("(too many lines to display)", patterns,
"""
Not found any one of patterns:

{patterns}

{msg}"""
        .format(msg=msg if msg != None else "", patterns=str(patterns).splitlines()), values, 'does not match'))

    return matches


def should_match_a_regexp(text, pattern: str, msg=None, values=False):
    """Fails if ``text`` does not match a ``pattern`` as a regular expression."""

    if not is_string(pattern):
        raise DataError("pattern must be string type")

    lines = str(text).splitlines()

    for index, line in enumerate(lines):
        res = re.search(pattern, line)
        if res:
            match = res.groupdict()

            return match
        else:
            if index == len(lines) - 1:
                raise AssertionError(BuiltIn()._get_string_msg("(too many lines to display)", pattern,
"""
Not found pattern:

{pattern}

{msg}"""        .format(msg=msg if msg != None else "", pattern=pattern), values, 'does not match'))


def should_match_a_regexp_for_table(text, pattern: str, msg=None, values=False):
    """Fails if ``text`` does not match a ``pattern`` on the table as a regular expression."""

    if not is_string(pattern):
        raise DataError("pattern must be string type")

    number = 0
    matches = dict()
    lines = str(text).splitlines()

    for index, line in enumerate(lines):
        res = re.search(pattern, line)
        if res:
            match = res.groupdict()
            copied_match = match.copy()
            match.clear()

            number = number + 1
            for key in copied_match.keys():
                match[key + "_" + str(number)]  = copied_match[key]

            matches.update(match)
        else:
            if (index == len(lines) - 1) and (not matches):
                raise AssertionError(BuiltIn()._get_string_msg("(too many lines to display)", pattern,
"""
Not found pattern on the table:

{pattern}

{msg}"""            .format(msg=msg if msg != None else "", pattern=pattern), values, 'does not match'))

    return matches

def should_not_match_a_regexp_for_table(text, pattern: str):
    """Fails if ``text`` does not match a ``pattern`` on the table as a regular expression."""

    if not is_string(pattern):
        raise DataError("pattern must be string type")

    number = 0
    matches = dict()
    lines = str(text).splitlines()
    for index, line in enumerate(lines):
        res = re.search(pattern, line)
        if res:
            match = res.groupdict()
            copied_match = match.copy()
            match.clear()
            number = number + 1
            for key in copied_match.keys():
                match[key + "_" + str(number)]  = copied_match[key]
            matches.update(match)
    if matches:
        return matches

def compare_two_dictionaries_with_matched_key(original:dict, compare:dict, msg=None, values=False):
    """Fails if two dictionaries ``original`` does not match ``compare`` for matched key."""

    for key in original.keys():
        if original[key] != compare[key]:
            raise AssertionError(BuiltIn()._get_string_msg(original[key], compare[key],
"""
Key name {key} does not match:

original[{key}] = {original}
 compare[{key}] = {compare}

{msg}"""        .format(msg=msg if msg != None else "", key=key, original=original[key], compare=compare[key]),
                        values, 'does not match'))


def compare_two_dictionaries_by_value(original:dict, compare:dict, msg=None, values=False):
    """Fails if two dictionaries ``original`` does not match ``compare`` for matched value."""

    for key_o in original.keys():
        for key_c in compare.keys():
            if original[key_o] == compare[key_c]:
                break

            if key_c == compare.keys()[-1]:
                raise AssertionError(BuiltIn()._get_string_msg(original[key_o], "compare dictionary values",
"""
Not found value {value} on comapre dictionary:

original[{key}] = {value}

{msg}"""            .format(msg=msg if msg != None else "",
                        value=original[key_o], key=key_o,
                    ), values, 'not found on'))

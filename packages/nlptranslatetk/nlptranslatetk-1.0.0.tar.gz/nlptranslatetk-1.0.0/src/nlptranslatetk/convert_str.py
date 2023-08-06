import re
from typing import List


def __word_tokenize(__str: str) -> List[str]:
    return re.findall(r"\w+", __str)


def __unique_words(__str: str):
    return set(__word_tokenize(__str))


def __apply_conversions(__str: str, __repls: List[tuple[str]]):
    result = __str
    for (lhs, rhs) in __repls:
        result = result.replace(lhs, rhs)
    return result


def __sorted_conversions_list(__str: str, conversion_map: dict[str, str]):
    word_set = __unique_words(__str)
    results = []
    append = results.append
    for word in word_set:
        if word.islower():
            if word in conversion_map:
                value = (word, conversion_map[word])
                append(value)
        elif word.title() == word:
            lower_word = __str.lower()
            if lower_word in conversion_map:
                value = (__str, conversion_map[lower_word].title())
                append(value)
    results.sort(key=lambda value: len(value[0]), reverse=True)
    return results


def __convert_str_with_conversion_map(__str: str, conversion_map: dict[str, str]):
    result = __str
    if isinstance(result, str):
        conversions = __sorted_conversions_list(result, conversion_map=conversion_map)
        if conversions:
            result = __apply_conversions(result, conversions)
    return result


def with_conversion_map(__str: str, conversion_map: dict[str, str]):
    return __convert_str_with_conversion_map(__str, conversion_map=conversion_map)

from typing import Callable
from . import constants as _constants
from . import convert_str as _convert_str
from . import language_id as _language_id
from .objects import ConversionMapCache as _ConversionMapCache

__conversion_map_cache = _ConversionMapCache()


def __safe_conversion_map(__from_lang: str, __to_lang: str, __line_delimiter: str):
    from_index = _constants.LANGUAGE_INDEX_MAP[__from_lang]
    to_index = _constants.LANGUAGE_INDEX_MAP[__to_lang]

    result: dict[str, str] = {}
    for line in (
        line
        for line in _constants.WORD_CONVERSIONS.splitlines(keepends=False)
        if __line_delimiter in line
    ):
        words = line.split(__line_delimiter)
        from_word, to_word = words[from_index], words[to_index]
        result[from_word] = to_word
    return result


def __get_str_conversion_map(
    __from_lang: str = "en-gb", __to_lang: str = "en-us", __line_delimiter: str = ","
) -> dict[str, str]:
    result = {}
    from_lang = _language_id.recognize(__from_lang)
    if from_lang is not None:
        to_lang = _language_id.recognize(__to_lang)
        if to_lang is not None:
            result = __safe_conversion_map(from_lang, to_lang, __line_delimiter)
    return result


def __build_convert_str_method(from_lang: str, to_lang: str):
    conversion_map = __get_str_conversion_map(from_lang, to_lang)

    def method(__str: str):
        return _convert_str.with_conversion_map(__str, conversion_map=conversion_map)

    return method


def __get_convert_str_method(__from_lang: str, __to_lang: str) -> Callable[[str], str]:
    kwargs = dict(
        from_lang=__from_lang,
        to_lang=__to_lang,
        id=__from_lang + "->" + __to_lang,
        callback=__build_convert_str_method,
    )
    return __conversion_map_cache.get(**kwargs)


def convert_str(__str: str, from_lang: str, to_lang: str) -> str:
    return __get_convert_str_method(from_lang, to_lang)(__str)


def get_convert_text_method(from_lang: str, to_lang: str) -> Callable[[str], str]:
    return __get_convert_str_method(from_lang, to_lang)


def get_str_conversion_map(from_lang: str, to_lang: str) -> dict[str, str]:
    return __get_str_conversion_map(from_lang, to_lang)


def iter_alternate_language_ids(
    __language_id: str, delimiters: tuple[str] = _constants.LANGUAGE_ID_DELIMITERS
):
    return _language_id.iter_alternate_language_ids(
        __language_id, delimiters=delimiters
    )

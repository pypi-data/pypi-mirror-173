from . import constants as _constants


def __iter_alternate_language_ids(__language_id: str, delimiters: tuple[str]):
    results = [__language_id]
    append = results.append
    if "-" in __language_id:
        for delim in delimiters:
            alt_id = __language_id.replace("-", delim)
            append(alt_id)
            append(alt_id.upper())
        alt_id = __language_id.split("-", 1)[1]
        if alt_id:
            append(alt_id)
            append(alt_id.upper())
    return iter(results)


def __recognize_language_id(__language_id: str, delimiters: tuple[str]):

    if __language_id in _constants.LANGUAGE_IDS:
        result = __language_id
    else:
        result = None
        for language_id in _constants.LANGUAGE_IDS:
            if result is None:
                for alternate_id in __iter_alternate_language_ids(
                    language_id, delimiters=delimiters
                ):
                    if __language_id == alternate_id:
                        result = language_id
                        break
    return result


def iter_alternate_language_ids(__language_id: str, delimiters: tuple[str]):
    return __iter_alternate_language_ids(__language_id, delimiters=delimiters)


def recognize(
    __language_id: str, delimiters: tuple[str] = _constants.LANGUAGE_ID_DELIMITERS
):
    return __recognize_language_id(__language_id, delimiters=delimiters)

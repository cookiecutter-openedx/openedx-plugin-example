import json
from dateutil.parser import parse, ParserError
from unittest.mock import MagicMock
from collections.abc import MutableMapping

from opaque_keys.edx.locator import CourseLocator

SENSITIVE_KEYS = [
    "password",
    "token",
    "client_id",
    "client_secret",
    "Authorization",
    "secret",
]


def flatten_dict(dictionary, parent_key="", sep="_"):
    """
    Generate a flatten dictionary-like object.
    Taken from:
    https://stackoverflow.com/a/6027615/16823624
    """
    items = []
    for key, value in dictionary.items():
        new_key = parent_key + sep + key if parent_key else key
        if isinstance(value, MutableMapping):
            items.extend(flatten_dict(value, new_key, sep=sep).items())
        else:
            items.append((new_key, value))
    return dict(items)


def serialize_course_key(inst, field, value):  # pylint: disable=unused-argument
    """
    Serialize instances of CourseLocator.
    When value is anything else returns it without modification.
    """
    if isinstance(value, CourseLocator):
        return str(value)
    return value


def objects_key_by(iter, key):
    index = {}
    for obj in iter:
        value = getattr(obj, key)
        index[value] = obj
    return index


def parse_date_string(date_string, raise_exception=False):
    try:
        return parse(date_string)
    except (TypeError, ParserError):
        if not raise_exception:
            return
        raise


def masked_dict(obj) -> dict:
    """
    To mask sensitive key / value in log entries.
    masks the value of specified key.
    obj: a dict or a string representation of a dict, or None
    """

    def redact(key: str, obj):
        if key in obj:
            obj[key] = "*** -- REDACTED -- ***"
        return obj

    obj = obj or {}
    obj = dict(obj)
    for key in SENSITIVE_KEYS:
        obj = redact(key, obj)
    return obj


class PluginJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding="utf-8")
        if isinstance(obj, MagicMock):
            return ""
        try:
            return json.JSONEncoder.default(self, obj)
        except Exception:
            # obj probably is not json serializable.
            return ""

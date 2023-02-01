import base64
from typing import Any
from urllib.parse import unquote

from benedict.serializers.abstract import AbstractSerializer
from benedict.utils import type_util


class Base64CoreSerializer(AbstractSerializer):
    """
    This class describes a base64 core serializer.
    """

    def __init__(self):
        super().__init__(
            extensions=[
                "b64",
                "base64",
            ],
        )

    def _fix_url_encoding_and_padding(self, s: str) -> str:
        # fix urlencoded chars
        s = unquote(s)
        # fix padding
        m = len(s) % 4
        if m != 0:
            s += "=" * (4 - m)
        return s

    def decode(self, s: str, **kwargs: Any):
        value = self._fix_url_encoding_and_padding(s)
        encoding = kwargs.pop("encoding", "utf-8")
        # if encoding:
        #    value = value.encode(encoding)
        value = base64.b64decode(value).decode(encoding)
        # if encoding:
        #     return value.decode(encoding)
        return value

    def encode(self, d, **kwargs: Any) -> str:
        value = d
        encoding = kwargs.pop("encoding", "utf-8")
        if encoding and type_util.is_string(value):
            value = value.encode(encoding)
        value = base64.b64encode(value)
        if encoding:
            value = value.decode(encoding)
        return value


class Base64Serializer(Base64CoreSerializer):
    def __init__(self):
        super().__init__()

    def _pop_options(self, options):
        encoding = options.pop("encoding", "utf-8")
        subformat = options.pop("subformat", None)
        from benedict.serializers import get_serializer_by_format

        serializer = get_serializer_by_format(subformat)
        return (serializer, encoding)

    def decode(self, s: str, **kwargs: Any):
        serializer, encoding = self._pop_options(kwargs)
        value = super().decode(s, encoding=encoding)
        if serializer:
            value = serializer.decode(value, **kwargs)
        return value

    def encode(self, d, **kwargs: Any) -> str:
        serializer, encoding = self._pop_options(kwargs)
        value = d
        if serializer:
            value = serializer.encode(value, **kwargs)
        value = super().encode(value, encoding=encoding)
        return value

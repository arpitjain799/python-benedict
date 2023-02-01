import plistlib
from typing import Any

from benedict.serializers.abstract import AbstractSerializer


class PListSerializer(AbstractSerializer):
    """
    This class describes a p list serializer.
    https://docs.python.org/3/library/plistlib.html
    """

    def __init__(self):
        super().__init__(
            extensions=[
                "plist",
            ],
        )

    def decode(self, s: str, **kwargs: Any):
        kwargs.setdefault("fmt", plistlib.FMT_XML)
        encoding = kwargs.pop("encoding", "utf-8")
        return plistlib.loads(s.encode(encoding), **kwargs)

    def encode(self, d, **kwargs: Any) -> str:
        encoding = kwargs.pop("encoding", "utf-8")
        return plistlib.dumps(d, **kwargs).decode(encoding)

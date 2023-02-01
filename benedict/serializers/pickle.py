import base64
import pickle
from typing import Any

from benedict.serializers.abstract import AbstractSerializer


class PickleSerializer(AbstractSerializer):
    """
    This class describes a pickle serializer.
    """

    def __init__(self):
        super().__init__(
            extensions=[
                "pickle",
            ],
        )

    def decode(self, s: str, **kwargs: Any):
        encoding = kwargs.pop("encoding", "utf-8")
        return pickle.loads(base64.b64decode(s.encode(encoding)), **kwargs)

    def encode(self, d, **kwargs: Any) -> str:
        encoding = kwargs.pop("encoding", "utf-8")
        kwargs.setdefault("protocol", 2)
        return base64.b64encode(pickle.dumps(d, **kwargs)).decode(encoding)

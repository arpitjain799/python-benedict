from typing import Any

from benedict.serializers import JSONSerializer


def dump(obj: Any, **kwargs: Any) -> str:
    serializer = JSONSerializer()
    options = {"indent": 4, "sort_keys": True}
    options.update(**kwargs)
    try:
        output = serializer.encode(obj, **options)
        return output
    except TypeError as error:
        sort_keys = options.pop("sort_keys", False)
        if sort_keys:
            output = serializer.encode(obj, **options)
            return output
        raise error

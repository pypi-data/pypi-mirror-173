from dataclasses import dataclass, field


@dataclass(frozen=False, order=True)
class ConversionMapCache:

    limit: int = field(init=True, default=10)
    data: dict = field(init=True, default_factory=dict)
    ids: list = field(init=True, default_factory=list)

    def __contains__(self, __key: str):
        return __key in self.data

    def __getitem__(self, __key: str):
        return self.data[__key]

    def __setitem__(self, __key: str, __value):
        self.data[__key] = __value
        self.ids.append(__key)
        if len(self.ids) > self.limit:
            while len(self.ids) > self.limit:
                first_id = self.ids[0]
                del self[first_id]
                self.ids = self.ids[1:]

    def __delitem__(self, __key: str):
        if __key in self.data:
            del self.data[__key]

    def get(self, **kwargs):
        data_id = kwargs.get("id", None)
        if data_id is not None:
            if data_id in self:
                result = self[data_id]
            else:
                callback = kwargs["callback"]
                del kwargs["id"]
                del kwargs["callback"]
                result = callback(**kwargs)
                self[data_id] = result
        else:
            result = None
        return result

from copy import copy


class DummyNestedNamespace:

    def __init__(self, data):
        data = copy(data)
        for key, value in data.items():
            if type(value) is dict:
                data[key] = DummyNestedNamespace(value)
        self.data = data

    def __getattr__(self, name):
        namespace = self.data
        keys = name.split('.')
        value = namespace[keys[0]]
        if len(keys) > 1 and keys[1]:
            return getattr(value, '.'.join(keys[1:]))
        return value

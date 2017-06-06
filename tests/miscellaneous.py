from copy import deepcopy
from tempfile import NamedTemporaryFile


class DummyNestedNamespace:

    def __init__(self, data):
        data = deepcopy(data)
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

    def get(self, name, default):
        try:
            return self.__getattr__(name)
        except KeyError:
            return default


def create_named_temp_file(data='', **kwargs):
    temporary_file = NamedTemporaryFile(mode='w', delete=False, **kwargs)

    temporary_file.close()
    name = temporary_file.name

    with open(name, 'w') as f:
        f.write(data)

    return name

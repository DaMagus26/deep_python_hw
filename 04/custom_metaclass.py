class CustomMeta(type):
    def __new__(mcs, name, bases, dct):
        new_dct = {}

        # Changing initial attributes names
        for attr_name, attr_value in dct.items():
            if not attr_name.startswith("__") or not attr_name.endswith("__"):
                new_dct["custom_" + attr_name] = attr_value
            else:
                new_dct[attr_name] = attr_value

        # Adding __setattr__ method
        setattr_method = new_dct.get('__setattr__', None)

        def __setattr__(self, key, value):
            if setattr_method:
                setattr_method(self, 'custom_' + key, value)
            else:
                self.__dict__['custom_' + key] = value

        new_dct['__setattr__'] = __setattr__
        cls_instance = super().__new__(mcs, name, bases, new_dct)

        return cls_instance


if __name__ == '__main__':
    class Child(metaclass=CustomMeta):
        pass

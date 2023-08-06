from .entityMeta import EntityMeta
from .fields import Field
from .query import Query


class Entity(object, metaclass=EntityMeta):
    def __init__(self, *args, new=True, **kwargs):
        if args:
            raise TypeError('%s constructor accept only keyword arguments. Got: %d positional argument%s'
                                 % (self.__name__, len(args), len(args) > 1 and 's' or ''))
        # print(kwargs)
        # print('adf', self.attrs)
        for atr in self.attrs:
            if atr.name in kwargs:
                atr.changed = new
                atr.value = kwargs[atr.name]
        # for key in kwargs:
        #     self.__setattr__(key, kwargs[key])

    @property
    def fields(self):
        return self.__dict__.items()

    def save(self):
        return Query.save_item(self)
        # self.save_item(self)

    @classmethod
    def from_dict(cls, obj):
        return cls(new=False, **obj)

    def __getattribute__(self, item):
        field = object.__getattribute__(self, item)
        if isinstance(field, Field):
            return field.value
        return field

    def __setattr__(self, key, value):
        if key in self.attrs_dict:
            field = object.__getattribute__(self, key)
            field.value = value
            field.changed = True
        else:
            self.__dict__[key] = value

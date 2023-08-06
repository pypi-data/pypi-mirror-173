from .entityMeta import EntityMeta
from .query import Query


class Entity(object, metaclass=EntityMeta):
    def __init__(self, *args, **kwargs):
        if args:
            raise TypeError('%s constructor accept only keyword arguments. Got: %d positional argument%s'
                                 % (self.__name__, len(args), len(args) > 1 and 's' or ''))
        # print(kwargs)
        # print(self.attrs)
        for key in kwargs:
            self.__setattr__(key, kwargs[key])

    @property
    def fields(self):
        return self.__dict__.items()

    def save(self):
        return Query.save_item(self)
        # self.save_item(self)


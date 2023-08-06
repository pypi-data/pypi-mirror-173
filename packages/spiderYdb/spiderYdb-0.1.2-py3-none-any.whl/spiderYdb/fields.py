from ydb import PrimitiveType
# import uuid
import shortuuid

shortuuid.set_alphabet("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")


class Field:
    title = 'String'

    def __init__(self, pk=False):
        self.pk = pk
        self.changed = False

    def __eq__(self, other):
        # ==
        return '=', self, other

    def __ne__(self, other):
        # !=
        return '!=', self, other

    def __lt__(self, other):
        # <
        return '<', self, other

    def __le__(self, other):
        # <=
        return '<=', self, other

    def __gt__(self, other):
        # >
        return '>', self, other

    def __ge__(self, other):
        # >=
        return '>=', self, other

    def _init_(self, table, name):
        self.table = table
        self.name = name

    @property
    def need_update(self):
        if self.pk or (hasattr(self, 'value') and self.changed):
            return True

class Utf8(Field):
    title = 'Utf8'
    ydb_type = PrimitiveType.Utf8


class Uuid(Utf8):
    @staticmethod
    def new():
        return shortuuid.uuid()

    def __getattr__(self, item):
        if item == 'value' and self.pk:
            value = self.new()
            self.value = value
            self.changed = True
            return self.new()
        else:
            raise AttributeError(f"{self.__class__.__name__} object has no attribute {item}")


class Int64(Field):
    title = 'Int64'
    ydb_type = PrimitiveType.Int64


class Uint64(Field):
    title = 'Uint64'
    ydb_type = PrimitiveType.Uint64


class Bool(Field):
    title = 'Bool'
    ydb_type = PrimitiveType.Bool


class Datetime(Field):
    title = 'Bool'
    ydb_type = PrimitiveType.Datetime

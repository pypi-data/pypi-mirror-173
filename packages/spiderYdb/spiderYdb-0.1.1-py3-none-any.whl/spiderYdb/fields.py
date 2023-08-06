from ydb import PrimitiveType
import uuid

class Field:
    title = 'String'

    def __init__(self, pk=False):
        self.pk = pk

    def __eq__(self, other):
        # ==
        return '==', self, other

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


class Utf8(Field):
    title = 'Utf8'
    ydb_type = PrimitiveType.Utf8


class Uuid(Utf8):
    @staticmethod
    def new():
        return uuid.uuid4().hex


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

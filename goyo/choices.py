from typing import Union, Type


class ChoicesMeta(type):
    class ILLEGAL_CHOICE:
        ...

    def __new__(metacls, cls, bases, attrs):
        c = super().__new__(metacls, cls, bases, attrs)
        c.ILLEGAL_CHOICE = metacls.ILLEGAL_CHOICE
        c._members = {k: v for k, v in attrs.items() if not k.startswith('_')}
        c._reversed_members = {v: k for k, v in c._members.items()}

        def __init__(self, name: str, value: str):
            self.name = name
            self.value = value

        c.__init__ = __init__

        @classmethod
        def select(cls, name: str) -> Union[Type[metacls.ILLEGAL_CHOICE], cls]:
            value = c._members.get(name)
            if not value:
                return metacls.ILLEGAL_CHOICE
            return c(name, value)

        @classmethod
        def of(cls, value: str) -> Union[Type[metacls.ILLEGAL_CHOICE], cls]:
            name = c._reversed_members.get(value)
            if not name:
                return metacls.ILLEGAL_CHOICE
            return c(name, value)

        def __eq__(self, other):
            return self.name == other.name and self.value == other.value

        c.select = select
        c.of = of
        c.__eq__ = __eq__
        return c

    def __str__(cls) -> str:
        s = '/'.join(cls._members.values())
        return f'[{s}]'


class ChoiceEnum(metaclass=ChoicesMeta):
    ...
from typing import Union, Type


class ILLEGAL_CHOICE:
    ...


class ChoicesMeta(type):
    def __new__(metacls, cls, bases, attrs):
        c = super().__new__(metacls, cls, bases, attrs)
        c._members = {k: v for k, v in attrs.items() if not k.startswith('_')}
        c._reversed_members = {v: k for k, v in c._members.items()}

        @classmethod
        def select(cls, name: str) -> Union[Type[ILLEGAL_CHOICE], cls]:
            if name not in  c._members:
                return ILLEGAL_CHOICE
            return getattr(c(), name)

        @classmethod
        def of(cls, value: str) -> Union[Type[ILLEGAL_CHOICE], cls]:
            name = c._reversed_members.get(value)
            if not name:
                return ILLEGAL_CHOICE
            return getattr(c(), name)

        c.select = select
        c.of = of
        return c

    def __str__(cls) -> str:
        s = '/'.join(cls._members.values())  # type: ignore
        return f'[{s}]'


class ChoiceEnum(metaclass=ChoicesMeta):
    ...
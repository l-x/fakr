from typing import Iterator
from collections import Mapping


class TemplatedMapping(Mapping):

    def __init__(self, renderer: callable, **kwargs) -> None:
        self.__render=renderer
        self.__data=kwargs

    def __len__(self) -> int:
        return len(self.__data)

    def __getitem__(self, key: str) -> str:
        return self.__render(self.__data[key], self.__data)

    def __setitem__(self, key, value) -> None:
        self.__data[key]=value

    def __iter__(self) -> Iterator:
        return iter(self.__data)


def templated_mapping(renderer: callable) -> callable:
    return lambda **kwargs: TemplatedMapping(renderer, **kwargs)
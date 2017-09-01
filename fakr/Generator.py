import collections
import time
import random


class Generator:
    def __init__(self, renderer: callable, vocabulary: collections.Sequence, template_string: str):
        self.__vocabulary=vocabulary
        self.__render=renderer
        self.__template_string=template_string

    def __call__(self, count: int, delay: float) -> collections.Iterator:
        counter=0
        while count==-1 or counter < count:
            time.sleep(delay)
            yield self.__render(self.__template_string, random.choice(self.__vocabulary), row=counter)
            counter += 1

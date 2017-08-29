import jinja2
from collections import Mapping
from functools import lru_cache


class Jinja2Renderer:
    __max_recursions=10

    def __init__(self, jinja2_env: jinja2.Environment, template_prefix: str=None) -> None:
        self.__jinja2_env=jinja2_env
        self.__tpl_prefix=template_prefix

    @lru_cache(maxsize=128)
    def __get_template_object(self, tpl_str: str) -> jinja2.Template:
        return self.__jinja2_env.from_string(tpl_str)

    def __render(self, value: str, mapping: Mapping, extra: Mapping, recursions=0) -> str:
        data=dict(extra)
        data.update(mapping)

        assert recursions <= self.__max_recursions # todo: Raise specific exception

        if self.__tpl_prefix is None:
            return self.__get_template_object(value).render(**data)

        if str(value).startswith(self.__tpl_prefix):
            return self.__render(
                self.__get_template_object(value[len(self.__tpl_prefix):]).render(**data),
                mapping,
                extra,
                recursions+1
            )

        return value

    def __call__(self, value: str, mapping: Mapping, **extra) -> str:
        return self.__render(value, mapping, extra, recursions=0)


import jinja2
import unidecode
import random
import uuid
import time

custom_filters = dict(
    ascii=lambda value: unidecode.unidecode(str(value)),
    shuffle=lambda value: ''.join(random.sample(str(value), len(str(value)))),
    chance=lambda value, chance: value if random.uniform(0.0, 1.0) <= chance else '',
    rjust=lambda value, width, fillchar = ' ': str(value).rjust(width, fillchar),
    ljust=lambda value, width, fillchar = ' ': str(value).ljust(width, fillchar),
    center=lambda value, width, fillchar=' ': str(value).center(width, fillchar),
)

custom_globals=dict(
    translate=lambda value, **dictionary: dictionary[value],
    uuid4=lambda: str(uuid.uuid4()),
    unixtime=time.time
)


def environment() -> jinja2.Environment:
    env = jinja2.Environment()

    env.filters.update(custom_filters)
    env.globals.update(custom_globals)

    return env

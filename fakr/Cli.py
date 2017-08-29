from collections import Mapping, Sequence
import argparse
import sys
import os
import random
import time
from .Jinja2Renderer import Jinja2Renderer
from .CompoundMappingSequence import CompoundMappingSequence
from .TemplatedMapping import templated_mapping
from .jinja import environment
import jinja2.exceptions
from . import version, package_name

ENV_FAKR_VOCABUALRY= 'FAKR_VOCABULARY'


class Cli:

    def __init__(self, data: Sequence, renderer: callable):
        self.__data=data
        self.__render=renderer

    def __iterate(self, count: int, delay: float):
        counter=0
        while count==-1 or counter < count:
            yield random.choice(self.__data)
            time.sleep(delay)
            counter+=1

    def __real_main(self, template, count, delay):
        for row, item in enumerate(self.__iterate(count, delay)):
            print(self.__render(template, item, row=row))

    @staticmethod
    def main():
        j2env=environment()
        args=Cli.__parse_args()

        vocabulary=Cli.__load_vocabulary(args['vocabulary'], j2env)

        if args['list'] is True:
            print('\n'.join(sorted([v for v in list(vocabulary[0].keys()) + ['row']])))
            exit(0)

        if args['info'] is True:
            print('{}: {} unique entries'.format(args['vocabulary'].name, len(vocabulary)))
            exit(0)

        template = args['template'].read()
        renderer = Jinja2Renderer(j2env, template_prefix=None)

        try:
            Cli(vocabulary, renderer).__real_main(template, args['count'], args['delay'])
        except KeyboardInterrupt:
            exit(0)
        except jinja2.exceptions.TemplateError as e:
            sys.stderr.write('There was a problem with your templates: {}'.format(e.message))

    @staticmethod
    def __load_vocabulary(fp, j2env) -> Sequence:
        import json
        partitions=json.load(fp)
        mapping_factory=templated_mapping(Jinja2Renderer(j2env, template_prefix='%%'))
        return CompoundMappingSequence(mapping_factory, *partitions)

    @staticmethod
    def __parse_args() -> Mapping:
        parser = argparse.ArgumentParser(
            prog=package_name,
            description='''
                {} reads a jinja2 template from STDIN or from a file, renders it with random values from the
                builtin us_top1000 vocabulary or from a custom file and writes the result to STDOUT
            '''.format(package_name)
        )

        meta_group=parser.add_argument_group('Information')

        meta_group.add_argument('--version',
                            action='version',
                            version='%(prog)s {}'.format(version)
                            )

        parser.add_argument('-c', '--count',
                            metavar='COUNT',
                            type=int,
                            default=-1,
                            help='Number of datasets to generate, defaults to 0 (unlimited)'
                            )

        parser.add_argument('-d', '--delay',
                            metavar='SECONDS',
                            type=float,
                            default=0,
                            help='Wait SECONDS between dataset generation, defaults to 0 (no waiting)'
                            )

        meta_group.add_argument('-l', '--list',
                            action='store_true',
                            help='show the available variables and exit'
                            )

        meta_group.add_argument('-i', '--info',
                            action='store_true',
                            help='show some vocabulary information and exit'
                            )

        parser.add_argument('-t', '--template',
                            metavar='FILENAME',
                            type=argparse.FileType('r'),
                            help='Path to the template file. If omitted the template is read from STDIN',
                            default=sys.stdin
                            )

        parser.add_argument('-v', '--vocabulary',
                            metavar='FILENAME',
                            type=argparse.FileType('r'),
                            help='Path to the vocabulary file. Defaults to the builtin us_top1000 vocabulary. This setting overrides the vocabulary selection via the environment variable FAKR_VOCABULARY',
                            default=os.getenv(ENV_FAKR_VOCABUALRY, os.path.dirname(os.path.realpath(__file__)) + '/vocabularies/us_top1000.json'))

        return vars(parser.parse_args())
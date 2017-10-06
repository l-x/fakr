from collections import Mapping, Sequence
import argparse
import sys
import os
from .Jinja2Renderer import Jinja2Renderer
from .CompoundMappingSequence import CompoundMappingSequence
from .TemplatedMapping import templated_mapping
from .jinja import environment
import jinja2.exceptions
from . import version, package_name, default_vocabulary, vocabulary
from .Generator import Generator

ENV_FAKR_VOCABUALRY= 'FAKR_VOCABULARY'
ENV_FAKR_MIXIN= 'FAKR_MIXIN'


def main():
    j2env = environment()
    args = __parse_args()

    vocabulary_fps=args['vocabulary'] + args['mixin']
    vocabulary = load_vocabulary(j2env, *vocabulary_fps)

    if args['list'] is True:
        sys.stdout.write('\n'.join(sorted([v for v in list(vocabulary[0].keys()) + ['row']])) + '\n')
        exit(0)

    if args['info'] is True:
        try:
            voclen=len(vocabulary)
        except OverflowError:
            voclen='Too many'

        sys.stdout.write('{} unique entries in\n{}\n'.format(voclen, '\n'.join(['\t- ' + os.path.realpath(fp.name) for fp in vocabulary_fps])))
        exit(0)

    try:
        generator = Generator(Jinja2Renderer(j2env, template_prefix=None), vocabulary, sys.stdin.read())
        for item in generator(args['count'], args['delay']):
            sys.stdout.write(item + '\n')
    except KeyboardInterrupt:
        exit(0)
    except jinja2.exceptions.TemplateError as e:
        sys.stderr.write('There was a problem with your templates: {}'.format(e.message))
    except OSError as e:
        sys.stderr.write(e.strerror)


def load_vocabulary(j2env, *fps) -> Sequence:
    partitions=list()
    for fp in fps:
        partitions+=vocabulary.read(fp)

    mapping_factory=templated_mapping(Jinja2Renderer(j2env, template_prefix='%%'))
    return CompoundMappingSequence(mapping_factory, *partitions)


def __parse_args() -> Mapping:
    parser = argparse.ArgumentParser(
        prog=package_name,
        description='''
            {} reads a jinja2 template from STDIN or from a file, renders it with random values from a vocabulary or from a custom file and writes the result to STDOUT
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

    parser.add_argument('-v', '--vocabulary',
                        metavar='FILENAME',
                        action=VocabularyFileAction,
                        help='Path to the vocabulary file. Defaults to the builtin vocabulary "{}". This setting overrides the vocabulary selection via the environment variable FAKR_VOCABULARY'.format(os.path.basename(default_vocabulary)),
                        default=VocabularyFileAction.openFiles(os.getenv(ENV_FAKR_VOCABUALRY, default_vocabulary)))

    parser.add_argument('-m', '--mixin',
                        metavar='FILENAME',
                        action=VocabularyFileAction,
                        help='Additional vocabulary files to mix into the main vocabulary. This setting overrides the vocabulary selection via the environment variable FAKR_MIXIN',
                        nargs='*',
                        default=VocabularyFileAction.openFiles(*[v.strip() for v in filter(None, os.getenv(ENV_FAKR_MIXIN, '').split(':'))])
                        )

    return vars(parser.parse_args())


class VocabularyFileAction(argparse.Action):

    @staticmethod
    def openFiles(*files: str, resolver: callable = lambda v: v) -> list:
        fps=[]
        for file in files:
            try:
                fp = open(resolver(file), 'rb')
                fps.append(fp)
            except FileNotFoundError as e:
                print('{}: {}'.format(file, e.strerror))
                exit(1)

        return fps

    def __call__(self, parser, args, values, option_string=None):
        if type(values) is str:
            values=[values]

        setattr(args, self.dest, self.openFiles(*values, resolver=vocabulary.search))
from unittest import TestCase
from unittest.mock import MagicMock
from fakr.TemplatedMapping import TemplatedMapping, templated_mapping
import collections


class TestTemplatedMapping(TestCase):

    renderer=MagicMock()
    mapping=dict(key1='value1', key2='value2', key3='value3')

    def setUp(self):
        self.subject=TemplatedMapping(self.renderer, **self.mapping)

    def test_is_mapping(self):
        self.assertIsInstance(self.subject, collections.Mapping)

    def test_len(self):
        self.assertIs(len(self.subject), len(self.mapping))

    def test_getitem(self):
        self.renderer.side_effect=lambda value, data: value

        for k, v in self.mapping.items():
            actual=self.subject[k]

            call_args=self.renderer.call_args[0]
            expected=(v, self.mapping)

            self.assertIs(actual, self.mapping[k])
            self.assertEqual(expected, call_args)

    def test_iter(self):
        self.assertIsInstance(iter(self.subject), collections.Iterator)

    def test_templated_mapping(self):
        mapping_factory=templated_mapping(self.renderer)
        self.assertTrue(callable(mapping_factory))

        subject=mapping_factory(**self.mapping)
        self.assertIsInstance(subject, TemplatedMapping)

        self.assertEqual(self.mapping, subject._TemplatedMapping__data)
        self.assertIs(self.renderer, subject._TemplatedMapping__render)
import unittest
from fakr.CompoundMappingSequence import CompoundMappingSequence


class TestCompoundMappingSequence(unittest.TestCase):
    partitions=[
        [
            dict(a='1', b='2', c='3'),
            dict(a='4', b='5', c='6'),
        ],
        [
            dict(d='1', e='2', f='3'),
            dict(d='4', e='5', f='6'),
        ],
    ]

    expected=[
        dict(id=0, guid='cfcd2084-95d5-65ef-66e7-dff9f98764da', a='1', b='2', c='3', d='1', e='2', f='3'),
        dict(id=1, guid='c4ca4238-a0b9-2382-0dcc-509a6f75849b', a='4', b='5', c='6', d='1', e='2', f='3'),
        dict(id=2, guid='c81e728d-9d4c-2f63-6f06-7f89cc14862c', a='1', b='2', c='3', d='4', e='5', f='6'),
        dict(id=3, guid='eccbc87e-4b5c-e2fe-2830-8fd9f2a7baf3', a='4', b='5', c='6', d='4', e='5', f='6'),
    ]

    sequence_length=4

    def setUp(self):
        self.mapping_factory=dict

        self.subject=CompoundMappingSequence(self.mapping_factory, *self.partitions)

    def test_len(self):
        self.assertIs(self.sequence_length, len(self.subject))

    def test_getitem_raises_index_error(self):
        try:
            self.subject[self.sequence_length+1]
        except IndexError as e:
            return

        self.fail('Expected IndexError was not raised')

    def test_getitem(self):
        for k, v in enumerate(self.subject):
            self.assertEqual(v, self.expected[k])
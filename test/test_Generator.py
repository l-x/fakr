import unittest
from unittest import mock
from fakr.Generator import Generator
import collections


class TestGenerator(unittest.TestCase):
    def setUp(self):
        self.template_string='template string'
        self.vocabulary=['vo', 'ca', 'bu', 'lary']
        self.renderer=mock.MagicMock()

        self.subject=Generator(self.renderer, self.vocabulary, self.template_string)

    def test_call_returns_iterator(self):
        self.assertIsInstance(self.subject(1, 1), collections.Iterator)

    @mock.patch('random.choice')
    @mock.patch('time.sleep')
    def test_iterator(self, mock_sleep, mock_choice):
        iterations=4
        delay=2

        self.renderer.side_effect = lambda t, v, **x: 'rendered'
        mock_choice.return_value='choice'
        subject=self.subject(iterations, delay)

        for row, item in enumerate(subject):
            self.renderer.assert_called_with(self.template_string, 'choice', row=row)
            mock_sleep.assert_called_with(delay)
            self.assertEqual('rendered', item)

        self.assertEqual(iterations, self.renderer.call_count)
        self.assertEqual(iterations, mock_sleep.call_count)


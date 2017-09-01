import unittest
from unittest import mock
from fakr import jinja


class TestCustomFilters(unittest.TestCase):

    def setUp(self):
        self.subject=jinja.custom_filters

    @mock.patch('unidecode.unidecode', side_effect=lambda v: v)
    def test_ascii(self, mock_unidecode: mock.MagicMock):
        test_value='value'
        value=mock.MagicMock()
        value.__str__.return_value=test_value

        self.assertIs(test_value, self.subject['ascii'](value))
        value.__str__.assert_called_once_with()
        mock_unidecode.assert_called_once_with(test_value)

    @mock.patch('random.sample', side_effect=lambda v, _: v)
    def test_shuffle(self, mock_sample: mock.MagicMock):
        test_value='value'
        value=mock.MagicMock()
        value.__str__.return_value=test_value

        self.assertIn(test_value, self.subject['shuffle'](value))
        value.__str__.assert_called_with()
        mock_sample.assert_called_once_with(test_value, len(test_value))

    def test_chance(self):
        def assertChance(test_value: str, test_chance: float, expected_value: str):
            random_uniform_result=0.5
            with mock.patch('random.uniform', side_effect=lambda f, t: random_uniform_result) as mock_uniform:
                self.assertIs(expected_value, self.subject['chance'](test_value, test_chance))
                mock_uniform.assert_called_once_with(0.0, 1.0)

        assertChance('value', 0.0, '')
        assertChance('value', 0.49999999999, '')
        assertChance('value', 0.5, 'value')
        assertChance('value', 1.0, 'value')
        assertChance('value', 1234, 'value')

    def assertStringFunction(self, filter: str, value: str, width: int, fillchar: str, expected: str):
        value_mock=mock.MagicMock()
        value_mock.__str__.return_value=value

        self.assertEqual(expected, self.subject[filter](value_mock, width, fillchar))
        value_mock.__str__.assert_called_once_with()

    def test_ljust(self):
        self.assertStringFunction('ljust', 'v', 3, 'x', 'vxx')

    def test_rjust(self):
        self.assertStringFunction('rjust', 'v', 3, 'x', 'xxv')

    def center(self):
        self.assertStringFunction('center', 'v', 3, 'x', 'xvx')


class TestCustomGlobals(unittest.TestCase):

    def setUp(self):
        self.subject=jinja.custom_globals

    def test_translate(self):
        test_value='test_value'
        expected_value='expected_value'

        self.assertEqual(expected_value, self.subject['translate'](test_value, test_value=expected_value))

    def test_unixtime(self):
        import time
        self.assertIs(self.subject['unixtime'], time.time)

    @mock.patch('uuid.uuid4')
    def test_uuid4(self, mock_uuid: mock.MagicMock):
        uuid_value='test-uuid'
        uuid4=mock.MagicMock()
        uuid4.__str__.return_value=uuid_value
        mock_uuid.return_value=uuid4

        self.assertEqual(uuid_value, self.subject['uuid4']())
        uuid4.__str__.assert_called_once_with()
        mock_uuid.assert_called_once_with()


class TestEnvironment(unittest.TestCase):

    @mock.patch('jinja2.Environment')
    def test_environment(self, mock_env):
        env=mock_env.return_value

        self.assertIs(env, jinja.environment())
        env.filters.update.assert_called_once_with(jinja.custom_filters)
        env.globals.update.assert_called_once_with(jinja.custom_globals)
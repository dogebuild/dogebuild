import unittest

from doge_script import process_arguments as parse


class ArgsParsing(unittest.TestCase):
    """\
    Test argument parsing function

    NB: 'doge' in array is for beauty reason (mimics call from shell). First argument contains script path and always be
    ignored.
    """
    def test_no_arg(self):
        res = parse([
            'doge',
        ])
        self.assertEqual(res, {
            'no': True,
        })

    def test_init(self):
        res = parse([
            'doge',
            'init',
        ])
        self.assertEqual(res, {
            'init': True,
            'use_venv': True,
        })

    def test_init_no_venv(self):
        res = parse([
            'doge',
            'init',
            '--no-venv',
        ])
        self.assertEqual(res, {
            'init': True,
        })

    def test_unknown(self):
        res = parse([
            'doge',
            'some_nonexisting_command',
        ])
        self.assertEquals(res, {
            'unknown': True
        })

    def test_help(self):
        res  = parse([
            'doge',
            'help',
        ])
        self.assertEquals(res, {
            'help': True,
        })


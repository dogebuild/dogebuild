import unittest

from doge_script import process_arguments as parse


class ArgsParsing(unittest.TestCase):
    def test_no_arg(self):
        res = parse([
            'Path_to_exec_never_checked',
        ])
        self.assertEqual(res, {
            'no': True,
        })

    def test_init(self):
        res = parse([
            'Path_to_exec_never_checked',
            'init',
        ])
        #self.assertEqual(res, {
        #    'no': True,
        #})


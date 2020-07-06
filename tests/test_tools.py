from unittest import TestCase
from os import environ

from dogebuild.tools import Environment


class TestEnvironment(TestCase):
    def test_environment(self):
        environ["A"] = "A"
        environ["B"] = "B"

        with Environment({"B": "NEW_B"}):
            environ["C"] = "NEW_C"

            self.assertEqual(environ["A"], "A", "Do not see outer inside scope")
            self.assertEqual(environ["B"], "NEW_B", "Changed env do not appear inside scope")
            self.assertEqual(environ["C"], "NEW_C", "New env do not appear inside scope ")

        self.assertEqual(environ["A"], "A", "Env was changed inside scope")
        self.assertEqual(environ["B"], "B", "New value appear inside scope")
        self.assertTrue("C" not in environ, "Changes can be seen outside scope")

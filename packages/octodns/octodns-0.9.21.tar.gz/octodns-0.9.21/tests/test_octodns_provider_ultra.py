#
#
#

from unittest import TestCase


class TestUltraShim(TestCase):
    def test_missing(self):
        with self.assertRaises(ModuleNotFoundError):
            from octodns.provider.ultra import UltraProvider

            UltraProvider

#
#
#

from unittest import TestCase


class TestOvhShim(TestCase):
    def test_missing(self):
        with self.assertRaises(ModuleNotFoundError):
            from octodns.provider.ovh import OvhProvider

            OvhProvider

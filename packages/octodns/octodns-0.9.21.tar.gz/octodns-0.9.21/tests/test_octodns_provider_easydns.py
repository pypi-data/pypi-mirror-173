#
#
#

from unittest import TestCase


class TestEasyDnsShim(TestCase):
    def test_missing(self):
        with self.assertRaises(ModuleNotFoundError):
            from octodns.provider.easydns import EasyDnsProvider

            EasyDnsProvider

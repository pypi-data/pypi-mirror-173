#
#
#

from unittest import TestCase


class TestEtcHostsShim(TestCase):
    def test_missing(self):
        with self.assertRaises(ModuleNotFoundError):
            from octodns.provider.etc_hosts import EtcHostsProvider

            EtcHostsProvider

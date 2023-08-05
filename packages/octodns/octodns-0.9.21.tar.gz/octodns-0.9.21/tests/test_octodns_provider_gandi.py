#
#
#

from unittest import TestCase

# Just for coverage
import octodns.provider.fastdns

# Quell warnings
octodns.provider.fastdns


class TestGandiShim(TestCase):
    def test_missing(self):
        with self.assertRaises(ModuleNotFoundError):
            from octodns.provider.gandi import GandiProvider

            GandiProvider

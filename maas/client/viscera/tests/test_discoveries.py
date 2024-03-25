"""Test for `maas.client.viscera.discoveries`"""

import datetime

from ..discoveries import Discoveries, Discovery

from testtools.matchers import Equals

from ..testing import bind
from ...testing import make_string_without_spaces, TestCase

from ...errors import ParameterNotSupplied, OperationNotAllowed


def make_origin():
    """
    Create a new origin with Spaces and Space. The former
    refers to the latter via the origin, hence why it must be bound.
    """
    return bind(Discoveries, Discovery)


class TestDiscoveries(TestCase):

    def test__discoveries_read(self):
        Discoveries = make_origin().Discoveries
        discoveries = [
            {
                "id": make_string_without_spaces(),
                "ip": "127.0.0.1",
                "mac_address": make_string_without_spaces(),
                "hostname": "localhost",
                "fabric_name": make_string_without_spaces(),
                "last_seen": datetime.datetime.now(tz=datetime.timezone.utc),
                "vid": None,
            }
            for _ in range(2)
        ]
        Discoveries._handler.read.return_value = discoveries
        discoveries = Discoveries.read()
        self.assertThat(len(discoveries), Equals(2))

    def test__discoveries_clear_no_parameter(self):
        Discoveries = make_origin().Discoveries
        self.assertRaises(ParameterNotSupplied, Discoveries.clear)

    def test__discoveries_clear_all(self):
        Discoveries = make_origin().Discoveries
        Discoveries.clear(all=True)
        Discoveries._handler.clear.assert_called_once_with(
            all=True, mdns=False, neighbours=False
        )

    def test__discoveries_scan_all_not_force(self):
        Discoveries = make_origin().Discoveries
        self.assertRaises(OperationNotAllowed, Discoveries.scan)

    def test__discoveries_scan_all_force(self):
        Discoveries = make_origin().Discoveries
        Discoveries.scan(force=True)
        Discoveries._handler.scan.assert_called_once_with(
            always_use_ping=False, force=True, slow=False, threads=0
        )


class TestDiscovery(TestCase):

    def test__discovery_read(self):
        Discovery = make_origin().Discovery
        discovery = {
            "id": make_string_without_spaces(),
            "ip": "127.0.0.1",
            "mac_address": make_string_without_spaces(),
            "hostname": "localhost",
            "fabric_name": make_string_without_spaces(),
            "last_seen": datetime.datetime.now(tz=datetime.timezone.utc),
            "vid": None,
        }
        Discovery._handler.read.return_value = discovery
        self.assertThat(
            Discovery.read(discovery_id=discovery["id"]), Equals(Discovery(discovery))
        )
        Discovery._handler.read.assert_called_once_with(discovery_id=discovery["id"])

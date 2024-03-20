"""Objects for Network discoveries"""

from . import (
    check,
    check_optional,
    parse_timestamp,
    Object,
    ObjectType,
    ObjectSet,
    OriginObjectRef,
    ObjectField,
)


class DiscoveriesType(ObjectType):
    """Metaclass for `Discoveries`."""

    async def read(cls):
        data = await cls._handler.read()
        return cls(map(cls._object, data))


class Discoveries(ObjectSet, metaclass=DiscoveriesType):
    """The set of network discoveries."""

    _object = OriginObjectRef("Discovery")


class DiscoveryType(ObjectType):
    """Metaclass for `Discovery`."""

    async def read(cls, id: str):
        data = await cls._handler.read(discovery_id=id)
        return cls(data)


class Discovery(Object, metaclass=DiscoveryType):
    """A network discovery."""

    id = ObjectField.Checked("discovery_id", check(str), readonly=True)
    ip = ObjectField.Checked("ip", check(str), readonly=True)
    mac_address = ObjectField.Checked("mac_address", check(str), readonly=True)
    last_seen = ObjectField.Checked("last_seen", parse_timestamp, readonly=True)
    hostname = ObjectField.Checked("hostname", check_optional(str), readonly=True)
    fabric_name = ObjectField.Checked("fabric_name", check(str), readonly=True)
    vid = ObjectField.Checked("vid", check_optional(int), readonly=True)

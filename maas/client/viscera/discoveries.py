"""Objects for Network discoveries"""

from maas.client.errors import ParameterNotSupplied, OperationNotAllowed

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

    async def clear(
        cls, all: bool = False, mdns: bool = False, neighbours: bool = False
    ):
        """Deletes all discovered neighbours and/or mDNS entries."""
        if not (all or mdns or neighbours):
            raise ParameterNotSupplied(
                "One of `mdns`, `neighbours`, or `all` parameters must be supplied."
            )
        await cls._handler.clear(all=all, mdns=mdns, neighbours=neighbours)

    async def scan(
        cls,
        always_use_ping: bool = False,
        cidr: str = "",
        force: bool = False,
        slow: bool = False,
        threads: int = 0,
    ):
        """Immediately run a neighbour discovery scan on all rack networks."""
        if cidr == "" and not force:
            message = """Scanning all subnets is not allowed unless force=True is specified.
            **WARNING: This will scan ALL networks attached to MAAS rack controllers.
            Check with your internet service provider or IT department to be sure this is
            allowed before proceeding.**"""
            raise OperationNotAllowed(message)
        if cidr == "":
            await cls._handler.scan(
                always_use_ping=always_use_ping, force=force, slow=slow, threads=threads
            )
        else:
            await cls._handler.scan(
                always_use_ping=always_use_ping,
                cidr=cidr,
                force=force,
                slow=slow,
                threads=threads,
            )


class Discoveries(ObjectSet, metaclass=DiscoveriesType):
    """The set of network discoveries."""

    _object = OriginObjectRef("Discovery")


class DiscoveryType(ObjectType):
    """Metaclass for `Discovery`."""

    async def read(cls, discovery_id: str):
        data = await cls._handler.read(discovery_id=discovery_id)
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

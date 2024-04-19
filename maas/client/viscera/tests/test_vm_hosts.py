"""Test for `maas.client.viscera.vmhosts`."""

import random

from testtools.matchers import Equals, IsInstance

from ...errors import OperationNotAllowed
from ..vm_hosts import VmHost, VmHosts
from ..testing import bind
from ...testing import make_name_without_spaces, make_string_without_spaces, TestCase


def make_origin():
    """
    Create a new origin with VmHosts and VmHost. The former
    refers to the latter via the origin, hence why it must be bound.
    """
    return bind(VmHosts, VmHost)


def make_vmhost():
    """Returns a vmhost dictionary."""
    return {
        "id": random.randint(1, 100),
        "type": make_name_without_spaces("type"),
        "name": make_name_without_spaces("name"),
        "architectures": [make_string_without_spaces() for _ in range(3)],
        "capabilities": [make_string_without_spaces() for _ in range(3)],
        "zone": {
            "id": random.randint(1, 100),
            "name": make_name_without_spaces("name"),
            "description": make_name_without_spaces("description"),
        },
        "tags": [make_string_without_spaces() for _ in range(3)],
        "cpu_over_commit_ratio": random.uniform(0, 10),
        "memory_over_commit_ratio": random.uniform(0, 10),
        "available": {
            "cores": random.randint(1, 100),
            "memory": random.randint(4096, 8192),
            "local_storage": random.randint(1024, 1024 * 1024),
        },
        "used": {
            "cores": random.randint(1, 100),
            "memory": random.randint(4096, 8192),
            "local_storage": random.randint(1024, 1024 * 1024),
        },
        "total": {
            "cores": random.randint(1, 100),
            "memory": random.randint(4096, 8192),
            "local_storage": random.randint(1024, 1024 * 1024),
        },
    }


class TestVmHosts(TestCase):
    def test__vmhosts_create(self):
        type = make_string_without_spaces()
        power_address = make_string_without_spaces()
        power_user = make_string_without_spaces()
        power_pass = make_string_without_spaces()
        name = make_string_without_spaces()
        zone = make_string_without_spaces()
        tags = make_string_without_spaces()
        origin = make_origin()
        VmHosts, VmHost = origin.VmHosts, origin.VmHost
        VmHosts._handler.create.return_value = {}
        observed = VmHosts.create(
            type=type,
            power_address=power_address,
            power_user=power_user,
            power_pass=power_pass,
            name=name,
            zone=zone,
            tags=tags,
        )
        self.assertThat(observed, IsInstance(VmHost))
        VmHosts._handler.create.assert_called_once_with(
            type=type,
            power_address=power_address,
            power_user=power_user,
            power_pass=power_pass,
            name=name,
            zone=zone,
            tags=tags,
        )

    def test__vmhosts_create_raises_error_for_rsd_and_no_power_user(self):
        origin = make_origin()
        origin.VmHosts._handler.create.return_value = {}
        self.assertRaises(
            OperationNotAllowed,
            origin.VmHosts.create,
            type="rsd",
            power_address=make_string_without_spaces(),
        )

    def test__vmhosts_create_raises_error_for_rsd_and_no_power_pass(self):
        origin = make_origin()
        origin.VmHosts._handler.create.return_value = {}
        self.assertRaises(
            OperationNotAllowed,
            origin.VmHosts.create,
            type="rsd",
            power_address=make_string_without_spaces(),
            power_user=make_string_without_spaces(),
        )

    def test__vmhosts_create_raises_type_error_for_zone(self):
        origin = make_origin()
        origin.VmHosts._handler.create.return_value = {}
        self.assertRaises(
            TypeError,
            origin.VmHosts.create,
            type=make_string_without_spaces(),
            power_address=make_string_without_spaces(),
            power_user=make_string_without_spaces(),
            power_pass=make_string_without_spaces(),
            zone=0.1,
        )

    def test__vmhosts_read(self):
        VmHosts = make_origin().VmHosts
        vmhosts = [make_vmhost() for _ in range(3)]
        VmHosts._handler.read.return_value = vmhosts
        vmhosts = VmHosts.read()
        self.assertThat(len(vmhosts), Equals(3))


class TestVmHost(TestCase):
    def test__vmhost_read(self):
        VmHost = make_origin().VmHost
        vmhost = make_vmhost()
        VmHost._handler.read.return_value = vmhost
        self.assertThat(VmHost.read(id=vmhost["id"]), Equals(VmHost(vmhost)))
        VmHost._handler.read.assert_called_once_with(id=vmhost["id"])

    def test__vmhost_refresh(self):
        VmHost = make_origin().VmHost
        vmhost_data = make_vmhost()
        vmhost = VmHost(vmhost_data)
        vmhost.refresh()
        VmHost._handler.refresh.assert_called_once_with(id=vmhost_data["id"])

    def test__vmhost_parameters(self):
        VmHost = make_origin().VmHost
        vmhost_data = make_vmhost()
        vmhost = VmHost(vmhost_data)
        vmhost.parameters()
        VmHost._handler.parameters.assert_called_once_with(id=vmhost_data["id"])

    def test__vmhost_compose(self):
        VmHost = make_origin().VmHost
        vmhost_data = make_vmhost()
        vmhost = VmHost(vmhost_data)
        cores = random.randint(1, 100)
        memory = random.randint(4096, 8192)
        cpu_speed = random.randint(16, 256)
        architecture = make_name_without_spaces("architecture")
        storage = make_string_without_spaces()
        hostname = make_name_without_spaces("hostname")
        domain = random.randint(1, 10)
        zone = random.randint(1, 10)
        interfaces = make_string_without_spaces()
        vmhost.compose(
            cores=cores,
            memory=memory,
            cpu_speed=cpu_speed,
            architecture=architecture,
            storage=storage,
            hostname=hostname,
            domain=domain,
            zone=zone,
            interfaces=interfaces,
        )
        VmHost._handler.compose.assert_called_once_with(
            id=vmhost_data["id"],
            cores=str(cores),
            memory=str(memory),
            cpu_speed=str(cpu_speed),
            architecture=architecture,
            storage=storage,
            hostname=hostname,
            domain=str(domain),
            zone=str(zone),
            interfaces=interfaces,
        )

    def test__vmhost_compose_raises_type_error_for_zone(self):
        VmHost = make_origin().VmHost
        vmhost_data = make_vmhost()
        vmhost = VmHost(vmhost_data)
        cores = random.randint(1, 100)
        memory = random.randint(4096, 8192)
        cpu_speed = random.randint(16, 256)
        architecture = make_name_without_spaces("architecture")
        storage = make_string_without_spaces()
        hostname = make_name_without_spaces("hostname")
        domain = random.randint(1, 10)
        zone = 0.1
        interfaces = make_string_without_spaces()
        self.assertRaises(
            TypeError,
            vmhost.compose,
            cores=cores,
            memory=memory,
            cpu_speed=cpu_speed,
            architecture=architecture,
            storage=storage,
            hostname=hostname,
            domain=domain,
            zone=zone,
            interfaces=interfaces,
        )

    def test__vmhost_delete(self):
        VmHost = make_origin().VmHost
        vmhost_data = make_vmhost()
        vmhost = VmHost(vmhost_data)
        vmhost.delete()
        VmHost._handler.delete.assert_called_once_with(id=vmhost_data["id"])

    def test__save_add_tag(self):
        VmHost = make_origin().VmHost
        vmhost_data = make_vmhost()
        vmhost = VmHost(vmhost_data)
        tag = make_string_without_spaces()
        vmhost.tags.append(tag)
        VmHost._handler.add_tag.return_value = None
        vmhost.save()
        VmHost._handler.add_tag.assert_called_once_with(id=vmhost.id, tag=tag)

    def test__save_remove_tag(self):
        VmHost = make_origin().VmHost
        vmhost_data = make_vmhost()
        tag = make_string_without_spaces()
        vmhost_data["tags"] = [tag]
        vmhost = VmHost(vmhost_data)
        vmhost.tags.remove(tag)
        VmHost._handler.remove_tag.return_value = None
        vmhost.save()
        VmHost._handler.remove_tag.assert_called_once_with(id=vmhost.id, tag=tag)

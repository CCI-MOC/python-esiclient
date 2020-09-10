#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

from esiclient.tests import base
from esiclient.v1 import network_subnet


class TestCreate(base.TestCommand):

    def setUp(self):
        super(TestCreate, self).setUp()
        self.cmd = network_subnet.Create(self.app, None)
        self.network_attrs = {
            "name": "network1",
            "shared": True,
            "provider:network_type": "vlan",
            "provider:physical_network": "datacentre",
            "provider:segmentation_id": "111"}

        self.network_dict = self.network_attrs.copy()
        self.network_dict.update({
            "id": "uuid_network_1"
        })

        self.subnet_attrs = {
            "name": "subnet1",
            "network_id": "uuid_network_1",
            "ip_version": 4,
            "cidr": "192.168.199.0/24",
            "gateway_ip": "192.168.199.200",
            "allocation_pools": [{
                "start": "192.168.199.200", "end": "192.168.199.254"
                }],
            "enable_dhcp": True}

        self.subnet_dict = self.subnet_attrs.copy()
        self.subnet_dict.update({
            "id": "uuid_subnet_1",
        })

        self.app.client_manager.network.create_network.\
            return_value = {"network": self.network_dict}

        self.app.client_manager.network.create_subnet.\
            return_value = {"subnet": self.subnet_dict}

    def test_take_action(self):
        arglist = [
            "--network-name", "network1",
            "--provider-network-type", "vlan",
            "--provider-physical-network", "datacentre",
            "--provider-segment", "111",
            "--share",
            "--subnet-name", "subnet1",
            "--subnet-range", "192.168.199.0/24",
            "--gateway", "192.168.199.200",
            "--ip-version", "4",
            "--dhcp",
            "--allocation-pool", "start=192.168.199.200,end=192.168.199.254"]

        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        res = self.cmd.take_action(parsed_args)
        expected = (
            ["Network", "Network ID", "Subnet", "Subnet ID"],
            ["network1", "uuid_network_1", "subnet1", "uuid_subnet_1"]
        )
        self.assertEqual(res, expected)

        self.app.client_manager.network.create_network.\
            assert_called_once_with(**self.network_attrs)

        self.app.client_manager.network.create_subnet.\
            assert_called_once_with(**self.subnet_attrs)

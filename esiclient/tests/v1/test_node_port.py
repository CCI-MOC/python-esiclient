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
from esiclient.tests import utils
from esiclient.v1 import node_port


class TestCreate(base.TestCommand):

    def setUp(self):
        super(TestCreate, self).setUp()
        self.cmd = node_port.Create(self.app, None)
        self.node_info = {
            "uuid": "node_uuid_1",
            "name": "node1",
            "driver": "ipmi",
            "driver_info": {
                "ipmi_password": 123456,
                "ipmi_username": "root",
                "ipmi_port": 111,
                "ipmi_address": "0.0.0.1"
            },
            "resource_class": "baremetal"
        }
        self.node = utils.create_mock_object(self.node_info)
        self.port = utils.create_mock_object({
            "uuid": "port_uuid_1",
            "address": "0.0.0.2",
            "node_uuid": "node_uuid_1",
            "local_link_connection": {
                "switch_info": "switch1"
            },
            "physical_network": "datacentre"
        })

        self.app.client_manager.baremetal.node.create.\
            return_value._info = self.node_info

        self.app.client_manager.baremetal.port.create.\
            return_value = self.port

    def test_take_action(self):
        arglist = ["--node-name", "node1",
                   "--driver", "ipmi",
                   "--driver-info", "ipmi_username=root",
                   "--driver-info", "ipmi_password=123456",
                   "--driver-info", "ipmi_port=111",
                   "--driver-info", "ipmi_address=0.0.0.1",
                   "--resource-class", "baremetal",
                   "--port-address", "0.0.0.2",
                   "--local-link-connection", "switch_info=switch1",
                   "--physical-network", "datacentre"]
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        res = self.cmd.take_action(parsed_args)
        expected = (
            ["Node", "Node ID", "Port ID", "Port address"],
            ["node1", "node_uuid_1", "port_uuid_1", "0.0.0.2"]
        )
        self.assertEqual(res, expected)
        self.app.client_manager.baremetal.node.create. assert_called_once_with(
            name=self.node.name,
            driver=self.node.driver,
            driver_info=self.node.driver_info,
            resource_class=self.node.resource_class)

        self.app.client_manager.baremetal.port.create. assert_called_once_with(
            address=self.port.address,
            node_uuid=self.port.node_uuid,
            local_link_connection=self.port.local_link_connection,
            physical_network=self.port.physical_network)

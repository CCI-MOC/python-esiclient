#    Copyright (c) 2016 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import ddt
from tempest.lib import exceptions

from esiclient.tests.functional import base
from esiclient.tests.functional import utils


@ddt.ddt
class NodePowerTests(base.ESIBaseTestClass):
    """Functional tests for esi node power commands."""

    @classmethod
    def setUpClass(cls):
        super(NodePowerTests, cls).setUpClass()

        cls._init_dummy_project(cls, 'random', 'member')

    def setUp(self):
        super(NodePowerTests, self).setUp()
        self.clients = NodePowerTests.clients
        self.users = NodePowerTests.users
        self.projects = NodePowerTests.projects

    def test_owner_can_node_power_on_off(self):
        """Tests owner power functionality.

        Tests owner `baremetal node power on <node>` and
        `baremetal node power off <node>`.

        Test steps:
        1) Create a node and set its 'owner' field to project_id of a
            a random project.
        2) Check that the project can run `node power on` and
            `node power off`
        3) (cleanup) Delete the node created in step 1.

        """
        node = utils.node_create(self.clients['admin'])
        self.addCleanup(utils.node_delete,
                        self.clients['admin'],
                        identifier=node['name'])

        utils.node_set(self.clients['admin'],
                       identifier=node['name'],
                       owner=self.projects['random']['id'])

        utils.node_power_on(self.clients['random-member'],
                            identifier=node['name'])
        utils.node_power_off(self.clients['random-member'],
                             identifier=node['name'])

    def test_lessee_can_node_power_on_off(self):
        """Tests lessee power funcitonality.

        Tests that a node's 'lessee' can `baremetal node power on <node>`
        and `baremetal node power off <node>.

        Test steps:
            1) Create a node and set its 'lessee' field to project_id of a
                a random project.
            2) Check that the project can run `node power on` and
                `node power off`
            3) (cleanup) Delete the node created in step 1.
        """
        node = utils.node_create(self.clients['admin'])
        self.addCleanup(utils.node_delete,
                        self.clients['admin'],
                        identifier=node['name'])

        utils.node_set(self.clients['admin'],
                       identifier=node['name'],
                       lessee=self.projects['random']['id'])

        utils.node_power_on(self.clients['random-member'],
                            identifier=node['name'])
        utils.node_power_off(self.clients['random-member'],
                             identifier=node['name'])

    def test_non_owner_lessee_cannot_node_power_on_off(self):
        """Tests non owner and non lessee power functionality.

        Tests that a project which is not set to a node's 'owner' nor
            'lessee' cannot run `baremetal node power on <node>` or
            `baremetal node power off <node>.
            Test steps:
            1) Create a node
            2) Check that the project cannot run `node power on` or
                `node power off`
            3) (cleanup) Delete the node created in step 1.
        """
        node = utils.node_create(self.clients['admin'])
        self.addCleanup(utils.node_delete,
                        self.clients['admin'],
                        identifier=node['name'])

        self.assertRaises(exceptions.CommandFailed,
                          utils.node_power_on,
                          self.clients['random-member'],
                          identifier=node['name'])

        self.assertRaises(exceptions.CommandFailed,
                          utils.node_power_off,
                          self.clients['random-member'],
                          identifier=node['name'])

    def test_admin_can_node_power_on_off(self):
        """Tets admin power functionality.

        Tests that an admin project which is not set to a node's 'owner'
            nor 'lessee' cannot run `baremetal node power on <node>` or
            `baremetal node power off <node>.
            Test steps:
            1) Create a node
            2) Check that the project can run `node power on` and
                `node power off`
            3) (cleanup) Delete the node created in step 1.
        """
        node = utils.node_create(self.clients['admin'],
                                 name="owned")
        self.addCleanup(utils.node_delete,
                        self.clients['admin'],
                        identifier=node['name'])

        utils.node_power_on(self.clients['admin'], identifier=node['name'])
        utils.node_power_off(self.clients['admin'], identifier=node['name'])
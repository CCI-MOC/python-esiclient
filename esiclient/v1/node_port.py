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

import json
import logging
from osc_lib.command import command
from osc_lib import exceptions
from osc_lib.i18n import _


def _get_attrs_node(parsed_args):
    attrs = {}
    field_list = ["name", "driver", "driver_info", "resource_class"]
    attrs = dict((k, v) for (k, v) in vars(parsed_args).items()
                 if k in field_list and v is not None)
    if "driver_info" in attrs:
        attrs["driver_info"] = param_array_to_dict(attrs["driver_info"])
    return attrs


def _get_attrs_port(parsed_args):
    attrs = {}
    field_list = ["address", "node_uuid", "local_link_connection",
                  "physical_network"]
    attrs = dict((k, v) for (k, v) in vars(parsed_args).items()
                 if k in field_list and v is not None)
    if "local_link_connection" in attrs:
        attrs["local_link_connection"] = param_array_to_dict(
            attrs["local_link_connection"])
    return attrs


def param_array_to_dict(param_array):
    """Convert ['k1=v1', 'k2=v2' ...] to {k1: v1, k2: v2}"""
    def _maybe_json(v):
        try:
            return json.loads(v)
        except ValueError:
            return v

    param_dict = {}
    try:
        param_dict = dict((y[0], _maybe_json(y[1])) for y in [
            x.split("=", 1) for x in param_array
        ])
    except ValueError:
        raise exceptions.CommandError(
            "ERROR: attributes must be a list of KEY=VALUE")

    return param_dict


class Create(command.ShowOne):
    """Create baremetal port and set the switch config"""
    log = logging.getLogger(__name__ + ".Create")

    def get_parser(self, prog_name):
        parser = super(Create, self).get_parser(prog_name)
        parser.add_argument(
            "--node-name",
            dest="name",
            metavar="<node_name>",
            help=_("Name of the node"))
        parser.add_argument(
            "--driver",
            metavar="<driver>",
            required=True,
            help=_("Driver used to control the node"))
        parser.add_argument(
            "--driver-info",
            dest="driver_info",
            metavar="<key=value>",
            action="append",
            help=_("Key/value pair used by the driver"))
        parser.add_argument(
            "--resource-class",
            metavar="<resource_class>",
            help=_("Resource class for mapping nodes to Nova flavors"))
        parser.add_argument(
            "--port-address",
            dest="address",
            metavar="<port_address>",
            help=_("MAC address for this port"))
        parser.add_argument(
            "--local-link-connection",
            metavar="<key=value>",
            action="append",
            help=_("Key/value metadata describing port Local link connection"
                   "information"))
        parser.add_argument(
            "--physical-network",
            metavar="<physical_network>",
            help=_("Name of the physical network to which this port is "
                   "connected"))

        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)
        ironic_client = self.app.client_manager.baremetal
        attrs_node = _get_attrs_node(parsed_args)
        node = ironic_client.node.create(**attrs_node)._info
        node_uuid = node["uuid"]
        attrs_port = _get_attrs_port(parsed_args)
        attrs_port["node_uuid"] = node_uuid
        port = ironic_client.port.create(**attrs_port)
        return ["Node", "Node ID", "Port ID", "Port address"], \
            [node["name"],
             node_uuid,
             port.uuid,
             port.address]

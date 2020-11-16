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

import logging

from osc_lib.cli import parseractions
from osc_lib.command import command
from osc_lib.i18n import _


def _get_attrs_network(parsed_args):
    attrs = {}
    if parsed_args.network_name:
        attrs["name"] = parsed_args.network_name
    if parsed_args.share:
        attrs["shared"] = True
    if parsed_args.provider_network_type:
        attrs["provider:network_type"] = parsed_args.provider_network_type
    if parsed_args.provider_physical_network:
        attrs["provider:physical_network"] = \
            parsed_args.provider_physical_network
    if parsed_args.provider_segment:
        attrs["provider:segmentation_id"] = parsed_args.provider_segment
    return attrs


def _get_attrs_subnet(parsed_args):
    attrs = {}
    if parsed_args.subnet_name:
        attrs["name"] = parsed_args.subnet_name
    if parsed_args.ip_version:
        attrs["ip_version"] = parsed_args.ip_version
    if parsed_args.subnet_range:
        attrs["cidr"] = parsed_args.subnet_range
    if parsed_args.gateway:
        attrs["gateway_ip"] = parsed_args.gateway.lower()
    if parsed_args.allocation_pools:
        attrs["allocation_pools"] = parsed_args.allocation_pools
    if parsed_args.dhcp:
        attrs["enable_dhcp"] = True
    return attrs


class Create(command.ShowOne):
    """Create network and subnet"""

    log = logging.getLogger(__name__ + ".Create")

    def get_parser(self, prog_name):
        parser = super(Create, self).get_parser(prog_name)
        parser.add_argument(
            "--network-name",
            metavar="<network_name>",
            help=_("Name of network"))
        parser.add_argument(
            "--provider-network-type",
            metavar="<provider_network_type>",
            help=_("Type of the provider network"))
        parser.add_argument(
            "--provider-physical-network",
            metavar="<provider_physical_network>",
            help=_("Name of the physical network "
                    "over which the virtual network is implemented"))
        parser.add_argument(
            "--provider-segment",
            metavar="<provider_segment>",
            help=_("VLAN ID for the VLAN networks"))
        parser.add_argument(
            "--share",
            action="store_true",
            default=None,
            help=_("Set the network as shared"))
        parser.add_argument(
            "--subnet-name",
            metavar="<subnet_name>",
            help=_("Name of subnet"))
        parser.add_argument(
            "--subnet-range",
            metavar="<subnet_range>",
            help=_("Subnet range in CIDR notation"))
        parser.add_argument(
            "--gateway",
            metavar="<gateway>",
            default="auto",
            help=_("Specify a gateway for the subnet"))
        parser.add_argument(
            "--ip-version",
            type=int,
            default=4,
            choices=[4, 6],
            help=_("IP version"))
        parser.add_argument(
            "--dhcp",
            action="store_true",
            help=_("Enable DHCP (default)"))
        parser.add_argument(
            "--allocation-pool",
            metavar="start=<ip-address>,end=<ip-address>",
            dest="allocation_pools",
            action=parseractions.MultiKeyValueAction,
            required_keys=["start", "end"],
            help=_("Allocation pool IP addresses for this subnet "
                   "e.g.: start=192.168.199.2,end=192.168.199.254"))

        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)
        attrs_network = _get_attrs_network(parsed_args)
        neutron_client = self.app.client_manager.network
        network = neutron_client.create_network(**attrs_network)
        net_dict = network["network"]
        network_id = net_dict["id"]
        attrs_subnet = _get_attrs_subnet(parsed_args)
        attrs_subnet["network_id"] = network_id
        subnet = neutron_client.create_subnet(**attrs_subnet)
        subnet_dict = subnet["subnet"]
        return ["Network", "Network ID", "Subnet", "Subnet ID"], \
            [net_dict["name"],
             network_id,
             subnet_dict["name"],
             subnet_dict["id"]
             ]

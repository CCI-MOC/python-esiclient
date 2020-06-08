# CLI commands documentation

This document will cover and document three commands, attach, detach, and list. All three commands have a a log variable as well as two functions, get_parser, and take_action. 

For each function the get_parser method is the same:
* The function can add a node, network, or port, depending on the class. 
* The parser is then returned. 

Links to the commands are here:
* [Attach](#attach)
* [Detach](#detach)
* [List](#list)


## <a name="attach"></a>Attach

The attach command will attack a network to a node. 

**get_parser**
* A node is required but a network and port are optional variables.

**take_action:** 
* The user must explicitly identify only one port or network. 
*`if node.provision_state == MANAGEABLE`, two lists, `node_revert`, and `node_update` are made.
* The lists are then given the node image source and the node capabilities, if they are not in the node info. 
* If the node is active, all baremetal ports are then checked for a free port, and an error message is shown if no ports are availible.
* If there is a free port, the node is attached to that port, if not it is attached to a network.
* The node, port address, network, fixed IP, and IP address are returned.

## <a name="detach"></a>Detach

The detach command will detach a network from a node. 

**get_parser**
* A node and a port are required variables, it cannot take in a network.

**take_action:**
* Assuming the node is correctly connected to the network, the node is then disconnected and the port is deleted.
* If the node is not attached an error message displays.

## <a name="list"></a>List

The list command will list the networks that are attached to a node. 

**get_parser**
* Both the node and network variables are optional, it cannot take in a port.

**take_action:**
* The function checks for a node and a network and sets up a data list to contain the data of said node and network.
* This data list as well as a list of strings explaining what value corresponds to which space in the data list is returned. 

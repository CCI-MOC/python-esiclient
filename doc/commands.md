# CLI commands documentation

This document will cover and document three commands, attach, detach, and list. All three commands have a a log variable as well as two functions, get_parser, and take_action. 

For each function the get_parser method is the same:
* The function can add a node or a network, in the attach and detach class these are required variables, but they are not required in the List class. 
* The parser is then returned. 

Links to the commands are here:
* [Attach](#attach)
* [Detach](#detach)
* [List](#list)


## <a name="attach"></a>Attach

The attach command will attack a network to a node.

**take_action:** 
* If the node and network are manageable, `if node.provision_state == MANAGEABLE`.
* The lists are then given the node image source and the node capabilities, if they are not in the node info. 
* If the node is active, all baremetal ports are then checked for a free port.
* If there is a free port, the node is attached to that network, and the node, port address, network, and fixed IP are returned.

## <a name="detach"></a>Detach

The detach command will detach a network from a node. 

**take_action:**
* Assuming the node is correctly connected to the network, the node is then disconnected and the port is deleted.
* If the node is not attached an error message displays.

## <a name="list"></a>List

The list command will list the networks that are attached to a node. 

**take_action:**
* The function checks for a node and a network and sets up a data list to contain the data of said node and network.
* This data list as well as a list of strings explaining what value corresponds to which space in the data list is returned. 

#!/usr/bin/env python3
'''
This NodeServer controls Indoor Air Quality.
Author: Donovan Clay
Author: Dorian Clay
'''


import udi_interface

'''
udi_interface has a LOGGER that is created by default and logs to:
  logs/debug.log
You can use LOGGER.info, LOGGER.warning, LOGGER.debug, LOGGER.error,
LOGGER.critical levels as needed in your node server.
'''
LOGGER = udi_interface.LOGGER

from nodes import TemplateController

if __name__ == "__main__":
    try:
        """
        Instantiates the Interface to Polyglot.

        * Optionally pass list of class names
          - PG2 had the controller node name here
        """
        polyglot = udi_interface.Interface([TemplateController])
        """
        Starts MQTT and connects to Polyglot.
        """
        polyglot.start()

        """
        Creates the Controller Node and passes in the Interface, the node's
        parent address, node's address, and name/title

        * address, parent address, and name/title are new for Polyglot
          version 3
        * use 'controller' for both parent and address and PG3 will be able
          to automatically update node server status
        """
        control = TemplateController(polyglot, 'controller', 'controller', 'Pikes Peak Controller')
        
        # This is how example2 starts the node.
        # IAQNode.TemplplateController(polyglot, 'controller', 'controller', 'Pikes Peak Controller')

        """
        Sits around and does nothing forever, keeping your program running.

        * runForever() moved from controller class to interface class in
          Polyglot version 3
        """
        polyglot.runForever()
    except (KeyboardInterrupt, SystemExit):
        LOGGER.warning("Received interrupt or exit...")
        """
        Catch SIGTERM or Control-C and exit cleanly.
        """
        polyglot.stop()
    except Exception as err:
        LOGGER.error('Excption: {0}'.format(err), exc_info=True)
    sys.exit(0)

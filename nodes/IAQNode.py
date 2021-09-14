
import udi_interface
import sys
import time
import urllib3

LOGGER = udi_interface.LOGGER

class IAQNode(udi_interface.Node):
    """
    This is the class that all the Nodes will be represented by. You will
    add this to Polyglot/ISY with the interface.addNode method.

    Class Variables:
    self.primary: String address of the parent node.
    self.address: String address of this Node 14 character limit.
                  (ISY limitation)
    self.added: Boolean Confirmed added to ISY

    Class Methods:
    setDriver('ST', 1, report = True, force = False):
        This sets the driver 'ST' to 1. If report is False we do not report
        it to Polyglot/ISY. If force is True, we send a report even if the
        value hasn't changed.
    reportDriver(driver, force): report the driver value to Polyglot/ISY if
        it has changed.  if force is true, send regardless.
    reportDrivers(): Forces a full update of all drivers to Polyglot/ISY.
    query(): Called when ISY sends a query request to Polyglot for this
        specific node
    """

    """
    id of the node from the nodedefs.xml that is in the profile.zip. This tells
    the ISY what fields and commands this node has.
    """
    id = 'IAQNodeid'

    """
    Optional.
    This is an array of dictionary items containing the variable names(drivers)
    values and uoms(units of measure) from ISY. This is how ISY knows what kind
    of variable to display. Check the UOM's in the WSDK for a complete list.
    UOM 2 is boolean so the ISY will display 'True/False'
    """
    drivers = [
        {'driver': 'ST', 'value': 0, 'uom': 2},
        {'driver': 'GV0', 'value': 0, 'uom': '7'},  # Total Exhaust CFM
        {'driver': 'GV1', 'value': 0, 'uom': '7'},  # Total Makeup Air CFM
        {'driver': 'GV2', 'value': 0, 'uom': '51'},  # 12in Fan Dimming Percent
        {'driver': 'GV3', 'value': 0, 'uom': '51'},  # 8in Fan Dimmming Percent
        {'driver': 'GV4', 'value': int(False), 'uom': '2'},  # 8in Fan Damper Open/Closed
    ]

    def __init__(self, polyglot, primary, address, name):
        """
        Optional.
        Super runs all the parent class necessities. You do NOT have
        to override the __init__ method, but if you do, you MUST call super.

        :param polyglot: Reference to the Interface class
        :param primary: Parent address
        :param address: This nodes address
        :param name: This nodes name
        """
        super(IAQNode, self).__init__(polyglot, primary, address, name)
        self.poly = polyglot
        self.lpfx = '%s:%s' % (address,name)

        self.poly.subscribe(self.poly.START, self.start, address)
        self.poly.subscribe(self.poly.POLL, self.poll)

        self.Exhaust_CFM = 45
        self.Makeup_CFM = 55

        self.reportDrivers()

    def start(self):
        """
        Optional.
        This method is called after Polyglot has added the node per the
        START event subscription above
        """
        LOGGER.debug('%s: get ST=%s',self.lpfx,self.getDriver('ST'))
        self.setDriver('ST', 1)
        LOGGER.debug('%s: get ST=%s',self.lpfx,self.getDriver('ST'))
        self.setDriver('ST', 0)
        LOGGER.debug('%s: get ST=%s',self.lpfx,self.getDriver('ST'))
        self.setDriver('ST', 1)
        LOGGER.debug('%s: get ST=%s',self.lpfx,self.getDriver('ST'))
        self.setDriver('ST', 0)
        LOGGER.debug('%s: get ST=%s',self.lpfx,self.getDriver('ST'))
        self.http = urllib3.PoolManager()

    #def poll(self, polltype):
        """
        This method is called at the poll intervals per the POLL event
        subscription during init.
        """

        # TODO: check if address is correct
        # response = self.isy.cmd('nodes/3F.AF.D2/query')
        # LOGGER.info(f'Got response from ISY for powder room: {response}')

    '''
    FROM EXAMPLE 2: "This is where the real work happens."  
    '''
    def poll(self, polltype):
        if 'longPoll' in polltype:
            LOGGER.debug('longPoll (node)')
            self.setDriver('GV0',self.Exhaust_CFM, True, True)
        else:
            LOGGER.debug('shortPoll (node)')
            self.setDriver('GV1',self.Makeup_CFM, True, True)
            if int(self.getDriver('ST')) == 1:
                self.setDriver('ST',0)
            else:
                self.setDriver('ST',1)
            LOGGER.debug('%s: get ST=%s',self.lpfx,self.getDriver('ST'))


    def cmd_on(self, command):
        """
        Example command received from ISY.
        Set DON on IAQNode.
        Sets the ST (status) driver to 1 or 'True'
        """
        self.setDriver('ST', 1)

    def cmd_off(self, command):
        """
        Example command received from ISY.
        Set DOF on IAQNode
        Sets the ST (status) driver to 0 or 'False'
        """
        self.setDriver('ST', 0)

    def cmd_ping(self,command):
        """
        Not really a ping, but don't care... It's an example to test LOGGER
        in a module...
        """
        LOGGER.debug("cmd_ping:")
        r = self.http.request('GET',"google.com")
        LOGGER.debug("cmd_ping: r={}".format(r))

    """
    This is a dictionary of commands. If ISY sends a command to the NodeServer,
    this tells it which method to call. DON calls setOn, etc.
    """
    commands = {
        'DON': cmd_on,
        'DOF': cmd_off,
        'PING': cmd_ping
    }


    def query(self,command=None):
        """
        Called by ISY to report all drivers for this node. This is done in
        the parent class, so you don't need to override this method unless
        there is a need.
        """
        self.reportDrivers()



   


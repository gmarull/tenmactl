from enum import Enum
import logging
import string
from time import sleep

from serial import Serial


__version__ = '0.2.0.dev0'
_logger = logging.getLogger(__name__)


class TenmaSupply(object):
    """Driver for the Tenma 72-XXXX power supplies.

    Args:
        device (str): Serial port (e.g. /dev/ttyACM0)
    """

    _BAUDRATE = 9600
    """int: Baudrate."""

    _RETRIES = 2
    """int: Response retries."""

    _T_RESP = 0.1
    """float: Response time (s)."""

    _STATUS_MODE = 0
    """int: Status mode bit."""

    _STATUS_BEEP = 4
    """int: Status beep bit."""

    _STATUS_LOCK = 5
    """int: Status lock bit."""

    _STATUS_OUTPUT = 6
    """int: Status output bit."""

    class MODE(Enum):
        """Mode."""
        CC = 0
        CV = 1

    def __init__(self, port):
        self._dev = Serial(port, baudrate=self._BAUDRATE)

        # NOTE: power supply does not have a way to query the state of some
        # parameters.
        self._ocp_enabled = False
        self._ovp_enabled = False

    def _request(self, command, raw=False):
        """Perform a request to the device.

        Notes:
            Unfortunately it is quite frequent to see garbage on the reply
            (sometimes even missing chars...!) or no-reply. For this reason a
            retry mechanism is implemented, and received response is filtered
            to ASCII-only characters.

        Args:
            command (str): Command.
            raw (bool, optional): Return raw response.

        Returns:
            str: Reply (if command ends with ``?``).
        """

        retries = 0
        while retries < self._RETRIES:
            _logger.debug('TX: %s', command)
            self._dev.write(command.encode('utf-8'))

            sleep(self._T_RESP)

            if not command.endswith('?'):
                return

            reply = self._dev.read(self._dev.in_waiting)
            if reply:
                _logger.debug('RX: %s', reply)
                if raw:
                    return reply

                return ''.join(filter(lambda x: x in string.printable,
                                      reply.decode('utf-8')))

            _logger.warning('Transmission retry')

    @property
    def identification(self):
        return self._request('*IDN?')

    @property
    def current(self):
        return float(self._request('ISET1?'))

    @current.setter
    def current(self, current):
        self._request('ISET1:{:.3f}'.format(current))

    @property
    def voltage(self):
        return float(self._request('VSET1?'))

    @voltage.setter
    def voltage(self, voltage):
        self._request('VSET1:{:.2f}'.format(voltage))

    @property
    def actual_current(self):
        return float(self._request('IOUT1?'))

    @property
    def actual_voltage(self):
        return float(self._request('VOUT1?'))

    @property
    def enabled(self):
        status = ord(self._request('STATUS?', raw=True))
        return (status & (1 << self._STATUS_OUTPUT)) != 0

    @enabled.setter
    def enabled(self, enabled):
        self._request('OUT' + ('1' if enabled else '0'))

    @property
    def mode(self):
        status = ord(self._request('STATUS?', raw=True))
        return self.MODE((status >> self._STATUS_MODE) & 0x1)

    @property
    def beep(self):
        status = ord(self._request('STATUS?', raw=True))
        return (status & (1 << self._STATUS_BEEP)) != 0

    @beep.setter
    def beep(self, enabled):
        self._request('BEEP' + ('1' if enabled else '0'))

    @property
    def locked(self):
        status = ord(self._request('STATUS?', raw=True))
        return (status & (1 << self._STATUS_LOCK)) != 0

    @property
    def ocp(self):
        return self._ocp_enabled

    @ocp.setter
    def ocp(self, enabled):
        self._ocp_enabled = enabled
        self._request('OCP' + ('1' if enabled else '0'))

    @property
    def ovp(self):
        return self._ovp_enabled

    @ovp.setter
    def ovp(self, enabled):
        self._ovp_enabled = enabled
        self._request('OVP' + ('1' if enabled else '0'))

    def recall(self, number):
        """Load settings from a memory slot.

        Args:
            number (int): Memory slot.
        """
        self._request('RCL{}'.format(number))

    def save(self, number):
        """Save current settings to a memory slot.

        Args:
            number (int): Memory slot.
        """
        self._request('SAV{}'.format(number))

import argparse
import logging
from time import sleep
import sys

from tenmactl import TenmaSupply


def main(port):
    supply = TenmaSupply(port)

    print('Connected device: {}'.format(supply.identification))
    print('Status:')
    print('\tEnabled: {}'.format(supply.enabled))
    print('\tBeep active: {}'.format(supply.beep))
    print('\tLocked: {}'.format(supply.locked))

    voltage = float(input('Enter voltage: '))
    supply.voltage = voltage

    current = float(input('Enter current: '))
    supply.current = current

    print('Enabling...')
    supply.enabled = True

    print('Press Ctrl+C to terminate')
    while True:
        try:
            sys.stdout.write('\033[K')
            print('Actual voltage/current/mode: {} V, {} A, {}'.format(
                  supply.actual_voltage, supply.actual_current, supply.mode))
            sys.stdout.write('\033[F')
            sleep(0.5)
        except KeyboardInterrupt:
            break

    print('Disabling...')
    supply.enabled = False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tenma Example')
    parser.add_argument('-p', '--port', type=str, required=True,
                        help='Serial port')
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug messages')

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    main(args.port)

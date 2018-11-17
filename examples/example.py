import argparse
import logging

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
    print('Actual voltage: {} V'.format(supply.actual_voltage))
    print('Actual current: {} A'.format(supply.actual_current))
    print('Mode: {}'.format(supply.mode))

    input('Pres ENTER to disable the power supply and terminate')
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

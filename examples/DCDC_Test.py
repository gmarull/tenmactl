from time import sleep
from tenmactl import TenmaLoad, TenmaSupply
import matplotlib.pyplot as plt

supply_port = 'COM4'
load_port = 'COM5'

set_supply_voltage = 24

supply = TenmaSupply(supply_port)
print('Connected device: {}'.format(supply.identification))
print('Status:')
print('\tEnabled: {}'.format(supply.enabled))
print('\tBeep active: {}'.format(supply.beep))
print('\tLocked: {}'.format(supply.locked))
print('Disabling...')
supply.enabled = False

load = TenmaLoad(load_port)
print('Connected device: {}'.format(load.identification))
print('Status:')
print('\tEnabled: {}'.format(load.enabled))
print(load.actual_voltage)
print(load.actual_current)
print(load.actual_power)
load.enabled = False
load.current = 0.001
load.mode = 'CC'

# Set DCDC input voltage and current limit
supply.voltage = set_supply_voltage
supply.current = 0.5
power_in = []
power_out = []
efficiency = []
current_out = []
voltage_out = []

for step in range(20):
    load.current = step * 0.01
    supply.enabled = True
    sleep(1)
    load.enabled = True
    sleep(2)
    Vin = supply.actual_voltage
    Iin = supply.actual_current
    Pin = Vin * Iin
    Vout = load.actual_voltage
    Iout = load.actual_current
    Pout = load.actual_power
    eff = Pout/Pin
    print(f"Vin: {Vin}, Iin: {Iin}, Vout: {Vout}, Iout: {Iout}, Pin: {Pin}, Pout {Pout},  Eff: {eff}")
    load.enabled = False
    supply.enabled = False
    power_in.append(Pin)
    power_out.append(Pout)
    efficiency.append(eff)
    current_out.append(Iout)
    voltage_out.append(Vout)
    sleep(2)
supply.enabled = False

plt.plot(power_in, power_out, label= 'Power out')
plt.plot(power_in, efficiency, label = 'Efficiency')
plt.xlabel('Power in')
plt.legend()
plt.grid()

plt.figure(2)
plt.plot(power_in, label= 'Power in')
plt.plot(power_out, label= 'Power out')
plt.plot(efficiency, label = 'Efficiency')
plt.xlabel('Step')
plt.legend()
plt.grid()

plt.figure(3)
plt.plot(voltage_out, label= 'Voltage out')
plt.xlabel('Step')
plt.ylabel('Voltage (V)')
plt.legend()
plt.grid()

plt.figure(4)
plt.plot(current_out, label= 'Current out')
plt.xlabel('Step')
plt.ylabel('Current (A)')
plt.legend()
plt.grid()

plt.show()


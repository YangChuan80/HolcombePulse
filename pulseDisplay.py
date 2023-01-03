import max30102
import hrcalc

import sys
import lcddriver

display = lcddriver.lcd()


m = max30102.MAX30102() # sensor initialization
#red, ir = m.read_sequential() # get LEDs readings

while(1):
    red, ir = m.read_sequential() # get LEDs readings
    d = hrcalc.calc_hr_and_spo2(ir[:100], red[:100]) # give 100 values
    print('心率', d[0], '     血氧', d[2], '%')
    
    display.lcd_display_string('HR: {:.0f} bpm    '.format(d[0]), 1)
    display.lcd_display_string('SpO2: {:.1f} %    '.format(d[2]), 2)

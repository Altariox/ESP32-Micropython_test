from machine import SoftI2C,Pin
import time
from lcd1602 import Lcd1602
i2c=SoftI2C(scl=Pin(22),sda=Pin(21),freq=400000)
lcd=Lcd1602(i2c)
while True:
    t=time.localtime()
    lcd.set_cursor(0,0); lcd.puts("Heure:")
    lcd.set_cursor(0,1); lcd.puts("{:02d}:{:02d}:{:02d}".format(t[3],t[4],t[5]))
    time.sleep(1)
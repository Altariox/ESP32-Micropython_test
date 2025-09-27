from machine import Pin
import time
from lcd1602 import Lcd1602
rs=Pin(15,Pin.OUT); e=Pin(2,Pin.OUT); d4=Pin(4,Pin.OUT); d5=Pin(5,Pin.OUT); d6=Pin(18,Pin.OUT); d7=Pin(19,Pin.OUT)
lcd=Lcd1602(rs,e,d4,d5,d6,d7)
while True:
    t=time.localtime(); lcd.set_cursor(0,0); lcd.putstr("Heure:"); lcd.set_cursor(0,1); lcd.putstr("{:02d}:{:02d}:{:02d}".format(t[3],t[4],t[5])); time.sleep(1)
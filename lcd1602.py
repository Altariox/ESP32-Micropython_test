import time
from machine import Pin

class Lcd1602:
    def __init__(self,rs,e,d4,d5,d6,d7):
        self.rs=rs; self.e=e; self.d4=d4; self.d5=d5; self.d6=d6; self.d7=d7
        for p in (rs,e,d4,d5,d6,d7): p.value(0)
        self._init()
    def _pulse(self):
        self.e.value(1); time.sleep_us(1); self.e.value(0); time.sleep_us(40)
    def _write4(self,n):
        self.d4.value((n>>0)&1); self.d5.value((n>>1)&1); self.d6.value((n>>2)&1); self.d7.value((n>>3)&1); self._pulse()
    def _cmd(self,c):
        self.rs.value(0); self._write4(c>>4); self._write4(c&0x0F); time.sleep_ms(2)
    def _data(self,c):
        self.rs.value(1); self._write4(c>>4); self._write4(c&0x0F)
    def _init(self):
        time.sleep_ms(50)
        for _ in range(3): self._write4(0x03); time.sleep_ms(5)
        self._write4(0x02)
        for c in (0x28,0x0C,0x06,0x01): self._cmd(c)
    def clear(self): self._cmd(0x01)
    def set_cursor(self,x,y): self._cmd((0x80,0xC0)[y]+x)
    def putstr(self,s):
        for ch in s: self._data(ord(ch))
    def puts(self,s,y=0,x=0):
        self.set_cursor(x,y); self.putstr(s)
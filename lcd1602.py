import time
from machine import SoftI2C, Pin

class Lcd1602:
    def __init__(self,i2c):
        self.i2c=i2c
        while True:
            s=i2c.scan()
            if s: self.LCD_I2C_ADDR=s[0]; break
            time.sleep_ms(10)
        self.bufs=[]; self.BK=0x08; self.RS=0; self.E=0x04
        for seq in (0x30,0x30,0x30,0x20):
            self.queue(seq); self.execute(); time.sleep_ms(5)
        self.add_command(0x28,run=True); self.on(); self.add_command(0x06); self.add_command(0x01); self.execute()

    def queue(self,dat):
        dat &= 0xF0; dat|=self.BK; dat|=self.RS
        self.bufs.append(dat|0x04); self.bufs.append(dat)
            
    def execute(self):
        if not self.bufs: return
        ba=bytearray(self.bufs)
        self.i2c.writeto(self.LCD_I2C_ADDR,ba)
        self.bufs=[]; time.sleep_us(50)

    def add_command(self,cmd,run=False):
        self.RS=0; self.queue(cmd); self.queue(cmd<<4)
        if run: self.execute()

    def add_data(self,dat):
        self.RS=1; self.queue(dat); self.queue(dat<<4)

    def clear(self): self.add_command(1,run=True)

    def backlight(self,on): self.BK=0x08 if on else 0; self.add_command(0,run=True)

    def on(self): self.add_command(0x0C,run=True)

    def off(self): self.add_command(0x08,run=True)

    def shl(self): self.add_command(0x18,run=True)

    def shr(self): self.add_command(0x1C,run=True)

    def char(self,ch,x=-1,y=0):
        if x>=0:
            a=0x80 if y==0 else 0xC0
            if y==2: a=0x80+20
            if y==3: a=0xC0+20
            a+=x; self.add_command(a)
        self.add_data(ch)

    def puts(self,s,y=0,x=0):
        if s:
            self.char(ord(s[0]),x,y)
            for c in s[1:]: self.char(ord(c))
        self.execute()

    def create_charactor(self,pos,char):
        assert len(char)==8
        pos&=0x7; self.add_command(0x40 | (pos<<3))
        for b in char: self.add_data(b)
        self.execute()

    def set_cursor(self,x,y): self.char(0,x,y)
    def putstr(self,s): self.puts(s,0,0)
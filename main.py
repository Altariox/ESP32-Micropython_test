from machine import Pin, SPI
import time
from mfrc522 import MFRC522
import max7219

# --- CONFIGURATION LED témoin ---
LED_ACTIVE_LOW = True
LED_GPIO = 14
led = Pin(LED_GPIO, Pin.OUT)

def led_on(): 
    led.value(1 if LED_ACTIVE_LOW else 0)

def led_off(): 
    led.value(0 if LED_ACTIVE_LOW else 1)

led_off()

# --- CONFIGURATION RFID MFRC522 ---
rdr = MFRC522(sck=18, mosi=23, miso=19, rst=22, cs=21)

last_uid = None
last_time = 0
DEBOUNCE_MS = 1500

def ms(): 
    return time.ticks_ms() if hasattr(time, 'ticks_ms') else int(time.time() * 1000)

# --- CONFIGURATION MATRICE LED (MAX7219 8x8) ---
spi = SPI(1, baudrate=10000000, polarity=0, phase=0,
          sck=Pin(18), mosi=Pin(23))
cs = Pin(5, Pin.OUT)  # adapter si besoin
display = max7219.Matrix8x8(spi, cs, 1)
display.brightness(5)
display.fill(0)
display.show()

# --- DÉFINITIONS DES CHIFFRES ---
numbers = {
    "3": [
        "01110",
        "10001",
        "00001",
        "00110",
        "00001",
        "10001",
        "01110",
    ],
    "2": [
        "01110",
        "10001",
        "00001",
        "00010",
        "00100",
        "01000",
        "11111",
    ],
    "1": [
        "00100",
        "01100",
        "00100",
        "00100",
        "00100",
        "00100",
        "01110",
    ],
    "0": [
        "01110",
        "10001",
        "10011",
        "10101",
        "11001",
        "10001",
        "01110",
    ]
}

def show_number(num):
    display.fill(0)
    for y, row in enumerate(numbers[num]):
        for x, col in enumerate(row):
            if col == "1":
                display.pixel(x+1, y+1, 1)
    display.show()

# --- COMPTE À REBOURS ---
def countdown():
    for n in ["3", "2", "1", "0"]:
        show_number(n)
        time.sleep(1)
    display.fill(0)
    display.show()

# --- BOUCLE PRINCIPALE ---
try:
    while True:
        status, bits = rdr.request(MFRC522.REQIDL)
        if status == MFRC522.OK:
            stat, uid = rdr.anticoll()
            if stat == MFRC522.OK and uid:
                uid_bytes = uid[:5] if len(uid) >= 5 else uid
                uid_str = "".join("{:02X}".format(x) for x in uid_bytes)
                t = ms()
                if uid_str != last_uid or (t - last_time) > DEBOUNCE_MS:
                    last_uid = uid_str
                    last_time = t
                    # Action : LED + compte à rebours
                    led_on()
                    countdown()
                    led_off()
        time.sleep(0.05)
except KeyboardInterrupt:
    pass
finally:
    led_off()
    display.fill(0)
    display.show()
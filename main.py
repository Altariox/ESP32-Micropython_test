from machine import Pin
import time
from mfrc522 import MFRC522

#=====================================================
# CONFIGURATION
#=====================================================
# Si ta LED est câblée: 3V3 -> Résistance -> LED -> GPIO14
# (cathode sur le GPIO) alors elle est ACTIVE LOW (niveau 0 = ON)
# Mettre LED_ACTIVE_LOW = True dans ce cas.
# Si la LED est: GPIO14 -> Résistance -> LED -> GND (anode au GPIO)
# alors LED_ACTIVE_LOW = False (niveau 1 = ON).
LED_ACTIVE_LOW = True  # Met à True seulement si ta LED est entre 3V3 et le GPIO (active bas). Si LED toujours allumée: inverse cette valeur.

LED_GPIO = 14

led = Pin(LED_GPIO, Pin.OUT)

def led_on():
    led.value(0 if LED_ACTIVE_LOW else 1)

def led_off():
    led.value(1 if LED_ACTIVE_LOW else 0)

# Assure OFF au démarrage
led_off()

#=====================================================
# Initialisation RC522 (adapter les GPIO si besoin)
#=====================================================
rdr = MFRC522(
    sck=18,
    mosi=23,
    miso=19,
    rst=22,
    cs=21
)

print("RFID prêt. Passe un badge...")

last_uid = None
last_time = 0
DEBOUNCE_MS = 1500

def ms():
    # Compat escalade si time.ticks_ms pas dispo
    return time.ticks_ms() if hasattr(time, 'ticks_ms') else int(time.time()*1000)

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
                    print("Carte détectée UID =", uid_str)
                    last_uid = uid_str
                    last_time = t
                    led_on()
                    time.sleep(1)
                    led_off()
        time.sleep(0.05)
except KeyboardInterrupt:
    print("Arrêt manuel.")
finally:
    # Garantit LED éteinte quand on quitte
    led_off()
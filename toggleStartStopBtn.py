# 2019 Jeep Cherokee Kl
# Mimics button press
from panda import Panda
import time

panda = Panda()
panda.set_safety_mode(Panda.SAFETY_ALLOUTPUT)

time.sleep(0.01)
start_time = time.time()

while time.time() - start_time < 0.3:
    panda.can_send(0x7cc, b'\x80\x24', 0)

panda.set_safety_mode(Panda.SAFETY_SILENT)


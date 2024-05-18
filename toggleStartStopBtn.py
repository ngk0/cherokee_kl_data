# Import the datetime module for time operations
import datetime

# Import Panda class for communication
from panda import Panda
import time

# Instantiate Panda object
panda = Panda()

# Define debounce time for button press
debounce_time = 0.2  # in seconds

# Initialize last pressed time for debounce mechanism
last_pressed_time = time.time()

# Flag to indicate whether the start/stop button is enabled
startStopEnabled = False

# Initialize last time a test message was printed
last_test_message_time = time.time()

try:
    # Continuous loop to monitor button presses and automatically disable engine start-stop if enabled
    while True:       
        # Receive messages from the CAN bus
        can_recv = panda.can_recv()

        # Iterate through received messages
        for address, _, dat, src in can_recv:
            # Check if the message is from source 0
            if src == 0:
                # Check if the message corresponds to automatic engine start/stop enabled state
                if str(hex(address)) == "0x4d0":
                    # Check if the engine start-stop is enabled
                    if f"0x{dat.hex()}" == '0x0000dd0005c00000':
                        startStopEnabled = True
                    # Check if the engine start-stop is enabled
                    elif f"0x{dat.hex()}" == '0x0000dd0003480000':
                        startStopEnabled = False
                        # Optional: print("StartStop State: " + str(f"0x{dat.hex()}"))
                
                # Print statements if button is pressed
                if str(hex(address)) == "0x7cc":
                    if f"0x{dat.hex()}" == '0x8824':
                        # Record the current time
                        current_time = time.time()
                        # Check if debounce time has elapsed since the last press
                        if current_time - last_pressed_time >= debounce_time:
                            if startStopEnabled:
                                print("Automation Engine Start-Stop Button Pressed - Disabling Start/Stop")
                            else:
                                print("Automation Engine Start-Stop Button Pressed - Enabling Start/Stop")
                            # Update last pressed time
                            last_pressed_time = current_time
        
        # Check if 5 seconds have passed since the last test message was printed
        if time.time() - last_test_message_time >= 5:
            # Enable start/stop button if it's currently enabled
            if startStopEnabled:
                panda.set_safety_mode(Panda.SAFETY_ALLOUTPUT)
                time.sleep(0.01)
                start_time = time.time()

                # Send a message to the CAN bus to mimic the button press
                while time.time() - start_time < 0.3:
                    panda.can_send(0x7cc, b'\x80\x24', 0)

                # Disable start/stop button after sending message
                panda.set_safety_mode(Panda.SAFETY_SILENT)
            
            # Update the last test message time
            last_test_message_time = time.time()

# Handle keyboard interrupt to gracefully exit the program
except KeyboardInterrupt:
    print(f"\nNow exiting. ")

# Set Panda to silent safety mode before exiting
panda.set_safety_mode(Panda.SAFETY_SILENT)

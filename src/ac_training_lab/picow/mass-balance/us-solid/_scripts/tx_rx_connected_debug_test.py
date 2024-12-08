# connect the TX and RX pins of the Pico to test the UART communication
import time

from machine import UART, Pin

# Initialize UART interface
uart0 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

# Data to be sent
txData = b"RS232 receive test...\r\n"
print(f"Writing to uart0: {txData}")
uart0.write(txData)
time.sleep(0.1)

timeout = 10  # Timeout in seconds
start_time = time.time()

print("Starting UART communication...")

while True:
    current_time = time.time()
    if current_time - start_time > timeout:
        print("Timeout exceeded. Exiting...")
        break

    # Check for data on uart0
    if uart0.any() > 0:
        print("Data available on uart0")
    while uart0.any() > 0:  # Channel 0 is spontaneous and self-collecting
        rxData0 = uart0.read()
        if rxData0:
            decoded_data = rxData0.decode("utf-8")
            print(f"uart0 received: {decoded_data}")
            uart0.write("{}".format(decoded_data))
            if uart0.any() == 0:
                uart0.write("\r\n")

    time.sleep(0.5)  # Add a small delay to avoid busy-waiting

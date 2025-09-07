# enroll_fingerprints.py
import time
from pyfingerprint.pyfingerprint import PyFingerprint

try:
    # Initialize the sensor (update port and password if needed)
    sensor = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
    
    if not sensor.verifyPassword():
        raise ValueError('The sensor password is wrong!')
except Exception as e:
    print('Failed to initialize sensor:', e)
    exit(1)

print('Sensor initialized successfully!')
print('Place your finger on the sensor...')

# Wait until a finger is read
while not sensor.readImage():
    time.sleep(0.1)

# Convert the read image to characteristics
sensor.convertImage(0x01)

print('Remove your finger...')
time.sleep(2)  # Allow user to remove finger

try:
    # Store the fingerprint template
    position_number = sensor.storeTemplate()
    print(f'Fingerprint stored successfully at position #{position_number}')
    
    # Optional: verify by loading it back
    sensor.loadTemplate(position_number, 0x01)
    print('Fingerprint template verified!')
except Exception as e:
    print('Failed to store fingerprint:', e)

from pybleno import *
import signal
import struct
import random
import time

class TemperatureCharacteristic(Characteristic):
    def _init_(self):
        Characteristic._init_(self, {
            'uuid': '2A6E',
            'properties': ['read', 'notify'],
            'value': None
        })
        self._value = None
        self._updateValueCallback = None

    def onReadRequest(self, offset, callback):
        temperature = 25.0 + random.uniform(0, 10)  # Simulated temperature
        data = struct.pack('f', temperature)
        callback(Characteristic.RESULT_SUCCESS, data)

    def onSubscribe(self, maxValueSize, updateValueCallback):
        self._updateValueCallback = updateValueCallback

    def onUnsubscribe(self):
        self._updateValueCallback = None

    def notify(self):
        if self._updateValueCallback:
            temperature = 25.0 + random.uniform(0, 10)  # Simulated temperature
            data = struct.pack('f', temperature)
            self._updateValueCallback(data)

class HumidityCharacteristic(Characteristic):
    def _init_(self):
        Characteristic._init_(self, {
            'uuid': '2A6F',
            'properties': ['read', 'notify'],
            'value': None
        })
        self._value = None
        self._updateValueCallback = None

    def onReadRequest(self, offset, callback):
        humidity = 50.0 + random.uniform(0, 10)  # Simulated humidity
        data = struct.pack('f', humidity)
        callback(Characteristic.RESULT_SUCCESS, data)

    def onSubscribe(self, maxValueSize, updateValueCallback):
        self._updateValueCallback = updateValueCallback

    def onUnsubscribe(self):
        self._updateValueCallback = None

    def notify(self):
        if self._updateValueCallback:
            humidity = 50.0 + random.uniform(0, 10)  # Simulated humidity
            data = struct.pack('f', humidity)
            self._updateValueCallback(data)

bleno = Bleno()

def onStateChange(state):
    if state == 'poweredOn':
        bleno.startAdvertising('ESP32_Simulation', ['00000002-0000-0000-FDFD-FDFDFDFDFDFD'])
    else:
        bleno.stopAdvertising()

def onAdvertisingStart(error):
    if not error:
        bleno.setServices([
            BlenoPrimaryService({
                'uuid': '00000002-0000-0000-FDFD-FDFDFDFDFDFD',
                'characteristics': [
                    TemperatureCharacteristic(),
                    HumidityCharacteristic()
                ]
            })
        ])

bleno.on('stateChange', onStateChange)
bleno.on('advertisingStart', onAdvertisingStart)

bleno.start()

print('BLE Peripheral Simulation Running...')

def signal_handler(sig, frame):
    print('Stopping...')
    bleno.stopAdvertising()
    bleno.disconnect()
    bleno.stop()
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Notify temperature and humidity updates every second
while True:
    temperatureChar = bleno._services[0]._characteristics[0]
    humidityChar = bleno._services[0]._characteristics[1]
    temperatureChar.notify()
    humidityChar.notify()
    time.sleep(1)

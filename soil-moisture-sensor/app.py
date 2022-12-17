import time
import json
import threading

# packages setting up sensor and actuator simulation 
from counterfit_shims_grove.adc import ADC
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse
from counterfit_connection import CounterFitConnection
from counterfit_shims_grove.grove_relay import GroveRelay
CounterFitConnection.init('127.0.0.1', 5000)

connection_string = "HostName=soil-moisture-sensor-jeggslearns.azure-devices.net;DeviceId=soil-moisture-sensor;SharedAccessKey=Usc7SVLx58I+/4bsoxBREn2Yuh56CFPhjHIYdpHbxeI="

device_client = IoTHubDeviceClient.create_from_connection_string(connection_string)

print('Connecting')
device_client.connect()
print('Connected')

adc = ADC()
relay = GroveRelay(5)

def handle_method_request(request):
    print("Direct method received - ", request.name)

    if request.name == "relay_on":
        relay.on()
    elif request.name == "relay_off":
        relay.off()  

    method_response = MethodResponse.create_from_method_request(request, 200)
    device_client.send_method_response(method_response)  

device_client.on_method_request_received = handle_method_request

while True:
    soil_moisture = adc.read(0)
    print(f"Soil Moisture : ", soil_moisture)
    message = Message(json.dumps({ 'soil_moisture': soil_moisture }))
    device_client.send_message(message)
    time.sleep(2)

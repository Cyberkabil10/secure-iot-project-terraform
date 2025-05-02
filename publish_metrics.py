from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import time
import random

client = AWSIoTMQTTClient("MySecureIoTClient")
client.configureEndpoint("YOUR_ENDPOINT.iot.YOUR_REGION.amazonaws.com", 8883)
client.configureCredentials("root-CA.crt", "private.key", "certificate.pem.crt")

client.connect()

while True:
    message = {
        "metric": "cpu_usage",
        "value": round(random.uniform(10, 90), 2),
        "time": int(time.time() * 1000)
    }
    client.publish("metrics/system/telemetry", json.dumps(message), 1)
    print("Published:", message)
    time.sleep(5)

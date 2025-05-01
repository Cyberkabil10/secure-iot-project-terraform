import time
import json
import psutil
import socket
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder

# 🔧 AWS IoT Endpoint (replace with your actual value)
ENDPOINT = "arlswcawanftf-ats.iot.eu-west-1.amazonaws.com"

# 📁 Certificate file paths (adjust if needed)
CERT = "certs/device.pem.crt"
PRIVATE_KEY = "certs/private.pem.key"
ROOT_CA = "certs/AmazonRootCA1.pem"

# 🆔 MQTT client settings
CLIENT_ID = "my_secure_iot_client"
TOPIC = "metrics/system/telemetry"

# 🌐 Setup MQTT connection
event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)

mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint=ENDPOINT,
    cert_filepath=CERT,
    pri_key_filepath=PRIVATE_KEY,
    client_bootstrap=client_bootstrap,
    ca_filepath=ROOT_CA,
    client_id=CLIENT_ID,
    clean_session=False,
    keep_alive_secs=30,
)

print(f"🔌 Connecting to {ENDPOINT}...")
mqtt_connection.connect().result()
print("✅ Connected to AWS IoT Core!")

# 🔁 Real-time loop
try:
    while True:
        net_io = psutil.net_io_counters()
        payload = {
            "device_id": CLIENT_ID,
            "hostname": socket.gethostname(),
            "cpu_usage": psutil.cpu_percent(interval=1),
            "memory_usage": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "uptime": time.time() - psutil.boot_time(),
            "network_io": {
                "bytes_sent": net_io.bytes_sent,
                "bytes_recv": net_io.bytes_recv
            },
            "timestamp": time.time()
        }

        message_json = json.dumps(payload)
        print(f"📤 Publishing: {message_json}")

        mqtt_connection.publish(
            topic=TOPIC,
            payload=message_json,
            qos=mqtt.QoS.AT_LEAST_ONCE
        )

        time.sleep(5)  # ⏱ Publish every 5 seconds

except KeyboardInterrupt:
    print("🛑 Interrupted by user, disconnecting...")

finally:
    mqtt_connection.disconnect().result()
    print("🚪 Disconnected from AWS IoT Core.")

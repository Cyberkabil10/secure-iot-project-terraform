import time
import json
import socket
import psutil
from awscrt import mqtt
from awsiot import mqtt_connection_builder

# --- AWS IoT Core Connection Details ---
ENDPOINT = "arlswcawanftf-ats.iot.eu-west-3.amazonaws.com"  # ← Replace with terraform output
CLIENT_ID = "my_secure_iot_client"
PATH_TO_CERT = "./certs/device.pem.crt"
PATH_TO_KEY = "./certs/private.pem.key"
PATH_TO_ROOT = "./certs/AmazonRootCA1.pem"
TOPIC = "metrics/system/telemetry"

# --- MQTT Connection ---
mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint=ENDPOINT,
    cert_filepath=PATH_TO_CERT,
    pri_key_filepath=PATH_TO_KEY,
    client_bootstrap=None,
    ca_filepath=PATH_TO_ROOT,
    client_id=CLIENT_ID,
    clean_session=False,
    keep_alive_secs=30
)

print("🔌 Connecting to AWS IoT Core...")
connect_future = mqtt_connection.connect()
connect_future.result()
print("✅ Connected!")

try:
    while True:
        # Gather system metrics
        net_io = psutil.net_io_counters()
        metrics = {
            "cpu_usage": psutil.cpu_percent(interval=1),
            "memory_usage": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "uptime": time.time() - psutil.boot_time(),
            "network_bytes_sent": net_io.bytes_sent,
            "network_bytes_recv": net_io.bytes_recv
        }

        # Publish one message per metric
        for metric_name, value in metrics.items():
            payload = {
                "device_id": CLIENT_ID,
                "hostname": socket.gethostname(),
                "metric": metric_name,
                "value": float(value),
                "timestamp": time.time()
            }

            message_json = json.dumps(payload)
            print(f"📤 Publishing: {message_json}")
            mqtt_connection.publish(
                topic=TOPIC,
                payload=message_json,
                qos=mqtt.QoS.AT_LEAST_ONCE
            )

        time.sleep(5)

except KeyboardInterrupt:
    print("\n⛔ Interrupted by user, disconnecting...")

finally:
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    print("🔌 Disconnected from AWS IoT Core.")

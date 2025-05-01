import json
import boto3
import time

timestream = boto3.client('timestream-write')

DATABASE_NAME = 'secure_iot_db'
TABLE_NAME = 'system_metrics'

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))

    try:
        dimensions = [
            {'Name': 'device_id', 'Value': event.get('device_id', 'unknown')},
            {'Name': 'hostname', 'Value': event.get('hostname', 'unknown')}
        ]

        records = [
            {
                'Dimensions': dimensions,
                'MeasureName': 'cpu_usage',
                'MeasureValue': str(event.get('cpu_usage', 0)),
                'MeasureValueType': 'DOUBLE',
                'Time': str(int(event.get('timestamp', time.time()) * 1000)),
                'TimeUnit': 'MILLISECONDS'
            },
            {
                'Dimensions': dimensions,
                'MeasureName': 'memory_usage',
                'MeasureValue': str(event.get('memory_usage', 0)),
                'MeasureValueType': 'DOUBLE',
                'Time': str(int(event.get('timestamp', time.time()) * 1000)),
                'TimeUnit': 'MILLISECONDS'
            },
            {
                'Dimensions': dimensions,
                'MeasureName': 'disk_usage',
                'MeasureValue': str(event.get('disk_usage', 0)),
                'MeasureValueType': 'DOUBLE',
                'Time': str(int(event.get('timestamp', time.time()) * 1000)),
                'TimeUnit': 'MILLISECONDS'
            }
        ]

        response = timestream.write_records(
            DatabaseName=DATABASE_NAME,
            TableName=TABLE_NAME,
            Records=records
        )

        print("Write successful:", response)
        return {
            'statusCode': 200,
            'body': json.dumps('Data written to Timestream')
        }

    except Exception as e:
        print("Error writing to Timestream:", str(e))
        raise

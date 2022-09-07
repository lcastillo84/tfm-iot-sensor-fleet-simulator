import json
from utils import get_timestamp
import random


def build_message(sensor_id: str, sensor_type: str, device_info: dict,
                  sequence: int, data: dict) -> dict:
    """
    Genera un diccionario con la estructura de un mensaje tipo JSON que se
    publicará en un tópico MQTT.
    """
    payload = {}
    if sensor_type == 'temperature':
        payload = {
            "BatV": 3.6,
            "TempC1": data[sensor_id][sequence],
            "ADC_CH0V": 0.29,
            "Digital_IStatus": "L",
            "EXTI_Trigger": "FALSE",
            "Door_status": "OPEN",
            "Work_mode": "IIC",
            "TempC_SHT": -0.1,
            "Hum_SHT": 6553.5
        }
    elif sensor_type == 'vibration':
        payload = {
            "acceX": data[sensor_id][sequence],
            "acceY": data[sensor_id][sequence] + random.randint(-100, 100),
            "acceZ": data[sensor_id][sequence] + random.randint(-100, 100),
            "angle": 0,
            "vol": 3.6,
        }
    return {
        "WirelessDeviceId": sensor_id,
        "DecodedPayloadData": {
            "statusCode": 200,
            **payload
        },
        "DeviceInfo": device_info,
        "ArrivalTimestamp": get_timestamp()}


def build_messages_list(
        devices: dict,
        sequence: int,
        data_filename: str) -> list:
    "Genera una lista de mensajes para ser publicados en un tópico MQTT"

    with open(data_filename) as f:
        sensor_data = json.load(f)

    messages = []
    for device_id, device_info in devices.items():
        sensor_type = device_info['sensorType']
        message = build_message(
            sensor_id=device_id,
            device_info=device_info,
            sequence=sequence,
            sensor_type=sensor_type,
            data=sensor_data[sensor_type]
        )
        messages.append(message)

    return messages

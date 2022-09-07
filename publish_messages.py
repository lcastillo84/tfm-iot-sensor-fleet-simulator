import json
import boto3
import asyncio
from message_builder import build_messages_list
from utils import get_timestamp, read_sequence, update_sequence

SEQUENCE_FILENAME = 'sequence.txt'
MAX_SEQUENCE_NBR = 572
SENSORDATA_FILENAME = 'data/sensorData.json'
DEVICEINFO_FILENAME = 'data/deviceInfo.json'


async def send_message(message: dict, topic: str, sensor_id: str,
                       iot_client) -> None:
    """
    Función asíncrona que publica un mensaje en el tópico MQTT
    especificado
    """
    ts = get_timestamp()
    print(f'{ts} | Publicando en tópico {topic}, sensor {sensor_id}')
    try:
        iot_client.publish(topic=topic, payload=json.dumps(message))
    except Exception as e:
        ts = get_timestamp()
        print(f'{ts} | Falló envío en tópico {topic}, sensor {sensor_id}\n '
              f'Error: {str(e)}')
        return


def build_parallel_function_call_list(messages, iot_client):
    """
    Genera una lista que contiene los llamados a la función send_message. Esta
    lista luego se debe pasar a asyncio.gather para que se hagan los llamados
    en paralelo a estas funciones.
    """
    publish_funcs = []
    for message in messages:
        sensor_type = message['DeviceInfo']['sensorType']
        sensor_id = message['WirelessDeviceId']
        topic = ''
        if sensor_type == 'vibration':
            topic = f'sensordata/vibration/sl500/{sensor_id}'
        elif sensor_type == 'temperature':
            topic = f'sensordata/temperature/lsn50v2/{sensor_id}'
        publish_funcs.append(send_message(
            message=message,
            topic=topic,
            sensor_id=sensor_id,
            iot_client=iot_client
        ))
    return publish_funcs


async def publish():
    "Publica un mensaje MQTT para cada dispositivo"
    # Leer "base de datos" de información de sensores
    with open(DEVICEINFO_FILENAME) as f:
        sensors = json.load(f)

    # Leer número de secuencia. Esto se utiliza para asignar valores de
    # las medidas de temperatura y vibración para cada sensor
    sequence = read_sequence(SEQUENCE_FILENAME)

    # Construimos una lista de mensajes
    messages = build_messages_list(
        sensors,
        sequence=sequence,
        data_filename=SENSORDATA_FILENAME)

    update_sequence(SEQUENCE_FILENAME, sequence, MAX_SEQUENCE_NBR)

    # Inicializamos cliente boto3
    iot_client = boto3.client('iot-data')

    # Construimos una lista que contiene llamadas a la función para
    # publicar los mensajes.
    publish_funcs = build_parallel_function_call_list(messages, iot_client)

    # Usamos la función gather de asyncio para hacer los llamados a las
    # funciones para publicar los datos en paralelo.
    await asyncio.gather(*publish_funcs)


if __name__ == '__main__':
    asyncio.run(publish())

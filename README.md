# Simulador de flota de sensores de vibración y temperatura publicando en tópicos MQTT
### Autor: Luis Castillo

Script utilizado en TFM "Diseño e implementación de arquitectura de analítica de datos en la nube para aplicación IIoT". Master en Business Analytics y Big Data de IMF Smart Education / Universidad Nebrija.

El script `publish_messages` publica mensajes que simulan el payload de sensores de vibración (aceleración) y temperatura en los siguientes tópicos MQTT:  
`sensordata/temperature/lsn50v2/<id del sensor>`  
`sensordata/vibration/sl500/<id del sensor>`

#### Requerimientos:
* Cuenta AWS.
* Credenciales para acceso programático.
* Instalar y configurar [aws-cli](https://aws.amazon.com/cli/).

#### Para ejecutar el script una vez:
`python publish_messages.py`

#### Para programar ejecución periódica usando crontab:  
1. Primero crear script .sh como el que sigue:
```
#!/bin/bash
echo "Iniciando script shell..."
/home/luis/tfm/tfm-iot-sensor-fleet-simulator/.venv/bin/python /home/luis/tfm/tfm-iot-sensor-fleet-simulator/publish_messages.py
```

2. Hacer el script ejecutable:
`chmod +x mqtt-publisher.sh`

3. Si queremos publicar el mensaje cada 5 minutos, por ejemplo, se añade la siguiente línea a crontab (`crontab -e`).  
`*/5 * * * * /home/luis/tfm/mqtt-publisher.sh >> /home/luis/tfm/mqtt-publisher.logs`


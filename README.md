# CAR-Forwarders
Forward MQTT messages to Websockets server and visa-versa

# Smart Trolley Devices
There is a Version 1 smart trolley device, as part of the Call-A-Robot project, that sends and receives data via websockets. V2 device sends and receives using MQTT. To make both devices work V2 messages are forwarded to websockets. In the future *presumably* all devices will use MQTT.

## Two Daemons
*MtoW.py* Listens on all topics listed in Config.py sent to the MQTT host. It then adds a dictionary message field of 'Forwarded-by: MtoW.py" and sends this message to the Websocket host named within Config.py. Some topic messages are re-formatted.

*WtoM.py* Listens to Websocket host named in Config.py for order-update messages and then sends to MQTT host. *Not completed*

## RUN
1. python MtoW.py
2. python WtoM.py

Both run as daemons

## Future
1. Which messages have been forwarded will be stored and saved to a locked file so multiple daemons can be run concurrently without resending a message twice

## Libraries / Package requirements
- import websocket
- import rel
- import paho.mqtt.client as mqtt
- from websocket import create_connection
- import json

## Config.py
Not saved within repo as it has password

MQTT_USER = '*****'
MQTT_PASSWORD = '**********'
MQTT_HOST = 'MQTT server host'
MQTT_PORT = 8097

**Topics as a list**
MQTT_TOPICS = ['trolley/gps', 'trolley/battery', 'trolley/method', 'trolley/registration', 'trolley/status']

WS_HOST = 'wss://host name'
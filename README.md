# CAR-Forwarders
Forward MQTT messages to Websockets server and visa-versa

## Two Daemons
*MtoW.py* Listens on all topics listed in Config.py sent to the MQTT host. It then adds a dictionary message field of 'Forwarded-by: MtoW.py" and sends this message to the Websocket host named within Config.py. Some topic messages are re-formatted.

*WtoM.py* Listens to Websocket host named in Config.py for order-update messages and then sends to MQTT host. *Not completed*

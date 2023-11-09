#####################################################################
# Author:       Andy Perrett (18684092@students.lincoln.ac.uk)      #
# Version:      1                                                   #
# Date:         19/05/2022                                          #
# Description:  Websockets forwarder to MQTT as part of Call-A-Robot#
#               and Smart Trolley Device project. This module is    #
#               for use by WtoM.py                                  #
# Module:       WSForward.py                                        #
#####################################################################

# Standard imports
from socket import socket
import websocket
import rel
import paho.mqtt.client as mqtt
import json
import time

# My imports
from Config import *

###############
# WSforwarded #
###############



class WSforwarder:

    ############
    # __init__ #
    ############
    def __init__(self, host=WS_HOST):
        self.ws = None
        self.host = host
        self.state_switch = {
            'car_INIT': 'INIT',
            'car_CALLED': 'CALLED',
            'car_ACCEPT': 'ACCEPT',
            'car_ARRIVED': 'ARRIVED',
            'car_LOADED': 'LOADED',
            'car_CANCEL': 'INIT'
        }

        websocket.enableTrace(False)
    
    #################
    # on_ws_message #
    #################
    def on_ws_message(self, ws, message):
        #print (message)
        message = json.loads(message)

        if 'method' in message.keys() and message['method'] == 'update_orders':
            print('=> processing WS message : %s' % message)
            MQTTclient = mqtt.Client("MQTT_to_Websockets_Translator")
            MQTTclient.username_pw_set(MQTT_USER, MQTT_PASSWORD)
            MQTTclient.connect(MQTT_HOST, MQTT_PORT)
            
            for item in message['states']:
                message['states'][item] = self.state_switch.get(message['states'][item], message['states'][item])
            
            message['epoch'] = int(time.time())
            message['Forward-By'] = "WtoM.py"
        
            message = json.dumps(message)
            ret= MQTTclient.publish(MQTT_LISTEN_TOPIC, message, retain=False, qos=0)
            print('<= published on MQTT topic "%s": %s' % (MQTT_LISTEN_TOPIC, message))
            MQTTclient.disconnect()


    ###############
    # on_ws_error #
    ###############
    def on_ws_error(self, ws, error):
        print("### error ###", error)
        if isinstance(error, KeyboardInterrupt) or isinstance(error, SystemExit):
            self.ws.close()

    ###############
    # on_ws_close #
    ###############
    def on_ws_close(self, ws, close_status_code, close_msg):
        print("### closed ###", close_status_code, close_msg)

    ##############
    # on_ws_open #
    ##############
    def on_ws_open(self, ws):
        print("Opened connection")

    ###############
    # run_forever #
    ###############
    # NOTE these defaults and ping_interval / timeout solved
    # an exception issue whereby the connection simply
    # broke
    def run_forever(self, sockopt=None, sslopt=None,
                    ping_interval=0, ping_timeout=None,
                    http_proxy_host=None, http_proxy_port=None,
                    http_no_proxy=None, http_proxy_auth=None,
                    skip_utf8_validation=False,
                    host=None, origin=None):
        self.ws.run_forever(ping_interval=70, ping_timeout=10)
        #self.ws.run_forever(dispatcher=rel, ping_interval=70, ping_timeout=10)
        #rel.signal(2, rel.abort)  # Keyboard Interrupt
        #rel.dispatch()

    #######
    # run #
    #######
    def run(self):
        print("attempt connection to %s" % self.host)
        self.ws = websocket.WebSocketApp(self.host,
                                on_open=self.on_ws_open,
                                on_message=self.on_ws_message,
                                on_error=self.on_ws_error,
                                on_close=self.on_ws_close)
        while True:
            try:
                time.sleep(0.1)
                teardown = self.run_forever()
            
            except KeyboardInterrupt:
                print ('KeyboardInterrupt')
                self.ws.close()
                break
            
            except websocket._exceptions.WebSocketException as e:
                self.ws.sock = None
                pass
            
            finally:
                if teardown and not teardown:
                    print (teardown, 'KeyboardInterrupt')
                    self.ws.close()
                    break

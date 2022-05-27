#####################################################################
# Author:       Andy Perrett (18684092@students.lincoln.ac.uk)      #
# Version:      1                                                   #
# Date:         19/05/2022                                          #
# Description:  MQTT forwarder to Websocket as part of Call-A-Robot #
#               and Smart Trolley Device project. This module is    #
#               for use by MtoW.py and is run in a thread           #
# Module:       MQTTForward.py                                      #
#####################################################################


# This originated as boilerplate code, then modified

# Standard Imports
import paho.mqtt.client as mqtt
from websocket import create_connection
import json

# My Imports
from Config import *

#################
# MQTTforwarder #
#################
class MQTTforwarder:

    # Defaults within Config.py
    def __init__(self, host = MQTT_HOST, port = MQTT_PORT, user = MQTT_USER, password = MQTT_PASSWORD, topicList = MQTT_TOPICS, wsHost = WS_HOST):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.topicList = topicList
        self.wsHost = wsHost
 
    ###################
    # on_mqtt_connect #
    ###################
    def on_mqtt_connect(self, client, userdata, flags, rc): 
        print("MQTT connected with result code {0}".format(str(rc)))  

        # Multiple topics
        for p in self.topicList:
            client.subscribe(p)  

    ###################
    # on_mqtt_message #
    ###################
    def on_mqtt_message(self, client, userdata, msg):  
        #t1 = Process(target=self.send, args=(msg.payload, msg.topic))
        #t1.start()
        self.send(msg.payload, msg.topic)  

    #######
    # run #
    #######
    def run(self):

        # Create instance
        self.MQTTclient = mqtt.Client("MQTT_to_Websockets_Translator") 
        self.MQTTclient.username_pw_set(self.user, self.password)

        # Set callbacks 
        self.MQTTclient.on_connect = self.on_mqtt_connect  
        self.MQTTclient.on_message = self.on_mqtt_message  
        
        # See config for connection details
        self.MQTTclient.connect(self.host, self.port)
        
        # Daemon
        self.MQTTclient.loop_forever()

    #########
    # WSend #
    #########
    def WSend(self, msg):
        msg['Forwared-By'] = "MtoW.py"
        ws = create_connection(self.wsHost)
        ws.send(msg)
        print("Sending...", msg)
        ws.close()

    ########
    # send #
    ########
    def send(self, msg, topic):

        # MQTT messages from all topics arrive here
        try:
            mDict = json.loads(msg.decode("utf-8") )
            tStr = str(topic)
            #print("Received", mDict, topic)

            # The extra field isn't recognised by WS server
            if tStr == "trolley/method" or tStr == "trolley/registration":
                self.WSend(json.dumps(mDict))
            
            # reformat message (MQTT has a lot more info in and WS server only
            # wants some of it)    
            elif tStr == "trolley/gps":
                gps = {}
                gps['latitude'] = mDict['LATITUDE']
                gps['method'] = "location_update"
                gps['longitude'] = mDict['LONGITUDE']

                # NOTE not sure about _id
                gps['_id'] = mDict['CLIENT_ID']

                # TODO This field needs changing with the device itself
                # it will be STD-v2-*UNIQUE MAC* (Smart Trolley Device Version 2)
                gps['user'] = "ESP32_CAR_USER_Andy"

                gps['accuracy'] = mDict['PDOP']

                # NOTE The row isn't sent by STDv2 - it also won't be known by the device?
                gps['row'] = ""
                gps['rcv_time'] = mDict['UTC_DATE_TIME']

                # Call-A-Robot prefers -1 for no GPS
                # NOTE will be set within STD in near future
                if gps['latitude'] == "" or gps['longitude'] == "":
                    gps['latitude'] = "-1"
                    gps['longitude'] = "-1"
                self.WSend(json.dumps(gps))
            
            # Battery info - WS ignores this at present
            elif tStr == "trolley/battery":
                bat = {}
                states = {}
                states['voltage'] = mDict['Voltage']
                states['status'] = mDict['Status']
                bat['information'] = states
                bat['_id'] = mDict['CLIENT_ID']
                bat['method'] = "battery"
                bat['user'] = "ESP32_CAR_USER_Andy"
                self.WSend(json.dumps(bat))
        
        # Garbage may appear within MQTT message (like byte coded 
        # message that can't be converted to UTF-8)
        except Exception as e:
            print("Exception:", e)




        
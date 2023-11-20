######################################################################
# Author:       Andy Perrett (18684092@students.lincoln.ac.uk)      #
# Version:      1                                                   #
# Date:         19/05/2022                                          #
# Description:  MQTT forwarder to Websocket as part of Call-A-Robot #
#               and Smart Trolley Device project. This module is    #
#               for use by MtoW.py                                  #
# Module:       MQTTForward.py                                      #
#####################################################################


# This originated as boilerplate code, then modified

# Standard Imports
import paho.mqtt.client as mqtt
from websocket import create_connection
import json
from calendar import timegm
import time
from pprint import pformat


#################
# MQTTforwarder #
#################
class MQTTforwarder:

    # Defaults within Config.py
    def __init__(self, host, port, user, password, topicList, wsHost):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.topicList = topicList
        self.wsHost = wsHost
        self.ws = create_connection(self.wsHost)

    ###################
    # on_mqtt_connect #
    ###################
    def on_mqtt_connect(self, client, userdata, flags, rc):
        print("MQTT connected with result code {0}".format(str(rc)))

        # Multiple topics
        for p in self.topicList:
            print('subscribing to %s' % p)
            client.subscribe(p)

    ###################
    # on_mqtt_message #
    ###################
    def on_mqtt_message(self, client, userdata, msg):
        #t1 = Process(target=self.send, args=(msg.payload, msg.topic))
        #t1.start()
        #file = open ("mqtt.txt", "a")
        #file.write(str(msg.topic) +","+str(msg.payload) + "\n")
        #file.close()
        self.send(msg.payload, msg.topic)

    #######
    # run #
    #######
    def run(self):

        # Create instance
        self.MQTTclient = mqtt.Client(clean_session=True)
        self.MQTTclient.username_pw_set(self.user, self.password)

        # Set callbacks
        self.MQTTclient.on_connect = self.on_mqtt_connect
        self.MQTTclient.on_message = self.on_mqtt_message
        self.MQTTclient.on_disconnect = self.on_mqtt_disconnect

        # See config for connection details
        self.MQTTclient.connect(self.host, self.port)

        # Daemon
        self.MQTTclient.loop_forever()

    def on_mqtt_disconnect(self, client, userdata, rc):
        print('mqtt disconnected %s' % userdata)
        self.run()

    #########
    # WSend #
    #########
    def WSend(self, msg):
        try:
            print("Sending to websocket...", msg)
            self.ws.send(msg)
        except Exception as e:
            print("couldn't send, trying to reconnect: %s" % e)
            self.ws = create_connection(self.wsHost)
            if self.ws:
                self.ws.send(msg)



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
            if tStr == "trolley/method" or tStr == "trolley/register":
                mDict['Forward-By'] = "MtoW.py"
                if 'method' in mDict:
                    if mDict['method'] == 'call':
                        mDict['method'] = 'car_call'
                    elif mDict['method'] == 'cancel':
                        mDict['method'] = 'car_cancel_task'
                    elif (mDict['method'] == 'set_state') and (mDict['state'] == 'LOADED'):
                        mDict['method'] = 'car_load'
                print('message: %s' % pformat(mDict))
                self.WSend(json.dumps(mDict))

            # reformat message (MQTT has a lot more info in and WS server only
            # wants some of it)
            elif tStr == "trolley/gps":
                gps = {}
                try:
                    gps['latitude'] = float(mDict['LATITUDE'])
                    gps['longitude'] = float(mDict['LONGITUDE'])
                except:
                    gps['latitude'] = ""
                    gps['longitude'] = ""
                gps['method'] = "location_update"

                # NOTE not sure about _id
                gps['user'] = "STD_v2_"+ mDict['CLIENT_ID']

                # Accuracy is a float
                try:
                    gps['accuracy'] = float(mDict['PDOP'])
                    gps['HDOP'] = float(mDict['HDOP'])
                    gps['VDOP'] = float(mDict['VDOP'])
                    gps['C/N0_MAX'] = float(mDict['C/N0_MAX'])
                except:
                    gps['accuracy'] = -1
                    gps['HDOP'] = -1
                    gps['VDOP'] = -1
                    gps['C/N0_MAX'] = -1

                gps['row'] = ""
                # NOTE The row isn't sent by STDv2 - it also won't be known by the device?
                utc_time = time.strptime(mDict['UTC_DATE_TIME'], "%Y%m%d%H%M%S.%f")
                gps['rcv_time'] = timegm(utc_time)


                # Call-A-Robot prefers -1 for no GPS
                # NOTE will be set within STD in near future
                if gps['latitude'] == "" and gps['longitude'] == "":
                    gps['latitude'] = -1
                    gps['longitude'] = -1

                gps['Forward-By'] = "MtoW.py"
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
                bat['Forward-By'] = "MtoW.py"
                self.WSend(json.dumps(bat))

        # Garbage may appear within MQTT message (like byte coded
        # message that can't be converted to UTF-8)
        except Exception as e:
            print("Exception:", e)

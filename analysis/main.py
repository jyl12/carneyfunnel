import paho.mqtt.client as mqtt
import time

class Communication (object):
    def __init__(self, message = None):
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect('127.0.0.1', 1883, 60)
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.on_disconnect = self.on_disconnect
        self.mqtt_client.loop_start()
        print('init')
        self.run()
    
    def on_connect (self, client, userdata, flags, rc):
        if rc == 0:
            print ('Connected to broker.')
        else:
            print ('Connection failed.')
        self.mqtt_client.subscribe("main/analysis")
        
    def on_disconnect(self, client, userdata, flags, rc):
        self.mqtt_client.reconnect()
        
    def on_message(self, client, userdata, message):
        print('on message')
        print('received:',str(message.payload.decode('utf-8')))
        message_payload = str(message.payload.decode('utf-8'))
        if message.topic == 'main/analysis':
            print('from main message')
            #call class service analysis and publish back the result.
    def run(self):
        self.mqtt_client.publish('main/analysis','fes')
        print('run')
        time.sleep(4)
            
class ServiceAnalysis(object):
    def func():
        print ('this is analysis')
        
    def flowrate(duration, weight_powder):
#         print('flowrate')
        flowrate = duration / weight_powder
        return flowrate

    def apparent_density(weight_scrapecup, weight_powder):
#         print('apparent density')
        apparent_density = weight_scrapecup / weight_powder
        return apparent_density
def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
   
if __name__ == "__main__":
    print('analysis main')
    ##direct call
#     client = mqtt.Client() #create new instance
#     client.on_message=on_message #attach function to callback
#     print("connecting to broker")
#     client.connect('127.0.0.1') #connect to broker
#     client.loop_start() #start the loop
#     print("Subscribing to topic","house/bulbs/bulb1")
#     client.subscribe("house/bulbs/bulb1")
#     print("Publishing message to topic","house/bulbs/bulb1")
#     client.publish("house/bulbs/bulb1","OFF")
#     time.sleep(4) # wait
#     client.loop_stop() #stop the loop
## class
#     Communication()




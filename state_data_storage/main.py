#!/usr/bin/env python3

from opcua import Server, ua, uamethod
# from opcua.common.ua_utils import value_to_datavalue
# from opcua.ua.attribute_ids import AttributeIds
# from opcua.ua.uatypes import ValueRank
import time
from random import randint
import datetime
import csv
import socket

class ExtendedServer(Server):
    def __init__(self,port):
        super().__init__()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8",80))
        ip = s.getsockname()[0]
        s.close()
        self.url = "opc.tcp://" + str(ip) + ":" + str(port)
        self.set_endpoint(self.url)
        name = "opcua_simulation_server"
        self.addspace = self.register_namespace(name)
#         print("namespace is:", self.addspace)

def opcuaserver_settings(objectname = "Parameters" , variablename = "Variable"):
    global Temp
    node = server.get_objects_node()
#     print("node is:", node)
    param = node.add_object(server.addspace, objectname)
#     print("param is:",param)
    Temp = param.add_variable (server.addspace, variablename, 0)
    server.start()
    print("Server is started at {}".format(server.url))

class Communication:  #try to wrap
    def __init__(self, port=None):
        self.server = ExtendedServer(port)
    
    def opcuaserver_pub(self,objectname = "Parameters" , variablename = "Variable"):
        global Temp1
        node = self.server.get_objects_node()
#         print("node is:", node)
        param = node.add_object(self.server.addspace, objectname)
#         print("param is:",param)
        Temp1 = param.add_variable (self.server.addspace, variablename, 0)
        self.server.start()
        print("Server is started at {}".format(self.server.url))

def start():
    global Temp1, Temp2, Temp3, Temp4, Temp5, Temp6, Temp7, myevgen, mysecondevgen 
    server = ExtendedServer(4840)
    node = server.get_objects_node()
#     print("node is:", node)
    param = node.add_object(server.addspace, "Parameters")
#     print("param is:",param)
###
    # Creating a custom event: Approach 1
    # The custom event object automatically will have members from its parent (BaseEventType)
    etype = server.create_custom_event_type(server.addspace, 'MyFirstEvent', ua.ObjectIds.BaseEventType, [('MyNumericProperty', ua.VariantType.Float), ('MyStringProperty', ua.VariantType.String)])

    myevgen = server.get_event_generator(etype, param)

    # Creating a custom event: Approach 2
    custom_etype = server.nodes.base_event_type.add_object_type(2, 'MySecondEvent')
    custom_etype.add_property(server.addspace, 'MyIntProperty', ua.Variant(0, ua.VariantType.Int32))
    custom_etype.add_property(server.addspace, 'MyBoolProperty', ua.Variant(True, ua.VariantType.Boolean))

    mysecondevgen = server.get_event_generator(custom_etype, param)
    ###
    Temp1 = param.add_variable (server.addspace, "Time stamp (s)", 0)
    Temp2 = param.add_variable (server.addspace, "Batch code", 0)
    Temp3 = param.add_variable (server.addspace, "Elapsed time (s)", 0)
    Temp4 = param.add_variable (server.addspace, "Powder mass (g)", 0)
    Temp5 = param.add_variable (server.addspace, "Scraped powder mass (g)", 0)
    Temp6 = param.add_variable (server.addspace, "Flowrate (g/s)", 0)
    Temp7 = param.add_variable (server.addspace, "Apparent density (g/cm3)", 0)
    server.start()
    print("Server is started at {}".format(server.url))
    
def write_csv(filename = None, **kwargs):
    if filename == None:
        print("File name not found.")
    else:
        time_stamp = datetime.datetime.now()
        with open(filename + ".csv" , 'a',newline='') as file:
            fields = [time_stamp, kwargs]
            writer = csv.writer(file)
            writer.writerow(fields)
        return 0
            
if __name__ == "__main__":
    print('state and data storage main')
    #try event
    start()
    count = 0
    while True:
        time.sleep(5)
        myevgen.event.Message = ua.LocalizedText("MyFirstEvent %d" % count)
        myevgen.event.Severity = count
        myevgen.event.MyNumericProperty = count
        myevgen.event.MyStringProperty = "Property " + str(count)
        myevgen.trigger()
        mysecondevgen.trigger(message="MySecondEvent %d" % count)
        count += 1
    #***** try wrapper***
#     opc = Communication(port = 4840)
#     opc.opcuaserver_pub("test_para","test_var")

    #***** without wrapper***
    # server = ExtendedServer(4840)
    # opcuaserver_settings("test_para","test_var")

    # node = server.get_objects_node()
    # print("node is:", node)
    # param = node.add_object(server.addspace, "Parameters")
    # print("param is:",param)
    # Temp = param.add_variable (server.addspace, "Temperature", 0)
    # server.start()
    # print("Server is started at {}".format(server.url))

#     while True:  
#         Temperature = randint(10, 50)
#         print("Temperature:",Temperature)
#         Temp1.set_value(Temperature)
#         time.sleep(2)


import paho.mqtt.client as mqtt 
import asyncio 
import websockets 
import time 
import requests
from configuration import config 
import json 
 
#---------------------> mqtt client code 
def on_connect(client, userdata, flags, rc):     
    print("mqtt connected successfully: {}".format( 
            mqtt.connack_string(rc))) 
    client.subscribe("#") 
 
def on_message(client, userdata, msg): 
    global message    
    message = msg.payload 
    dat=json.loads(message) 
    global imei 
    imei=(dat['data']['imei']) 
    # print(imei) 
 
    # print(message) 
 
client = mqtt.Client()   
client.username_pw_set('pds',password='Pds@orahi123') 
 
client.on_connect = on_connect     
client.on_message = on_message    
 
client.connect("mqtt.orahi.com",1883,60)     
client.loop_start() 
 
#---------------------------> websocket code starts here 
webclients = set() 

id_and_socket={} 
 
async def web_socket(websocket, path): 
    
    print("client connected " + str(len(webclients)+1)) 
    webclients.add(websocket) 

    id = await websocket.recv() 

    imei_list=[] 
    

    parameter={"id":id}
    response=requests.get("https://apx.orahi.com/mob/device/getDevices/",params=parameter)
    details = response.json()

    for i in details["data"]["devices"]:
        imei_list.append(i["url"])
    print(imei_list)
    id_and_socket[id]=websocket 
    # print(imei_list) 
    # print(id_and_socket)
    # print(webclients) 
    while True: 
        for i in imei_list: 
            # print(i==imei) 
            if i==imei: 
                try:
                    await asyncio.wait([id_and_socket[id].send(message) for ws in webclients]) 
                    time.sleep(0.2) 
                except websockets.exceptions.ConnectionClosedError:
                    print("client disconnected")
         
start_server = websockets.serve(web_socket, config['host'], config['port']) 
asyncio.get_event_loop().run_until_complete(start_server) 
asyncio.get_event_loop().run_forever() 
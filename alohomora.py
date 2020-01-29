import os
import paho.mqtt.client as mqtt
import requests

DEVICE_IP = os.getenv('DEVICE_IP')
LOGIN = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')
MQTTSERVER = os.getenv('MQTTSERVER')
MQTTUSER = os.getenv('MQTTUSER')
MQTTPASS = os.getenv('MQTTPASS')
MQTTTOPIC = os.getenv('MQTTTOPIC')

login_payload = {
    'login': LOGIN,
    'password': PASSWORD,
}
sec_box_payload = {
    'actions': [{
        'action': 'sec_box',
        'parameters': 'id=65793,reason=3',
    }]
}

def on_connect(client, userdata, flags, rc):
    client.subscribe("+")

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_message(client, userdata, msg):
    if msg.topic == MQTTTOPIC and msg.payload.decode('utf-8') == 'True':
        login_url = f'http://{DEVICE_IP}/login.fcgi'
        response = requests.post(login_url, json=login_payload)
        session = response.json()['session']
        actions_url = f'http://{DEVICE_IP}/execute_actions.fcgi?session={session}'
        response = requests.post(actions_url, json=sec_box_payload)

mqttclient = mqtt.Client(client_id='Alohomora-Client')
mqttclient.on_connect = on_connect
mqttclient.on_message = on_message
mqttclient.username_pw_set(MQTTUSER, password=MQTTPASS)
mqttclient.connect(MQTTSERVER)
mqttclient.subscribe('controlid/open')
mqttclient.loop_forever()


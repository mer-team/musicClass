from joblib import dump, load
import requests
import json
import pika
import os

mquser = os.environ.get('USER')
mqpass = os.environ.get('PASS')
mqport = os.environ.get('PORT')
mqhost = os.environ.get('HOST')
apiurl = os.environ.get('API_URL')

credentials =  pika.PlainCredentials(mquser, mqpass)
connection = pika.BlockingConnection(pika.ConnectionParameters(mqhost, mqport,'/',credentials))

channel = connection.channel()
channel.queue_declare(queue='classifyMusic')
channel.queue_declare(queue='musicFeatures')
clf = load('trainedModel.joblib')
scaler = load('scaler.joblib')
print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    ch.basic_ack(delivery_tag = method.delivery_tag)
    print(" [x] Received %r" % body)# See all feature names in the pool in a sorted order
    b = json.loads(body.decode('utf-8'))
    name = b[0].split(".")[0]
    toTest = [b[1],b[2],b[3]]
    ft = scaler.transform([toTest])
    p = clf.predict(ft)
    print("Predict = ", p)
    emotion = ""
    if p == "1":
        emotion = "Feliz"
    if p == "2":
        emotion = "Tensa"    
    if p == "3":
        emotion = "Triste"   
    if p == "4":
        emotion = "Calma"

    PARAMS = {'idVideo': name, 'emocao': emotion}
    HEADERS = { 'Accept': 'application/json', 'Content-Type': 'application/json' }

    requests.post("http://"+apiurl+"/music/update", headers=HEADERS, json=PARAMS )
    print(' [*] Waiting for messages. To exit press CTRL+C')


channel.basic_consume(queue='classifyMusic',
                      auto_ack=False,
                      on_message_callback=callback)

channel.start_consuming()
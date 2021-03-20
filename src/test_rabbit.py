import pika
import os

mqhost = os.environ.get("MQHOST")
mquser = os.environ.get("MQUSER")
mqpass = os.environ.get("MQPASS")
mqport = os.environ.get("MQPORT")

credentials =  pika.PlainCredentials(mquser, mqpass)
connection = pika.BlockingConnection(pika.ConnectionParameters(mqhost, mqport, '/', credentials))

message = '["JiF3pbvR5G0.wav", 0.4483470916748047, 0.9279613494873047, 115.56307220458984]'
queue_send = 'classifyMusic'

def test_rabbitmq():
    """Check rabbitmq connection"""
    channel = connection.channel()

    assert connection.is_open == True and channel.is_open == True
    connection.close()

def test_send_message():
    """Send rabbitmq extractor result to classify"""
    connection = pika.BlockingConnection(pika.ConnectionParameters(mqhost, mqport, '/', credentials))
    channel = connection.channel()
    channel.queue_declare(queue=queue_send)
    channel.basic_publish(exchange='', routing_key=queue_send, body=message)
    print(" [x] Sent message to classify.")
    connection.close()

    assert connection.is_closed == True and channel.is_closed == True 
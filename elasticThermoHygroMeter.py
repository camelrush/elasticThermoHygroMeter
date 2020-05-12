import RPi.GPIO as GPIO
from devices import dht11
import datetime
import time
from elasticsearch import Elasticsearch

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

es = Elasticsearch('192.168.3.11:9200')
instance = dht11.DHT11(pin=14)

while True:
    sensorData = instance.read()
    timestamp = datetime.datetime.now()
    if sensorData.is_valid():
        es_body = {
            '@timestamp' : timestamp.isoformat(),
            'temperture' : sensorData.temperature,
            'humidity' : sensorData.humidity,
        }
    response = es.index(index='raspi_accel_meter',doc_type='doc',body=es_body)
    time.sleep(5)
    print(es_body)

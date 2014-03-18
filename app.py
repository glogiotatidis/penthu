#!/usr/bin/env python

import os
import json
import pika
from flask import Flask, request


RABBITMQ_QUEUE = 'penthu'

app = Flask(__name__)
if 'RABBITMQ_URL' in os.environ:
    parameters = pika.URLParameters(os.environ['RABBITMQ_URL'])
    connection = pika.BlockingConnection(parameters)
else:
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()
channel.queue_declare(queue=RABBITMQ_QUEUE)


@app.route('/', methods=['POST', 'GET'])
def root():
    if request.method == 'GET':
        return 'Not much here'.

    data = json.loads(request.form['payload'])
    repository = data['repository']['full_name']
    pr_number = data['pull_request']['number']

    channel.basic_publish(
        exchange='',
        routing_key=RABBITMQ_QUEUE,
        body=json.dumps({'pr_number': pr_number, 'repo_name': repository}))
    return 'OK'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

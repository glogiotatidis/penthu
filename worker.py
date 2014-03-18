#!/usr/bin/env python

import json
import pika
import subprocess
import os

RABBITMQ_QUEUE = 'penthu'

if 'RABBITMQ_URL' in os.environ:
    parameters = pika.URLParameters(os.environ['RABBITMQ_URL'])
    connection = pika.BlockingConnection(parameters)
else:
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue=RABBITMQ_QUEUE)

print ' [*] Waiting for messages. To exit press CTRL+C'


def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)
    data = json.loads(body)
    subprocess.call(['imhotep', '--pr-number', str(data['pr_number']),
                     '--repo_name', data['repo_name']])

channel.basic_consume(callback, queue=RABBITMQ_QUEUE, no_ack=True)

channel.start_consuming()

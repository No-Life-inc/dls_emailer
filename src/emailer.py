import os
import pika
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

# RabbitMQ connection parameters
RABBITMQ_URL = f"amqp://{os.getenv('RABBITUSER')}:{os.getenv('RABBITPW')}@{os.getenv('RABBITURL')}/%2F"
story_comment_queue = 'new_comment_on_story'

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue=story_comment_queue, durable=True)

def send_email(email, story_title):
    # Send an email to the user
    print(f"Sending email to {email} for story {story_title}")

def callback(ch, method, properties, body):
    # Parse the message
    message = json.loads(body)
    email = message['email']
    story_title = message['story_title']

    # Send the email
    send_email(email, story_title)

    # Acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)

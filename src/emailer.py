import os
import pika
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

# RabbitMQ connection parameters
RABBITMQ_URL = f"amqp://{os.getenv('RABBITUSER')}:{os.getenv('RABBITPW')}@{os.getenv('RABBITURL')}/%2F"
story_comment_queue = 'new_comment_on_story'
password_change_queue = 'password_changes'

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue=story_comment_queue, durable=True)
channel.queue_declare(queue=password_change_queue, durable=True)



def create_comment_message(email, story_title):
    # Create a message for a new comment
    return json.dumps({'email': email, 'story_title': story_title})

def create_password_change_message(email):
    # Create a message for a password change
    return json.dumps({'email': email})

def send_email(email, subject, body):
    # Send an email to the user
    print(f"Sending email to {email} with subject {subject} and body {body}")

def callback_new_comments(ch, method, properties, body):
    # Parse the message
    message = json.loads(body)
    email = message['email']
    story_title = message['story_title']

    # Create the email subject and body
    subject = f"New comment on {story_title}"
    body = f"A new comment has been posted on your story {story_title}."

    # Send the email
    send_email(email, subject, body)

    # Acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)

def callback_password_changes(ch, method, properties, body):
    # Parse the message
    message = json.loads(body)
    email = message['email']

    # Create the email subject and body
    subject = "Password change"
    body = "Your password has been changed."

    # Send the email
    send_email(email, subject, body)

    # Acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)


# Start consuming from the queues
channel.basic_consume(queue=story_comment_queue, on_message_callback=callback_new_comments, auto_ack=True)
channel.basic_consume(queue=password_change_queue, on_message_callback=callback_password_changes, auto_ack=True)

# Start the consumer
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
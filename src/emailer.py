import os
import pika
from dotenv import load_dotenv
from emailer_functions import callback_new_comments, callback_password_changes

# Load environment variables from .env file
load_dotenv()

# RabbitMQ connection parameters
RABBITMQ_URL = f"amqp://{os.getenv('RABBITUSER')}:{os.getenv('RABBITPW')}@{os.getenv('RABBITURL')}/%2F"
story_comment_queue = 'new_comment_on_story'
password_change_queue = 'password_changes'

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
channel = connection.channel()

# Declare the queues
channel.queue_declare(queue=story_comment_queue, durable=True)
channel.queue_declare(queue=password_change_queue, durable=True)

print("Starting to consume messages")
# Start consuming from the queues
channel.basic_consume(queue=story_comment_queue, on_message_callback=callback_new_comments)
channel.basic_consume(queue=password_change_queue, on_message_callback=callback_password_changes)

# Start the consumer
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

import json

def send_email(email, subject, body):
    # Send an email to the user
    print(f"Sending email to {email} with subject {subject} and body {body}")

def callback_new_comments(ch, method, properties, body):
    print("Received a new comment message")
    try:
        # Parse the message
        message = json.loads(body)
        email = message['user']['email']
        story_title = message['story_title']
        comment = message['comment']

        # Create the email subject and body
        subject = f"New comment on {story_title}"
        emailBody = f"A new comment has been posted on your story: {comment}."

        # Send the email
        send_email(email, subject, emailBody)

        # Acknowledge the message
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Error processing new comment message: {e}")
        raise

def callback_password_changes(ch, method, properties, body):
    print("Received a password change message")
    try:
        # Parse the message
        message = json.loads(body)
        email = message['user']['email']

        # Create the email subject and body
        subject = "Password change"
        emailBody = "Your password has been changed."

        # Send the email
        send_email(email, subject, emailBody)

        # Acknowledge the message
        ch.basic_ack(delivery_tag=method.delivery_tag)
    
    except Exception as e:
        print(f"Error processing password change message: {e}")
        raise
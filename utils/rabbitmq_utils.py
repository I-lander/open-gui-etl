import os
import json
import base64
import requests


def send_message_to_rabbitmq(payload: dict):
    """
    Sends a message (JSON payload) to a RabbitMQ exchange using the HTTP API.

    Environment Variables (must be set beforehand):
    - RABBITMQ_USER: Username for RabbitMQ authentication.
    - RABBITMQ_PASS: Password for RabbitMQ authentication.
    - RABBITMQ_HOST: Hostname or IP of the RabbitMQ server.
    - RABBITMQ_EXCHANGE: Name of the exchange to publish the message to.

    Arguments:
    - payload (dict): The message payload to send (will be encoded as a JSON string).

    This function sends the payload to RabbitMQ using its HTTP API on port 15672.
    """
    user = os.getenv("RABBITMQ_USER")
    password = os.getenv("RABBITMQ_PASS")
    host = os.getenv("RABBITMQ_HOST")
    exchange = os.getenv("RABBITMQ_EXCHANGE")

    # Construct the message format required by RabbitMQ HTTP API
    message = {
        "properties": {},
        "routing_key": "",
        "payload": json.dumps(payload),
        "payload_encoding": "string",
    }

    # URL-encoded '/' is '%2f' for default virtual host in RabbitMQ
    url = f"http://{host}:15672/api/exchanges/%2f/{exchange}/publish"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Basic "
        + base64.b64encode(f"{user}:{password}".encode()).decode(),
    }

    # Send the POST request to RabbitMQ
    response = requests.post(url, headers=headers, json=message)
    print(f"Message: {payload}")

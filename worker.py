import pika
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

visited = set()

# Create folder to store pages
if not os.path.exists("pages"):
    os.makedirs("pages")

# Connect to RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)

channel = connection.channel()

# Declare queue
channel.queue_declare(queue='url_queue')

print("Worker waiting for messages...")

# Function that runs when message received
def callback(ch, method, properties, body):
    url = body.decode()

    # Skip already visited URLs
    if url in visited:
        print("Already visited:", url)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    print("Processing:", url)

    try:
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            html = response.text

            # Save HTML file
            filename = "pages/" + url.replace("https://", "").replace("/", "_") + ".html"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(html)

            print("Saved:", filename)

            # Extract links
            soup = BeautifulSoup(html, "html.parser")
            for link in soup.find_all("a"):
                href = link.get("href")

                if href:
                    full_url = urljoin(url, href)

                    if full_url.startswith("http"):
                        channel.basic_publish(
                            exchange='',
                            routing_key='url_queue',
                            body=full_url
                        )

        visited.add(url)

    except Exception as e:
        print("Error:", e)

    # Acknowledge message
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Start consuming messages
channel.basic_consume(
    queue='url_queue',
    on_message_callback=callback
)

channel.start_consuming()

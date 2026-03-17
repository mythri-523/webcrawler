import pika

# Seed URLs
seed_urls = [
    "https://www.ksrmce.ac.in",
    "https://books.toscrape.com"
]

# Connect to RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)

channel = connection.channel()

# Declare queue
channel.queue_declare(queue='url_queue')

# Send URLs to queue
for url in seed_urls:
    channel.basic_publish(
        exchange='',
        routing_key='url_queue',
        body=url
    )
    print("Sent:", url)

# Close connection
connection.close()

print("All seed URLs sent to queue")

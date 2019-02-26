
import pika
from pshconfig import Config


def test_output():


    # Create a new Config object to ease reading the Platform.sh environment variables.
    # You can alternatively use os.environ yourself.
    config = Config()

    # Get the credentials to connect to the RabbitMQ service.
    credentials = config.credentials('rabbitmq')

    # Establish a connection with the RabbitMQ server
    creds = pika.PlainCredentials(credentials['username'], credentials['password'])
    parameters = pika.ConnectionParameters(credentials['host'], credentials['port'], credentials=creds)

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # Check to make sure that the recipient queue exists
    channel.queue_declare(queue='deploy_days')

    # Try sending a message over the channel
    try:
        # Try sending a message over the channel
        channel.basic_publish(exchange='',
                              routing_key='deploy_days',
                              body='Friday!')

        # Receive the message
        def callback(ch, method, properties, body):
            print(" [x] Received {}".format(body))

        # Tell RabbitMQ that this particular function should receive messages from our 'hello' queue
        channel.basic_consume(callback,
                              queue='deploy_days',
                              no_ack=True)

        # This blocks on waiting for an item from the queue, so comment it out in this demo script.
        # print(' [*] Waiting for messages. To exit press CTRL+C')
        # channel.start_consuming()

        connection.close()

        return " [x] Sent 'Friday!'"
    except Exception as e:
        return e


    # return channel






# import pika
# from pshconfig import Config
# import traceback, sys
#
# # Step #3
# def on_open(connection):
#     connection.channel(on_channel_open)
#
# # Step #4
# def on_channel_open(channel):
#     channel.basic_publish('exchange_name',
#                           'routing_key',
#                           'Test Message',
#                           pika.BasicProperties(content_type='text/plain',
#                                                type='example'))
# def callback(body):
#     # In a real application you'd put the following in a separate script in a loop.
#     print("[x] Deploying on %s<br />\n".format(body))
#
# def test_output():
#
#     # Create a new Config object to ease reading the Platform.sh environment variables.
#     # You can alternatively use os.environ yourself.
#     config = Config()
#
#     # Get the credentials to connect to the RabbitMQ service.
#     credentials = config.credentials('rabbitmq')
#
#     try:
#
#         queue_name = 'deploy_days'
#
#         creds = pika.PlainCredentials(credentials['username'], credentials['password'])
#         parameters = pika.ConnectionParameters(credentials['host'], credentials['port'], credentials=creds)
#
#         # Connect to the RabbitMQ server.
#         connection = pika.SelectConnection(parameters)
#
#         # ERROR - connection closed, need open connection somewhere here.
#         channel = connection.channel(on_open_callback=on_open)
#
#         channel.queue_declare(queue_name)
#
#         msg = channel.basic_publish(exchange='', routing_key=queue_name, body='Friday')
#
#         print('[x] Sent Friday<br/>\n')
#
#         channel.basic_consume(callback(msg.body), queue=queue_name, no_ack=True)
#
#         channel.close()
#         connection.close()
#
#     except Exception as e:
#         return traceback.format_exc(), sys.exc_info()[0]

import pika
from pshconfig import Config
import traceback, sys

def callback(body):
    # In a real application you'd put the following in a separate script in a loop.
    print("[x] Deploying on %s<br />\n".format(body))

def test_output():

    # Create a new Config object to ease reading the Platform.sh environment variables.
    # You can alternatively use os.environ yourself.
    config = Config()

    # Get the credentials to connect to the RabbitMQ service.
    credentials = config.credentials('rabbitmq')

    try:

        queue_name = 'deploy_days'

        creds = pika.PlainCredentials(credentials['username'], credentials['password'])
        parameters = pika.ConnectionParameters(credentials['host'], credentials['port'], credentials=creds)

        # Connect to the RabbitMQ server.
        connection = pika.SelectConnection(parameters)

        channel = connection.channel()

        channel.queue_declare(queue_name)

        msg = channel.basic_publish(exchange='', routing_key=queue_name, body='Friday')

        print('[x] Sent Friday<br/>\n')

        channel.basic_consume(callback(msg.body), queue=queue_name, no_ack=True)

        channel.close()
        connection.close()

    except Exception as e:
        return traceback.format_exc(), sys.exc_info()[0]


# try:
#     queue_name = 'deploy_days'
# #     $queueName = 'deploy_days';
#
#     # Connect to the RabbitMQ server.
#     connection = pika.SelectConnection()
# #     $connection = new AMQPStreamConnection($credentials['host'], $credentials['port'], $credentials['username'], $credentials['password']);
#     channel = connection.channel()
# #     $channel = $connection->channel();
# #
# #     $channel->queue_declare($queueName, false, false, false, false);
# #
# #     $msg = new AMQPMessage('Friday');
# #     $channel->basic_publish($msg, '', 'hello');
# #
# #     echo "[x] Sent 'Friday'<br/>\n";
# #
# #     // In a real application you't put the following in a separate script in a loop.
# #     $callback = function ($msg) {
# #         printf("[x] Deploying on %s<br />\n", $msg->body);
# #     };
# #
# #     $channel->basic_consume($queueName, '', false, true, false, false, $callback);
# #
# #     // This blocks on waiting for an item from the queue, so comment it out in this demo script.
# #     //$channel->wait();
# #
# #     $channel->close();
# #     $connection->close();
# #
# except Exception as e:
#     print(e)
# # } catch (Exception $e) {
# #     print $e->getMessage();
# # }

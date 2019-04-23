
from json import dumps
from json import loads
from kafka import KafkaConsumer, KafkaProducer
from platformshconfig import Config


def usage_example():

    # Create a new Config object to ease reading the Platform.sh environment variables.
    # You can alternatively use os.environ yourself.
    config = Config()

    # Get the credentials to connect to the Kafka service.
    credentials = config.credentials('kafka')

    try:

        kafka_server = '{}:{}'.format(credentials['host'], credentials['port'])

        # Producer
        producer = KafkaProducer(bootstrap_servers=[kafka_server],
                                 value_serializer=lambda x: dumps(x).encode('utf-8'))
        for e in range(10):
            data = {'number' : e}
            producer.send('numtest', value=data)

        # Consumer
        consumer = KafkaConsumer(
            'numtest',
            bootstrap_servers=[kafka_server],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='my-group',
            value_deserializer=lambda x: loads(x.decode('utf-8')))

        output = ''
        for message in consumer:
            output += "{}\n".format(message)
            #output += message.value.number

        return output

    except Exception as e:
        return e

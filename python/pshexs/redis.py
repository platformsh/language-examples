from redis import Redis
from pshconfig import Config
import traceback, sys


def test_output():

    # Create a new config object to ease reading the Platform.sh environment variables.
    # You can alternatively use os.environ yourself.
    config = Config()

    # Get the credentials to connect to the Redis service.
    credentials = config.credentials('redis')

    try:

        # output = str(config.relationshipsDef)

        # host = '127.0.0.1'
        # port = int(os.environ["PORT"])

        redis = Redis(credentials['host'], credentials['port'])
        # redis = Redis(host, port)
        #
        key = "Deploy day"
        value = "Friday"

        # Set a value
        redis.set(key, value)

        # Read it back
        test = redis.get(key)

        return('Found value <strong>{0}</strong> for key <strong>{1}</strong>.'.format(test, key))
        # return relationships if isinstance(relationships, str) else str(relationships)
        # return 'Platform.sh config was properly imported'

    except Exception:
        # return 'platform.sh config WAS NOT properly imported.'
        return traceback.format_exc(), sys.exc_info()[0]



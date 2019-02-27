from redis import Redis
from pshconfig import Config

# Create a new config object to ease reading the Platform.sh environment variables.
# You can alternatively use os.environ yourself.
config = Config()

# Get the credentials to connect to the Redis service.
credentials = config.credentials('redis')

try:

    redis = Redis(credentials['host'], credentials['port'])

    key = "Deploy day"
    value = "Friday"

    # Set a value
    redis.set(key, value)

    # Read it back
    test = redis.get(key)

    print('Found value <strong>{0}</strong> for key <strong>{1}</strong>.'.format(test.decode("utf-8"), key))

except Exception as e:
    print(e)
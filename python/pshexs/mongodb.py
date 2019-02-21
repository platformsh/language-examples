from pymongo import MongoClient
from pshconfig import Config
import traceback, sys


def test_output():

    # Create a new Config object to ease reading the Platform.sh environment variables.
    # You can alternatively use os.environ yourself.
    config = Config()

    # The 'database' relationship is generally the name of primary SQL database of an application.
    # It could be anything, though, as in the case here here where it's called "mongodb".
    credentials = config.credentials('mongodb')

    try:

        server = '{}://{}:{}@{}:{}/{}'.format(
            credentials['scheme'],
            credentials['username'],
            credentials['password'],
            credentials['host'],
            credentials['port'],
            credentials['path']
        )

        client = MongoClient(server)

        collection = client.starwars

        result = collection.insert_one(
            {"name": "Rey",
             "occupation": "Jedi"}
        )

        result_id = result.inserted_id

        document = collection.find_one(
            {"_id": result_id}
        )

        return print('Found {0} ({1})<br />\n'.format(document.name, document.occupation))

    except Exception as e:
        return traceback.format_exc(), sys.exc_info()[0]

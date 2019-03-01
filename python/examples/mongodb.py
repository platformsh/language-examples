from pymongo import MongoClient
from pshconfig import Config


def usage_example():

    # Create a new Config object to ease reading the Platform.sh environment variables.
    # You can alternatively use os.environ yourself.
    config = Config()

    # The 'database' relationship is generally the name of primary SQL database of an application.
    # It could be anything, though, as in the case here here where it's called "mongodb".
    credentials = config.credentials('mongodb')

    try:
        server  = '{0}://{1}:{2}@{3}:{4}/{5}'.format(
            credentials['scheme'],
            credentials['username'],
            credentials['password'],
            credentials['host'],
            credentials['port'],
            credentials['path']
        )

        client = MongoClient(server)

        collection = client.main.starwars

        post = {
            "name": "Rey",
            "occupation": "Jedi"
        }

        post_id = collection.insert_one(post).inserted_id

        document = collection.find_one(
            {"_id": post_id}
        )

        return 'Found {0} ({1})<br />'.format(document['name'], document['occupation'])

    except Exception as e:
        return e

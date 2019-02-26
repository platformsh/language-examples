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

        # server = '{}://{}:{}@{}:{}/{}'.format(
        #     credentials['scheme'],
        #     credentials['username'],
        #     credentials['password'],
        #     credentials['host'],
        #     credentials['port'],
        #     credentials['path']
        # )


        client = MongoClient(credentials['host'], credentials['port'])
        # client = MongoClient(credentials['host'], credentials['port'], credentials['username'], credentials['password'])

        # client = MongoClient(server)

        db = client.test_database

        # ERROR HERE - no users authenticated
        db.command("createUser", credentials['username'], pwd=credentials['password'], roles=["root"])

        # db.createUser(credentials['username'], "readWrite")

        # db.grantRolesToUser(credentials['username'], ["readWrite"])

        # db.grantRolesToUser('admin', [{role: "root", db: "admin"}])

        collection = db.starwars

        rey = {"name": "Rey",
               "occupation": "Jedi"}

        result_id = collection.insert(rey).inserted_id

        document = collection.find_one(
            {"_id": result_id}
        )

        return print('Found {0} ({1})<br />\n'.format(document.name, document.occupation))

    except Exception as e:
        return traceback.format_exc(), sys.exc_info()[0]

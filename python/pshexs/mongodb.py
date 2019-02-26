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

        # {'username': 'main', 'scheme': 'mongodb', 'service': 'mongodb', 'ip': '169.254.133.75',
        #  'hostname': '4y3jxad5eybbbq7vgdbddfj73q.mongodb.service._.eu-3.platformsh.site',
        #  'cluster': 'rjify4yjcwxaa-pythonexs-y2koaha', 'host': 'mongodb.internal', 'rel': 'mongodb', 'path': 'main',
        #  'query': {'is_master': True}, 'password': 'main', 'type': 'mongodb:3.6', 'port': 27017}

        server  = '{0}://{1}:{2}@{3}:{4}/{5}'.format(
            credentials['scheme'],
            credentials['username'],
            credentials['password'],
            credentials['host'],
            credentials['port'],
            credentials['path']
            # 'default_db?authSource=admin'
        )

        client = MongoClient(server)

        collection = client.main.starwars

        post = {
            "name": "Rey",
            "occupation": "Jedi"
        }

        post_id = collection.insert_one(post).inserted_id

        # collection = db.starwars
        #
        # rey = {"name": "Rey",
        #        "occupation": "Jedi"}
        #
        # result_id = collection.insert(rey).inserted_id
        #
        # document = collection.find_one(
        #     {"_id": result_id}
        # )

        # return print('Found {0} ({1})<br />\n'.format(document.name, document.occupation))
        return post_id

    except Exception as e:
        return traceback.format_exc(), sys.exc_info()[0]

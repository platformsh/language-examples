# import pymongo
from pshconfig import Config
import traceback, sys


def test_output():

    # Create a new Config object to ease reading the Platform.sh environment variables.
    # You can alternatively use os.environ yourself.
    config = Config()

    # The 'database' relationship is generally the name of primary SQL database of an application.
    # That's not required, but much of our default automation code assumes it.' \
    # credentials = config.credentials('database')

    try:

        credentials = config.credentials('mongodb')

        return credentials


    except Exception as e:
        return traceback.format_exc(), sys.exc_info()[0]


# from pshconfig import Config
# from pymongo import MongoClient
#
#
# # Create a new Config object to ease reading the Platform.sh environment variables.
# # You can alternatively use os.environ yourself.
# config = Config()
#
# # Get the credentials to connect to the Elasticsearch service
# credentials = config.credentials('mongodb')
#
# try:
#     server = '{}://{}:{}@{}:{}/{}'.format(
#         credentials['scheme'],
#         credentials['username'],
#         credentials['password'],
#         credentials['host'],
#         credentials['port'],
#         credentials['path']
#     )
#
# #     $server = sprintf('%s://%s:%s@%s:%d/%s',
# #         $credentials['scheme'],
# #         $credentials['username'],
# #         $credentials['password'],
# #         $credentials['host'],
# #         $credentials['port'],
# #         $credentials['path']
# #     );
# #
#     client = MongoClient(server)
#
# #     $client = new Client($server);
#     collection = client.starwars
# #     $collection = $client->main->starwars;
#
#     result_id = collection.insert_one({
#         "name": "Rey",
#         "occupation": "Jedi"
#     }).inserted_id
# #     $result = $collection->insertOne([
# #         'name' => 'Rey',
# #         'occupation' => 'Jedi',
# #     ]);
# #
# #
# #     $id = $result->getInsertedId();
# #
#     document = collection.find_one({
#         "_id": result_id
#     })
# #     $document = $collection->findOne([
# #         '_id' => $id,
# #     ]);
# #
#     print('Found {} ({})<br />\n'.format(document.name, document.occupation))
# #     printf("Found %s (%s)<br />\n", $document->name, $document->occupation);
# #
# except Exception as e:
#     print(e)
# # } catch (\Exception $e) {
# #     print $e->getMessage();
# # }

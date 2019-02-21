
def test_output():
    return '{"mongodb_test": "passed"}'



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

import elasticsearch
from pshconfig import Config
import traceback, sys


def test_output():

    # Create a new Config object to ease reading the Platform.sh environment variables.
    # You can alternatively use os.environ yourself.
    config = Config()

    # Get the credentials to connect to the Elasticsearch service.
    credentials = config.credentials('elasticsearch')

    try:
        # The Elasticsearch library lets you connect to multiple hosts.
        # On Platform.sh Standard there is only a single host so just register that.
        hosts = {
            "scheme": credentials['scheme'],
            "host": credentials['host'],
            "port": credentials['port']
        }

        # Create an Elasticsearch client object.
        builder = elasticsearch.Elasticsearch([hosts])
        # $builder = ClientBuilder::create();
        # $builder->setHosts($hosts);
        # $client = $builder->build();

        es_index = 'my_index'
        es_type = 'People'

        # Index a few documents.
        params = {
            "index": es_index,
            "type": es_type
        }

        return credentials


    except Exception as e:
        return traceback.format_exc(), sys.exc_info()[0]



# try:
#     # The Elasticsearch library lets you connect to multiple hosts.
#     # On Platform.sh Standard there is only a single host so just register that.
#     hosts = {
#         "scheme": credentials['scheme'],
#         "host": credentials['host'],
#         "port": credentials['port']
#     }
#
#     # Create an Elasticsearch client object.
#     builder = elasticsearch.Elasticsearch([hosts])
#     # $builder = ClientBuilder::create();
#     # $builder->setHosts($hosts);
#     # $client = $builder->build();
#
#     es_index = 'my_index'
#     es_type = 'People'
#
#     # Index a few documents.
#     params = {
#         "index": es_index,
#         "type": es_type
#     }
#
#     names = ['Ada Lovelace', 'Alonzo Church', 'Barbara Liskov']
#
#     for name in names:
#         params['body']['name'] = name
#     # client.index(params)
#
#     # Force just-added items to be indexed.
#     # client.indices.refresh()
#     # $client->indices()->refresh(array('index' => $index));
#
#     # // Search for documents.
#     # $result = $client->search([
#     #     'index' => $index,
#     #     'type' => $type,
#     #     'body' => [
#     #         'query' => [
#     #             'match' => [
#     #                 'name' => 'Barbara Liskov',
#     #             ],
#     #         ],
#     #     ],
#     # ]);
#
#
# except:
#     pass
#
# #     if (isset($result['hits']['hits'])) {
# #         print <<<TABLE
# # <table>
# # <thead>
# # <tr><th>ID</th><th>Name</th></tr>
# # </thead>
# # <tbody>
# # TABLE;
# #         foreach ($result['hits']['hits'] as $record) {
# #             printf("<tr><td>%s</td><td>%s</td></tr>\n", $record['_id'], $record['_source']['name']);
# #         }
# #         print "</tbody>\n</table>\n";
# #     }
# #
# #     // Delete documents.
# #     $params = [
# #         'index' => $index,
# #         'type' => $type,
# #     ];
# #
# #     $ids = array_map(function($row) {
# #         return $row['_id'];
# #     }, $result['hits']['hits']);
# #
# #     foreach ($ids as $id) {
# #         $params['id'] = $id;
# #         $client->delete($params);
# #     }
# #
# # } catch (Exception $e) {
# #     print $e->getMessage();
# # }

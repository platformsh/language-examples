
import pysolr
import urllib
from pshconfig import Config
import traceback, sys


def test_output():

    # Create a new Config object to ease reading the Platform.sh environment variables.
    # You can alternatively use os.environ yourself.
    config = Config()

    # Get the credentials to connect to the Solr service.
    credentials = config.credentials('solr')

    try:

        # Create a new Solr Client using config variables
        client = pysolr.Solr(credentials['host'])

        # Add a document
        doc_1 = {
            "id": 123,
            "name": "Valentina Tereshkova"
        }

        client.add(doc_1)

        # Add a document

        # Select one document

        # Delete one document


        # credentials = {'service': 'solr', 'ip': '169.254.70.40',
        # 'hostname': '63wf3k4p72q6pxnhkrps3i4csy.solr.service._.eu-3.platformsh.site',
        # 'cluster': 'rjify4yjcwxaa-pythonexs-y2koaha', 'host': 'solr.internal',s
        # 'rel': 'solr', 'path': 'solr/collection1', 'scheme': 'solr', 'type': 'solr:6.6', 'port': 8080}

        # host = credentials['host']
        # port = credentials['port']


        # solr = pysolr.Solr(credentials['host'])
        #
        # solr.add([
        #     {
        #         "id": 123,
        #         "name": "Valentina Tereshkova"
        #     }
        # ])


        # results = solr.search()
        #
        # print("Saw {0} result(s).".format(len(results)))
        #
        # messages = 'Adding one document. Status (0 is success): {0} <br />\n'.format(result'
        #            ' .$result->getStatus(). "<br />\n'

        return credentials


    except Exception as e:
        return traceback.format_exc(), sys.exc_info()[0]

    # try:

        # config_solr = {
        #     "enpoint": {
        #         "localhost": {
        #             "host": credentials['host'],
        #             "port": credentials['port'],
        #             "path": '/' + credentials['path']
        #         }
        #     }
        # }
    #
    # client = KazooClient(config_solr)
    #
    # # Add a document
    # update = client.createUpdate()
#
#     // Add a document
#     $update = $client->createUpdate();
#
#     $doc1 = $update->createDocument();
#     $doc1->id = 123;
#     $doc1->name = 'Valentina Tereshkova';
#
#     $update->addDocuments(array($doc1));
#     $update->addCommit();
#
#     $result = $client->update($update);
#     print "Adding one document. Status (0 is success): " .$result->getStatus(). "<br />\n";
#
#     // Select one document
#     $query = $client->createQuery($client::QUERY_SELECT);
#     $resultset = $client->execute($query);
#     print  "Selecting documents (1 expected): " .$resultset->getNumFound() . "<br />\n";
#
#     // Delete one document
#     $update = $client->createUpdate();
#
#     $update->addDeleteById(123);
#     $update->addCommit();
#     $result = $client->update($update);
#     print "Deleting one document. Status (0 is success): " .$result->getStatus(). "<br />\n";
#
# } catch (Exception $e) {
#     print $e->getMessage();
# }

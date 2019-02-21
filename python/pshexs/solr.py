
# import pysolr
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

        credentials = config.credentials('solr')

        return credentials


    except Exception as e:
        return traceback.format_exc(), sys.exc_info()[0]

# import pysolr
# from pshconfig import Config


# def test_output():

    # Create a new config object to ease reading the Platform.sh environment variables.
    # You can alternatively use getenv() yourself.
    # config = Config()

    # Get the credentials to connect to the Solr service.
    # credentials = config.credentials('solr')

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

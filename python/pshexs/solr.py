
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

        url = "http://{0}:{1}/{2}".format(credentials['ip'],
                                          credentials['port'],
                                          credentials['path'])

        # Create a new Solr Client using config variables
        client = pysolr.Solr(url)

        # Add a document
        doc_1 = {
            "id": 123,
            "name": "Valentina Tereshkova"
        }

        client.add([doc_1])
        result = client.commit()

        # Select one document
        results = client.search('*:*')

        # Delete one document

        return result


    except Exception as e:
        return traceback.format_exc(), sys.exc_info()[0]

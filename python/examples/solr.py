
import pysolr
import solr
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

        message = ''

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

        result0 = client.add([doc_1])
        client.commit()
        message += 'Adding one document. Status (01 is success): {0}'.format(str(result0))

        # Select one document
        query = client.search('*:*')
        message += '\nSelecting documents (1 expected): {0}\n'.format(query.hits)

        # # Delete one document
        result1 = client.delete(doc_1['id'])
        client.commit()
        message += '\nDeleting one document. Status (00 is success): {0}\n'.format(str(result1))

        return message


    except Exception as e:
        return traceback.format_exc(), sys.exc_info()[0]
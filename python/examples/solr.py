
import pysolr
from xml.etree import ElementTree
from pshconfig import Config
import traceback
import sys


def usage_example():

    # Create a new Config object to ease reading the Platform.sh environment variables.
    # You can alternatively use os.environ yourself.
    config = Config()

    # Get the credentials to connect to the Solr service.
    credentials = config.credentials('solr')

    try:
        # message = ''
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
        # message += 'Adding one document. Status (01 is success): {0}'.format(str(result0))

        # Select one document
        query = client.search('*:*')
        # message += '\nSelecting documents (1 expected): {0}'.format(str(query.hits))

        # Delete one document
        result1 = client.delete(doc_1['id'])
        client.commit()
        # message += '\nDeleting one document. Status (00 is success): {0}'.format(str(result1))

        message = '''
Adding one document. Status (01 is success): {0}
Selecting documents (1 expected): {0}
Deleting one document. Status (00 is success): {0}
        '''.format(result0.getStatus(), str(query.hits), str(result1))

        # tree = ElementTree.fromstring(str(result0))
        # response = tree.find("response")
        # status = response.find("status")

        # return type(result0), str(result0), type(query.hits), str(query.hits), type(result1), str(result1)
        # return '{0}, {1}, {2}'.format(result0.getStatus(), str(query.hits), result1.getStatus())
        return message

    except Exception as e:
        return traceback.format_exc(), sys.exc_info()[0]

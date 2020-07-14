
import pysolr
from xml.etree import ElementTree as et
import json
from platformshconfig import Config


def usage_example():

    # Create a new Config object to ease reading the Platform.sh environment variables.
    # You can alternatively use os.environ yourself.
    config = Config()

    # Get the credentials to connect to the Solr service.
    credentials = config.credentials('solr')

    try:
        # Ge the pysolr-formatted connection string.
        formatted_url = config.formatted_credentials('solr', 'pysolr')

        # Create a new Solr Client using config variables
        client = pysolr.Solr(formatted_url)

        # Add a document
        message = ''
        doc_1 = {
            "id": 123,
            "name": "Valentina Tereshkova"
        }
        result0 = client.add([doc_1], commit=True)
        message += 'Adding one document. Status (0 is success): {} <br />'.format(json.loads(result0)['responseHeader']['status'])

        # Select one document
        query = client.search('*:*')
        message += '\nSelecting documents (1 expected): {} <br />'.format(str(query.hits))

        # Delete one document
        result1 = client.delete(doc_1['id'], commit=True)
        message += '\nDeleting one document. Status (0 is success): {}'.format(et.fromstring(result1)[0][0].text)

        return message

    except Exception as e:
        return e

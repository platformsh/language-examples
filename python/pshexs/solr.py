
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


        url = "http://{0}:{1}/{2}".format(credentials['ip'],
                                          credentials['port'],
                                          credentials['path'])
        #
        # client = solr.Solr(url)
        #
        # doc_1 = {
        #     "id": 123,
        #     "name": "Valentina Tereshkova"
        # }
        #
        # result = client.add(doc_1, commit=True)
        #
        # response = client.select('name:Valentina Tereshkova')
        #
        # return result, dir(response)

        # # ----- pysolr attempt -----
        #
        # Create a new Solr Client using config variables
        client = pysolr.Solr(url)

        # Add a document
        doc_1 = {
            "id": 123,
            "name": "Valentina Tereshkova"
        }
        doc_2 = {
            "id": 124,
            "name": "Robert California"
        }

        result0 = client.add([doc_1])
        result1 = client.commit()

        # Select one document
        result2 = client.search('*:*')

        # Delete one document
        client.delete(doc_1['id'])
        client.commit()

        # Am I getting no output for result2 because it is not a string but an object? need dir()?

        # return result0, result1, result2
        # return dir(result0), dir(result1), dir(result2)

        # result0 - string. info in string?
        # result1 - string. info in string?
        return result0, result1, result2.hits


    except Exception as e:
        return traceback.format_exc(), sys.exc_info()[0]

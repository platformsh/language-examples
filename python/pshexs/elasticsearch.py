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
        client = elasticsearch.Elasticsearch([hosts])

        # Index a few documents
        es_index = 'my_index'
        es_type = 'People'

        # Index a few documents.
        params = {
            "index": es_index,
            "type": es_type,
            "body": {"name": ''}
        }

        names = ['Ada Lovelace', 'Alonzo Church', 'Barbara Liskov']

        for name in names:

            params['body']['name'] = name
            # client.index(params)
            client.index(index=params["index"], doc_type=params["type"], body=params['body'])

            # client.index(index=es_index, doc_type=es_type, body={"name": name})

        # Force just-added items to be indexed.
        client.indices.refresh(index=es_index)

        # Search for documents.
        result = client.search(index=es_index, body={
            'query': {
                'match': {
                    'name': 'Barbara Liskov'
                }
            }
        })

        if result['hits']['hits']:

            # table = "<<<TABLE" \
            #         "<table>" \
            #         "<thead>" \
            #         "<tr><th>ID</th><th>Name</th></tr>" \
            #         "</thead>" \
            #         "<tbody>" \
            #         "TABLE;"

            table = "<table>" \
                    "<thead>" \
                    "<tr><th>ID</th><th>Name</th></tr>" \
                    "</thead>" \
                    "<tbody>"

            for record in result['hits']['hits']:

                table += "<tr><td>{0}</td><td>{1}</td><tr>\n".format(record['_id'], record['_source']['name'])

            table += "</tbody>\n</table>\n"
            # Delete documents.




            return table


    except Exception as e:
        return traceback.format_exc(), sys.exc_info()[0]


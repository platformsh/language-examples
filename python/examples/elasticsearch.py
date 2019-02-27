import elasticsearch
from pshconfig import Config


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

        params = {
            "index": es_index,
            "type": es_type,
            "body": {"name": ''}
        }

        names = ['Ada Lovelace', 'Alonzo Church', 'Barbara Liskov']

        for name in names:
            params['body']['name'] = name
            client.index(index=params["index"], doc_type=params["type"], body=params['body'])

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

        table = "<table>\n" \
                "<thead>\n" \
                "<tr><th>ID</th><th>Name</th></tr>\n" \
                "</thead>\n" \
                "<tbody>\n"

        if result['hits']['hits']:

            for record in result['hits']['hits']:

                table += "<tr><td>{0}</td><td>{1}</td><tr>\n".format(record['_id'], record['_source']['name'])

            table += "</tbody>\n</table>\n"

        # Delete documents.
        params = {
            "index": es_index,
            "type": es_type,
        }

        # NEED TO INCLUDE DELETE LOOP - this doesn't look right.
        for name in names:
            client.delete(index=params['index'], doc_type=params['type'], body=params['body'])

        return table

    except Exception as e:
        return e
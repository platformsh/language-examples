import elasticsearch
from pshconfig import Config
import traceback, sys


def usage_example():

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

        indices = {}

        for name in names:
            params['body']['name'] = name
            indices[name] = client.index(index=params["index"], doc_type=params["type"], body=params['body'])

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

        table = '''<table>
<thead>
<tr><th>ID</th><th>Name</th></tr>
</thead>
<tbody>'''

        if result['hits']['hits']:
            for record in result['hits']['hits']:
                table += '''<tr><td>{0}</td><td>{1}</td><tr>\n'''.format(record['_id'], record['_source']['name'])
            table += '''</tbody>\n</table>\n'''

        # Delete documents.
        params = {
            "index": es_index,
            "type": es_type,
        }

        # NEED TO INCLUDE DELETE LOOP - this doesn't look right.
        for name in names:
            client.delete(index=params['index'], doc_type=params['type'], id=indices[name]['_id'])
        #     client.delete(index=params['index'], doc_type=params['type'], body=params['body'])

        # r = db.index(index="reestr", doc_type="some_type", body=doc)
        # # r = {u'_type': u'some_type', u'_id': u'AU36zuFq-fzpr_HkJSkT', u'created': True, u'_version': 1, u'_index': u'reestr'}
        #
        # db.delete(index="reestr", doc_type="some_type", id=r['_id'])

        return table
        # return str(indices['Ada Lovelace'])

    except Exception as e:
        return traceback.format_exc(), sys.exc_info()[0]

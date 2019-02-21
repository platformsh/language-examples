
import pshexs.examples as pshexamples
# import pshexs.web as pshweb
# from python.pshexs import file_get_contents
from pshexs.web import file_get_contents

def create_list():
    names = {
        "elasticsearch_ex": "Elasticsearch",
        "influxdb_ex": "InfluxDB",
        "memcached_ex": "Memcached",
        "mongodb_ex": "MongoDB",
        "mysql_ex": "MySQL",
        "postgresql_ex": "PostgreSQL",
        "rabbitmq_ex": "RabbitMQ",
        "redis_ex": "Redis",
        "solr_ex": "Solr",
    }
    header = '<html>' \
             '<head>' \
             '<title>Platform.sh Python service examples</title>' \
             '<script src="https://cdn.rawgit.com/google/code-prettify/master/loader/run_prettify.js"></script>' \
             '<style type="text/css">' \
             '  details {' \
             '      margin-top: 1em;' \
             '      border: 1px solid #aaa;' \
             '      border-radius: 4px;' \
             '      padding: 0.5em;' \
             '      width: 90%;' \
             '  }' \
             '' \
             '  summary {' \
             '      font-weight: bold;' \
             '      margin: -.5em -.5em 0;' \
             '      padding: .5em;' \
             '  }' \
             '' \
             '  details[open] {' \
             '      padding: .5em;' \
             '  }' \
             '' \
             '  details[open] summary {' \
             '      border-bottom: 1px solid #aaa;' \
             '      margin-bottom: .5em;' \
             '  }' \
             '' \
             '  table, table td, table th {' \
             '      border: 1px solid black;' \
             '  }' \
             '</style>' \
             '</head>' \
             '<body>' \
             '' \
             '<h1>Service examples for Python</h1>'

    body = ''

    services = [service for service in dir(pshexamples) if '__' not in service]

    for service in services:
        name = names[service]
        source = file_get_contents(service)
        # source = file_get_contents(service)
        output = getattr(getattr(pshexamples, service), 'test_output')()

        first = '<details>' \
            '<summary>{0} Sample Code</summary>' \
            '<section>' \
            '<h3>Source</h3>' \
            '<pre class="prettyprint lang-py">{1}</pre>' \
            '</section>' \
            '<section>' \
            '<h3>Output</h3>' \
            '{2}' \
            '</section>' \
            '</details>'.format(name, source, output)

        body += first

    footer = '</body>' \
             '</html>'

    return header + body + footer

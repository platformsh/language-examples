import os
import flask
import gevent.pywsgi
import html
# from xml.sax.saxutils import escape

import examples

app = flask.Flask(__name__)


@app.route('/python/')
def root():
    return create_list()


def file_get_contents(example):
    current_example = os.getcwd() + '/examples/{0}.py'.format(example)

    text = open(current_example, "r")
    contents = text.read()
    text.close()
    return contents


@app.route('/python/<example>')
def add_example_route(example):

    if hasattr(examples, example):
        contents = file_get_contents(example)
        resp = flask.make_response(contents)
        resp.headers['Content-Type'] = 'text/plain'
        return resp
    else:
        return "Sorry, no sample code is available."


@app.route('/python/<example>/output')
def add_example_output_route(example):

    if hasattr(examples, example):

        contents = getattr(getattr(examples, example), 'usage_example')()

        resp = flask.make_response(contents)
        resp.headers['Content-Type'] = 'text/plain'
        return resp
    else:
        return "Sorry, no sample code is available."


def create_list():
    names = {
        "elasticsearch": "Elasticsearch",
        # "influxdb": "InfluxDB",
        "kafka": "Kafka",
        "memcached": "Memcached",
        "mongodb": "MongoDB",
        "mysql": "MySQL",
        "postgresql": "PostgreSQL",
        "rabbitmq": "RabbitMQ",
        "redis": "Redis",
        "solr": "Solr",
        "oraclemysql": "Oracle MySQL"
    }

    header = '''
            <html>
            <head>
            <title>Platform.sh Python service examples</title>
            <script src="https://cdn.rawgit.com/google/code-prettify/master/loader/run_prettify.js"></script>
            <style type="text/css">
                details {
                    margin-top: 1em;
                    border: 1px solid #aaa;
                    border-radius: 4px;
                    padding: 0.5em;
                    width: 90%;
                }
                summary {
                    font-weight: bold;
                    margin: -.5em -.5em 0;
                    padding: .5em;
                }
                details[open] {
                    padding: .5em;
                }
                details[open] summary {
                    border-bottom: 1px solid #aaa;
                    margin-bottom: .5em;
                }
                table, table td, table th {
                    border: 1px solid black;
                }
              </style>
              </head>
              <body>
              <h1>Service examples for Python</h1>
            '''

    body = ''
    services = [service for service in dir(examples) if service in names.keys()]
    for service in services:
        name = names[service]
        source = html.escape(file_get_contents(service))
        output = getattr(getattr(examples, service), 'usage_example')()

        body += '''
                    <details>
                    <summary>{0} Sample Code</summary>
                    <section>
                    <h3>Source</h3>
                    <pre class="prettyprint"><code class="language-py">{1}</code></pre>
                    </section>
                    <section>
                    <h3>Output</h3>
                    {2}
                    </section>
                    </details>'''.format(name, source, output)

    footer = '''
            <body>
            <html>'''

    return header + body + footer


if __name__ == "__main__":
    http_server = gevent.pywsgi.WSGIServer(
        ('127.0.0.1', int(os.environ["PORT"])), app)
    http_server.serve_forever()

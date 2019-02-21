import os
import flask
import gevent.pywsgi

import pshexs.examples as pshexamples
from pshexs.web import create_list
# from pshexs.web import ExampleConverter

app = flask.Flask(__name__)
# app.url_map.converters['pyex'] = ExampleConverter


@app.route('/python/')
def root():
    return create_list()


def file_get_contents(example):
    current_example = os.getcwd() + '/pshexs/examples/{0}.py'.format(example)

    text = open(current_example, "r")
    contents = text.read()
    text.close()
    return contents


@app.route('/python/<example>')
def add_example_route(example):

    if hasattr(pshexamples, example):
        contents = file_get_contents(example)
        resp = flask.make_response(contents)
        resp.headers['Content-Type'] = 'text/plain'
        return resp
    else:
        return "Sorry, no sample code is available."


@app.route('/python/<example>/output')
def add_example_output_route(example):

    if hasattr(pshexamples, example):
        contents = getattr(getattr(pshexamples, example), 'test_output')()

        # resp = flask.make_response(contents)
        # resp.headers['Content-Type'] = 'text/plain'
        return contents
    else:
        return "Sorry, no sample code is available."


if __name__ == "__main__":
    http_server = gevent.pywsgi.WSGIServer(
        ('127.0.0.1', int(os.environ["PORT"])), app)
    http_server.serve_forever()

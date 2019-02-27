
import base64
import secrets
from influxdb import InfluxDBClient
import influxdb
from pshconfig import Config
import traceback, sys


def test_output():

    # Create a new Config object to ease reading the Platform.sh environment variables.
    # You can alternatively use os.environ yourself.
    config = Config()

    # Get the credentials to connect to the InfluxDB service.
    credentials = config.credentials('influxdb')

    try:

        client = InfluxDBClient(host=credentials['host'], port=credentials['port'])

        ping = str(client.ping())

        points = [
            {
                "deploy_time": 0.64,
                "time": 1546556400,
                "fields": {
                    "host": "server01",
                    "region": "us-west"
                },
                "additional": {
                    "cpucount": 10
                }
            },
            {
                "deploy_time": 0.84,
                "time": 1547161200,
                "fields": {
                    "host": "server01",
                    "region": "us-west"
                },
                "additional": {
                    "cpucount": 10
                }
            }
            ]






        #
        # # Read the data back
        # result = client.query('select * from deploy_time LIMIT 5')
        #
        # # if result:
        #
        # table = "<<<TABLE" \
        #         "<table>" \
        #         "<thead>" \
        #         "<tr><th>ID</th><th>Name</th></tr>" \
        #         "</thead>" \
        #         "<tbody>" \
        #         "TABLE;"
        #
        # if result:
        #
        #     for res in result:
        #         table += "<tr><td>{0}</td><td>{1}</td><tr>\n".format(result['time'], result['value'])
        #
        #     table += "</tbody>\n</table>\n"
        #
        # # Drop the database.
        # client.drop_database(database)
        #
        #
        # return table

        # user_list = client.get_list_privileges(username=USER)

        return ping


    except Exception as e:
        return traceback.format_exc(), sys.exc_info()[0]

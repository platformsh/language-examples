import os
import base64
import secrets
from influxdb import InfluxDBClient
import os
import base64
import requests
from pshconfig import Config
import traceback, sys


def test_output():

    # Create a new Config object to ease reading the Platform.sh environment variables.
    # You can alternatively use os.environ yourself.
    config = Config()

    # Get the credentials to connect to the InfluxDB service.
    credentials = config.credentials('influxdb')

    try:

        user = 'deploy_user'
        password = 'password'

        # ~  # curl -XPOST "http://localhost:8086/query" --data-urlencode "q=CREATE USER chronothan WITH PASSWORD 'supersecret' WITH ALL PRIVILEGES"
        #
        url_string = "http://{0}:{1}/query".format(credentials['host'], credentials['port'])
        data_string = "q=CREATE USER {0} WITH PASSWORD '{1}' WITH ALL PRIVILEGES".format(user, password)

        # "curl - XPOST http://localhost:8086/query - -data - urlencode q=CREATE USER {0} WITH PASSWORD '{1}' " \
        #     "WITH ALL PRIVILEGES".format(user, password)

        client = InfluxDBClient(host=credentials['host'], port=credentials['port'])

        # user = 'deploy_user'
        # password = 'password'
        #
        # url_string = "curl - XPOST http://{0}:{1}/query".format(credentials['ip'], credentials['port'])
        # data_string = "urlencode q=CREATE USER {0} WITH PASSWORD '{1}".format(user, password)

        # client.request(url_string, data=data_string)
        r = requests.post(url_string, data=data_string)



        # client.query("CREATE USER {0} WITH PASSWORD '{1}' WITH ALL PRIVILEGES".format(user, password))



        client = InfluxDBClient(host=credentials['ip'], port=credentials['port'], username=user, password=password)





        # dbname = 'deploys'
        # client.create_database(dbname)


        # client.query('SHOW DATABASES;')

        # client.switch_user('root', 'root')
        #
        # client.create_user(username=user, password=password)
        #
        # client = InfluxDBClient(host=credentials['ip'], port=credentials['port'], username=user,
        #                         password=password, database='deploys')

        # client.grant_admin_privileges(username=user)
        #
        # client.create_database(dbname)
        # client.create_retention_policy(name='test', duration='3d', replication='3', default=True)
        # client.switch_database('deploys')
        #
        # ping = str(client.ping())

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
        # Drop the database.
        # client.drop_database(dbname)
        #
        #
        # return table

        # user_list = client.get_list_privileges(username=USER)

        return str(r)

    except Exception as e:
        return traceback.format_exc(), sys.exc_info()[0]

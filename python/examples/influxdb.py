
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

        DATABASE = 'deploys'
        HOST = credentials['host']
        PORT = credentials['port']
        USER = 'deploy_user'
        PASSWORD = base64.b64encode(secrets.token_bytes())

        client = InfluxDBClient(host=HOST, port=PORT)

        #
        # client = InfluxDBClient(host=HOST, port=PORT, username=USER, password=PASSWORD, database=DATABASE)
        client.switch_user('root', 'root')




        # client.grant_privilege('all', username=USER, database=DATABASE)

        # client.grant_admin_privileges(username=USER)


        # client.switch_user(username=USER, password=PASSWORD)
        # client.create_database(DATABASE)

        # password = secrets.token_bytes()
        #
        # # Connecting to the InfluxDB server. By default it has no user defined, so you will need to create it.
        # # client = InfluxDBClient(credentials['host'], credentials['port'], username='deploy_user', password=password)
        # client = InfluxDBClient(credentials['host'], credentials['port'], 'root', 'root', 'deploys')
        #
        # # client = InfluxDBClient(credentials['host'], credentials['port'])
        #
        # # password = secrets.token_bytes()
        # client.create_user('deploy_user', PASSWORD, admin=True)
        # #
        # # client = InfluxDBClient(credentials['host'], credentials['port'], username='deploy_user', password=password)
        #
        # # password = ''
        # # client.query("CREATE USER 'deploy_user' WITH PASSWORD '' WITH ALL PRIVILEGES")
        #
        # # client = InfluxDBClient(credentials['host'], credentials['port'], username='deploy_user', password='')
        #


        # client.switch_user('deploy_user', PASSWORD)



        # database = client.create_database('deploys')
        # client.create_retention_policy('test', '1d', replication='2', database=DATABASE, default=True)
        #

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

        # # Write some data.
        # points = {
        #     "points":
        #     [['deploy_time',  # name of the measurement
        #      0.64,  # the measurement value
        #      {"host": "server01", "region": "us-west"},  # optional tags
        #      {"cpucount": 10},  # optional additional fields
        #      1546556400],  # Time precision has to be set to seconds!
        #
        #     ['deploy_time',  # name of the measurement
        #      0.84,  # the measurement value
        #      {"host": "server01", "region": "us-west"},  # optional tags
        #      {"cpucount": 10},  # optional additional fields
        #      1547161200]]  # Time precision has to be set to seconds!
        # }

        # strin object has now attr get
        # client.write_points(points, time_precision='s', database=DATABASE)




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

        return 'SUCCESS?'


    except Exception as e:
        return traceback.format_exc(), sys.exc_info()[0]

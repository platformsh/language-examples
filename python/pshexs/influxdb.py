
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
        password = secrets.token_bytes()

        # Connecting to the InfluxDB server. By default it has no user defined, so you will need to create it.
        # client = InfluxDBClient(credentials['host'], credentials['port'], username='deploy_user', password=password)
        client = InfluxDBClient(credentials['host'], credentials['port'], username='root', password='root')

        # client = InfluxDBClient(credentials['host'], credentials['port'])

        # password = secrets.token_bytes()
        # client.create_user('deploy_user', password, admin=True)
        #
        # client = InfluxDBClient(credentials['host'], credentials['port'], username='deploy_user', password=password)

        database = client.create_database('deploys')
        client.create_retention_policy('test', '1d', replication='2', database=database, default=True)

        # Write some data.
        points = [
            ['deploy_time',  # name of the measurement
             0.64,  # the measurement value
             {"host": "server01", "region": "us-west"},  # optional tags
             {"cpucount": 10},  # optional additional fields
             1546556400],  # Time precision has to be set to seconds!
            ['deploy_time',  # name of the measurement
             0.84,  # the measurement value
             {"host": "server01", "region": "us-west"},  # optional tags
             {"cpucount": 10},  # optional additional fields
             1547161200]]  # Time precision has to be set to seconds!

        client.write_points(points, time_precision='PRECISION_SECONDS', database=database)

        # Read the data back
        result = client.query('select * from deploy_time LIMIT 5')

        # if result:

        table = "<<<TABLE" \
                "<table>" \
                "<thead>" \
                "<tr><th>ID</th><th>Name</th></tr>" \
                "</thead>" \
                "<tbody>" \
                "TABLE;"

        if result:

            for res in result:
                table += "<tr><td>{0}</td><td>{1}</td><tr>\n".format(result['time'], result['value'])

            table += "</tbody>\n</table>\n"

        # Drop the database.
        client.drop_database(database)


        return table

        # return credentials


    except Exception as e:
        return traceback.format_exc(), sys.exc_info()[0]

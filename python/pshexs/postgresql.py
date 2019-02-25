import psycopg2
from pshconfig import Config
import traceback, sys


def test_output():

    # Create a new Config object to ease reading the Platform.sh environment variables.
    # You can alternatively use os.environ yourself.
    config = Config()

    # The 'database' relationship is generally the name of primary SQL database of an application.
    # That's not required, but much of our default automation code assumes it.' \
    database = config.credentials('postgresql')

    try:

        # Connect to the database.
        conn_params = {
            'host': database['host'],
            'port': database['port'],
            'dbname': database['path'],
            'user': database['username'],
            'password': database['password']
        }

        conn = psycopg2.connect(**conn_params)

        # Open a cursor to perform database operations.
        cur = conn.cursor()

        # Creating a table.
        sql = "CREATE TABLE People (" \
              "id SERIAL PRIMARY KEY," \
              "name VARCHAR(30) NOT NULL," \
              "city VARCHAR(30) NOT NULL" \
              ")"

        cur.execute(sql)

        # Insert data.
        sql = "INSERT INTO People (name, city) VALUES" \
              "('Neil Armstrong', 'Moon')," \
              "('Buzz Aldrin', 'Glen Ridge')," \
              "('Sally Ride', 'La Jolla');"

        cur.execute(sql)

        # Show table.
        sql = "SELECT * FROM People"
        cur.execute(sql)
        result = cur.fetchall()  # fetchmany(), fetchall()

        if result:
            table = "<table>" \
                    "<thead>" \
                    "<tr><th>ID</th><th>Name</th></tr>" \
                    "</thead>" \
                    "<tbody>"

            for record in result:
                table += "<tr><td>{0}</td><td>{1}</td><tr>\n".format(record[1], record[2])

            table += "</tbody>\n</table>\n"

        # Close communication with the database
        cur.close()
        conn.close()

        return table


    except Exception as e:
        return traceback.format_exc(), sys.exc_info()[0]

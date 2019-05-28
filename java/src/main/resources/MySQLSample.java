package sh.platform.languages;

import sh.platform.config.Config;
import sh.platform.config.MySQL;

import javax.sql.DataSource;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

public class MySQLSample {

    public static void main(String[] args) throws SQLException {
        Config config = new Config();
        MySQL database = config.getCredential("database", MySQL::new);
        DataSource dataSource = database.get();

        try (Connection connection = dataSource.getConnection()) {
            String sql = "CREATE TABLE JAVA_PEOPLE (" +
                    " id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY," +
                    "name VARCHAR(30) NOT NULL," +
                    "city VARCHAR(30) NOT NULL)";

            final Statement statement = connection.createStatement();
            statement.execute(sql);
            // Insert data.
            sql = "INSERT INTO JAVA_PEOPLE (name, city) VALUES" +
                    "('Neil Armstrong', 'Moon')," +
                    "('Buzz Aldrin', 'Glen Ridge')," +
                    "('Sally Ride', 'La Jolla')";

            statement.execute(sql);
            // Show table.
            sql = "SELECT * FROM JAVA_PEOPLE";
            final ResultSet resultSet = statement.executeQuery(sql);
            while (resultSet.next()) {
                int id = resultSet.getInt("id");
                String name = resultSet.getString("name");
                String city = resultSet.getString("city");
                System.out.println(String.format("the id %d the name %s and city %s", id, name, city));
            }
            statement.execute("DROP TABLE JAVA_PEOPLE");
        }
    }
}

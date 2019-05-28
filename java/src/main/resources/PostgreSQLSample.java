package sh.platform.languages;

import sh.platform.config.Config;
import sh.platform.config.MySQL;
import sh.platform.config.PostgreSQL;

import javax.sql.DataSource;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

public class PostgreSQLSample {

    public static void main(String[] args) throws SQLException {
        Config config = new Config();
        PostgreSQL database = config.getCredential("postgresql", PostgreSQL::new);
        DataSource dataSource = database.get();

        try (Connection connection = dataSource.getConnection()) {
            String sql = "CREATE TABLE JAVA_FRAMEWORKS (" +
                    " id SERIAL PRIMARY KEY," +
                    "name VARCHAR(30) NOT NULL)";

            final Statement statement = connection.createStatement();
            statement.execute(sql);
            // Insert data.
            sql = "INSERT INTO JAVA_FRAMEWORKS (name) VALUES" +
                    "('Spring')," +
                    "('Jakarta EE')," +
                    "('Eclipse JNoSQL')";

            statement.execute(sql);
            // Show table.
            sql = "SELECT * FROM JAVA_FRAMEWORKS";
            final ResultSet resultSet = statement.executeQuery(sql);
            while (resultSet.next()) {
                int id = resultSet.getInt("id");
                String name = resultSet.getString("name");
                System.out.println(String.format("the id %d the name %s ", id, name));
            }
            statement.execute("DROP TABLE JAVA_FRAMEWORKS");
        }
    }
}

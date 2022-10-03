package sh.platform.languages.sample;

import sh.platform.config.Config;
import sh.platform.config.MySQL;
import sh.platform.config.PostgreSQL;

import javax.sql.DataSource;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.function.Supplier;

public class PostgreSQLSample implements Supplier<String> {

    @Override
    public String get() {
        StringBuilder logger = new StringBuilder();

        // Create a new config object to ease reading the Platform.sh environment variables.
        // You can alternatively use getenv() yourself.
        Config config = new Config();

        // The 'database' relationship is generally the name of primary SQL database of an application.
        // It could be anything, though, as in the case here here where it's called "postgresql".
        PostgreSQL database = config.getCredential("postgresql", PostgreSQL::new);
        DataSource dataSource = database.get();

        // Connect to the database
        try (Connection connection = dataSource.getConnection()) {

            // Creating a table.
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
            logger.append("<p>");
            while (resultSet.next()) {
                int id = resultSet.getInt("id");
                String name = resultSet.getString("name");
                logger.append(String.format("the JAVA_FRAMEWORKS id %d the name %s ", id, name));
                logger.append('\n');
            }
            logger.append("</p>");
            statement.execute("DROP TABLE JAVA_FRAMEWORKS");
            return logger.toString();
        } catch (SQLException exp) {
            throw new RuntimeException("An error when execute PostgreSQL", exp);
        }
    }
}

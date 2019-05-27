package sh.platform.config.sample;

import sh.platform.config.Config;
import sh.platform.config.PostgreSQL;

import javax.sql.DataSource;

public class PostgreSQLSample {

    public static void main(String[] args) {
        Config config = new Config();
        PostgreSQL database = config.getCredential("database", PostgreSQL::new);
        DataSource dataSource = database.get();

    }
}

import com.mongodb.MongoClient;
import sh.platform.config.Config;
import sh.platform.config.MongoDB;

public class MongoDBSample {

    public static void main(String[] args) {
        Config config = new Config();
        MongoDB database = config.getCredential("database", MongoDB::new);
        MongoClient mongoClient = database.get();
    }
}

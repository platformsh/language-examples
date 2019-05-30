package sh.platform.languages.sample;

import com.mongodb.MongoClient;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import org.bson.Document;
import sh.platform.config.Config;
import sh.platform.config.MongoDB;

import java.util.function.Consumer;

import static com.mongodb.client.model.Filters.eq;

public class MongoDBSample implements Consumer<Void> {

    public static void main(String[] args) {

        // Create a new config object to ease reading the Platform.sh environment variables.
        // You can alternatively use getenv() yourself.
        Config config = new Config();
        // The 'database' relationship is generally the name of primary database of an application.
        // It could be anything, though, as in the case here here where it's called "mongodb".
        MongoDB database = config.getCredential("mongodb", MongoDB::new);
        MongoClient mongoClient = database.get();
        final MongoDatabase mongoDatabase = mongoClient.getDatabase(database.getDatabase());
        MongoCollection<Document> collection = mongoDatabase.getCollection("scientist");
        Document doc = new Document("name", "Ada Lovelace")
                .append("city", "London");

        collection.insertOne(doc);
        Document myDoc = collection.find(eq("_id", doc.get("_id"))).first();
        System.out.println(myDoc.toJson());
        collection.deleteOne(eq("_id", doc.get("_id")));

    }

    @Override
    public void accept(Void aVoid) {
        MongoDBSample.main(new String[0]);
    }
}

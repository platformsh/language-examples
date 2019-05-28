package sh.platform.languages;

import com.mongodb.MongoClient;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import org.bson.Document;
import sh.platform.config.Config;
import sh.platform.config.MongoDB;

import static com.mongodb.client.model.Filters.eq;

public class MongoDBSample {

    public static void main(String[] args)  {
        Config config = new Config();
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
}

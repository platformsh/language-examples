package examples

import (
  "fmt"
  "context"
  "time"
  psh "github.com/platformsh/config-reader-go/v2"
  "go.mongodb.org/mongo-driver/mongo"
  "go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo/options"
)

func FormattedCredentialsMongoDB(creds psh.Credential) (string, error) {
  formatted := fmt.Sprintf("%s://%s:%s@%s:%d/%s",
    creds.Scheme, creds.Username, creds.Password, creds.Host, creds.Port, creds.Path)
  return formatted, nil
}

func UsageExampleMongoDB() string {

  // Create a NewRuntimeConfig object to ease reading the Platform.sh environment variables.
	// You can alternatively use os.Getenv() yourself.
  config, err := psh.NewRuntimeConfig()
  if err != nil {
    panic(err)
  }

  // Get the credentials to connect to the Solr service.
  credentials, err := config.Credentials("mongodb")
  checkErr(err)

  formatted, err := FormattedCredentialsMongoDB(credentials)
  if err != nil {
    panic(err)
  }

  ctx, _ := context.WithTimeout(context.Background(), 10*time.Second)
  client, err := mongo.Connect(ctx, options.Client().ApplyURI(formatted))
  checkErr(err)

  collection := client.Database("main").Collection("starwars")

  res, err := collection.InsertOne(ctx, bson.M{"name": "Rey", "occupation": "Jedi"})
  id := res.InsertedID

  cursor, err := collection.Find(context.Background(), bson.M{"_id": id})
  if err != nil {
    panic(err)
  }

  cursor.Next(context.Background())
  document := cursor.Current

  // var result struct {
  //   Value float64
  // }
  // filter := bson.M{"_id": id}
  // ctx, _ = context.WithTimeout(context.Background(), 5*time.Second)
  // err = collection.FindOne(ctx, filter).Decode(&result)
  // if err != nil {
  //     panic(err)
  // }

  // printf("Found %s (%s)<br />\n", $document->name, $document->occupation);


  return fmt.Sprintf("Found %s (%s)", document[0], document[1])


  return "Successfully connected!"
}

package examples

import (
  "fmt"
  "context"
  "time"
  psh "github.com/platformsh/config-reader-go/v2"
  "github.com/mongodb/mongo-go-driver/mongo"
  "go.mongodb.org/mongo-driver/mongo/options"
)

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

  mongoString := fmt.Sprintf(credentials.Scheme + "%s://%s:%s@%s:%d/%s",
  credentials.Scheme, credentials.Username, credentials.Password, credentials.Host, credentials.Port, credentials.Path)

  ctx, _ := context.WithTimeout(context.Background(), 10*time.Second)
  client, err := mongo.Connect(ctx, options.Client().ApplyURI(mongoString))
  checkErr(err)

  fmt.Println(client)

  return credentials.Host
}

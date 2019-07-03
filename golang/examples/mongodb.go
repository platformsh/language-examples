package examples

import (
  "fmt"
  "context"
  "time"
  psh "github.com/platformsh/config-reader-go/v2"
  "go.mongodb.org/mongo-driver/mongo"
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

  fmt.Println(client)

  return err.Error()
}

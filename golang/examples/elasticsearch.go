package examples

import (
  "fmt"
  psh "github.com/platformsh/config-reader-go/v2"
  "gopkg.in/olivere/elastic.v5"
)

func UsageExampleElasticsearch() string {

  // Create a NewRuntimeConfig object to ease reading the Platform.sh environment variables.
	// You can alternatively use os.Getenv() yourself.
  config, err := psh.NewRuntimeConfig()
  if err != nil {
    panic(err)
  }

  // Get the credentials to connect to the Solr service.
  credentials, err := config.Credentials("elasticsearch")
  checkErr(err)

  formatted := fmt.Sprintf("http://%s:%s", credentials.Host, credentials.Port)
  client, err := elastic.NewClient(elastic.SetURL(formatted))
  if err != nil {
    panic(err)
  }

  fmt.Println(client)

  return "Successfully connected!"
}

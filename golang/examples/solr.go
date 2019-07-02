package examples

import (
  psh "github.com/platformsh/config-reader-go/v2"
)

func UsageExampleSolr() string {

  // Create a NewRuntimeConfig object to ease reading the Platform.sh environment variables.
	// You can alternatively use os.Getenv() yourself.
  config, err := psh.NewRuntimeConfig()
  if err != nil {
    panic(err)
  }

  // Get the credentials to connect to the Solr service.
  credentials, err := config.Credentials("solr")
  checkErr(err)


  return credentials.Host
}

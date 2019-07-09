package examples

import (
  "fmt"
  "strings"
  psh "github.com/platformsh/config-reader-go/v2"
  "github.com/vanng822/go-solr/solr"
)

type SolrCredentials struct {
  Url        string
  Collection string
}

func FormattedCredentialsSolr(creds psh.Credential) (SolrCredentials, error) {

  var formatted SolrCredentials

  path := strings.SplitAfter(creds.Path, "/")

  formatted.Url = fmt.Sprintf("%s:%d/%s", creds.Host, creds.Port, path[0])
  formatted.Collection = path[1]

  return formatted, nil

}

func UsageExampleSolr() string {

  // Create a NewRuntimeConfig object to ease reading the Platform.sh environment variables.
  // You can alternatively use os.Getenv() yourself.
  config, err := psh.NewRuntimeConfig()
  if err != nil {
    panic(err)
  }

  // Get the credentials to connect to the Solr service.
  credentials, err := config.Credentials("solr")
  if err != nil {
    panic(err)
  }

  // Retrieve Solr formatted credentials
  formatted, err := FormattedCredentialsSolr(credentials)
  if err != nil {
    panic(err)
  }

  si, err := solr.NewSolrInterface(formatted.Url, formatted.Collection)
  if err != nil {
    panic(err)
  }

  fmt.Println(si)

  return credentials.Host
}

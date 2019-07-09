package examples

import (
  "fmt"
  "strconv"
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

  formatted.Url = fmt.Sprintf("http://%s:%d/%s", creds.Host, creds.Port, path[0])
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

  // Retrieve Solr formatted credentials.
  formatted, err := FormattedCredentialsSolr(credentials)
  if err != nil {
    panic(err)
  }

  // Create a new Solr Interface using the formatted credentials.
  solrInt, err := solr.NewSolrInterface(formatted.Url, formatted.Collection)
  if err != nil {
    panic(err)
  }

  // Add a document.
  docs := make([]solr.Document, 0, 1)
  docs = append(docs, solr.Document{"id": 123, "name": "Valentina Tereshkova"})

  response, err := solrInt.Add(docs, 0, nil)
  if err != nil {
    panic(err)
  }

  message := fmt.Sprintf("Adding one document - Success: %s", strconv.FormatBool(response.Success))

  fmt.Println(message)

  // Commit the changes for search.
  response2, err := solrInt.Commit()
  if err != nil {
    panic(err)
  }

  fmt.Println(response2)

  // Select one document.
  query := solr.NewQuery()
  query.Q("*:*")
  s := solrInt.Search(query)
  res, err := s.Result(nil)
  if err != nil {
    panic(err)
  }

  numFound := res.Results.NumFound

  message2 := fmt.Sprintf("Selecting document (1 expected): %d", numFound)


  // Delete one document.

  return message2
}

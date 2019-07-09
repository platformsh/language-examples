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

  message := fmt.Sprintf("Adding one document - Success: %s\n", strconv.FormatBool(response.Success))
  // message += strconv.Itoa(responseStatus.Status)

  // Commit the changes for search.
  _, err = solrInt.Commit()
  if err != nil {
    panic(err)
  }



  // Check the core status and then select the document.
  ca, _ := solr.NewCoreAdmin(formatted.Url)
  query := solr.NewQuery()
  query.Q("*:*")

  responseStatus, err := ca.Status(formatted.Collection)
  if err != nil {
    panic(err)
  }

  if responseStatus.Status != 1 {
    s := solrInt.Search(query)
    // r, _ := s.Result(nil)
    // fmt.Println(r.Results.NumFound)
    fmt.Println(s)
  }

  // fmt.Println(responseStatus)
  //
  // s := solrInt.Search(query)
  // r, _ := s.Result(nil)
  // fmt.Println(r.Results.NumFound)



  // Delete the document.
  res, err := solrInt.Delete(solr.M{"id": 123}, nil)
  if err != nil {
    panic(err)
  }

  message += fmt.Sprintf("Deleting one document - Success: %s", strconv.FormatBool(res.Success))

  return message
}

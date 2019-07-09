package examples

import (
  "fmt"
  psh "github.com/platformsh/config-reader-go/v2"
  "github.com/bradfitz/gomemcache/memcache"
)

func FormattedCredentialsMemcached(creds psh.Credential) (string, error) {
  formatted := fmt.Sprintf("%s:%d", creds.Host, creds.Port)
  return formatted, nil
}

func UsageExampleMemcached() string {

  // Create a NewRuntimeConfig object to ease reading the Platform.sh environment variables.
	// You can alternatively use os.Getenv() yourself.
  config, err := psh.NewRuntimeConfig()
  if err != nil {
    panic(err)
  }

  // Get the credentials to connect to the Solr service.
  credentials, err := config.Credentials("memcached")
  checkErr(err)

  // Retrieve formatted credentials for gomemcache.
  formatted, err := FormattedCredentialsMemcached(credentials)
  checkErr(err)

  // Connect to Memcached.
  mc := memcache.New(formatted)

  // Set a value.
  key := "Deploy_day"
  value := "Friday"

  err = mc.Set(&memcache.Item{Key: key, Value: []byte(value)})

  // Read it back.
  test, err := mc.Get("Deploy_day")

  return fmt.Sprintf("Found value <strong>%s</strong> for key <strong>%s</strong>.", test.Value, key)
}

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

  // formatted := fmt.Sprintf("%s:%d", credentials.Host, credentials.Port)

  formatted, err := FormattedCredentialsMemcached(credentials)
  checkErr(err)

  mc := memcache.New(formatted)

  key := "Deploy_day"
  value := "Friday"

  err = mc.Set(&memcache.Item{Key: key, Value: []byte(value)})

  test, err := mc.Get("Deploy_day")

  return fmt.Sprintf("Found value <strong>%s</strong> for key <strong%sstrong>.", test.Value, key)
}

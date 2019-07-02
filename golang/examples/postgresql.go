package examples

import (
  psh "github.com/platformsh/config-reader-go/v2"
)

func UsageExamplePostgreSQL() string {

  // Create a new Config object to ease reading the Platform.sh environment variables.
  // You can alternatively use os.Getenv() yourself.
  config, err := psh.NewRuntimeConfig()
  if err != nil {
    panic(err)
  }

  // The 'database' relationship is generally the name of the primary SQL database of an application.
  // It could be anything, though, as in the case here where it's called "postgresql".
  credentials, err := config.Credentials("postgresql")
  checkErr(err)


  return credentials.Host
}

// checkErr is a simple wrapper for panicking on error.
// It likely should not be used in a real application.
func checkErr(err error) {
	if err != nil {
		panic(err)
	}
}

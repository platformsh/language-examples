package examples

import (
  "fmt"
  "database/sql"
  _ "github.com/lib/pq"
  psh "github.com/platformsh/config-reader-go/v2"
)

func UsageExamplePostgreSQL() string {

  // Create a NewRuntimeConfig object to ease reading the Platform.sh environment variables.
	// You can alternatively use os.Getenv() yourself.
  config, err := psh.NewRuntimeConfig()
  if err != nil {
    panic(err)
  }

  // The 'database' relationship is generally the name of the primary SQL database of an application.
  // It could be anything, though, as in the case here where it's called "postgresql".
  credentials, err := config.Credentials("postgresql")
  checkErr(err)

  psqlInfo := fmt.Sprintf("host=%s port=%d user=%s " + "password=%s dbname=%s sslmode=disable", credentials.Host, credentials.Port, credentials.Username, credentials.Password, credentials.Path)

  db, err := sql.Open("postgres", psqlInfo)
  if err != nil {
    panic(err)
  }
  defer db.Close()


  return "Successfully connected!"
}

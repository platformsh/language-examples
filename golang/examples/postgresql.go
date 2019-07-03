package examples

import (
  "fmt"
  "database/sql"
  _ "github.com/lib/pq"
  psh "github.com/platformsh/config-reader-go/v2"
)

func FormattedCredentialsPostgreSQL(creds psh.Credential) (string, error) {
  formatted := fmt.Sprintf("host=%s port=%d user=%s " + "password=%s dbname=%s sslmode=disable",
    creds.Host, creds.Port, creds.Username, creds.Password, creds.Path)
  return formatted, nil
}

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

  formatted, err := FormattedCredentialsPostgreSQL(credentials)
  if err != nil {
    panic(err)
  }

  db, err := sql.Open("postgres", formatted)
  if err != nil {
    panic(err)
  }
  defer db.Close()

  // Creating a table
  sqlCreate := `
CREATE TABLE IF NOT EXISTS People (
id SERIAL PRIMARY KEY,
name VARCHAR(30) NOT NULL,
city VARCHAR(30) NOT NULL)`

  _, err = db.Exec(sqlCreate)
  if err != nil {
    panic(err)
  }

  // Insert data.
  sqlInsert := `
INSERT INTO People (name, city) VALUES
('Neil Armstrong', 'Moon'),
('Buzz Aldrin', 'Glen Ridge'),
('Sally Ride', 'La Jolla');`

  _, err = db.Exec(sqlInsert)
  if err != nil {
    panic(err)
  }

  table := `<table>
<thead>
<tr><th>Name</th><th>City</th></tr>
</thead>
<tbody>`

  var id int
  var name string
  var city string

  rows, err := db.Query("SELECT * FROM People")
  if err != nil {
    panic(err)
  } else {
    for rows.Next() {
      err = rows.Scan(&id, &name, &city)
      checkErr(err)
      table += fmt.Sprintf("<tr><td>%s</td><td>%s</td><tr>\n", name, city)
    }
    table += "</tbody>\n</table>\n"
  }

  _, err = db.Exec("DROP TABLE People")
  if err != nil {
    panic(err)
  }

  return err.Error()
}

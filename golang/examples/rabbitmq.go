package examples

import (
  "fmt"
  "github.com/streadway/amqp"
  psh "github.com/platformsh/config-reader-go/v2"
)

func FormattedCredentialsRabbitMQ(creds psh.Credential) (string, error) {
  formatted := fmt.Sprintf("amqp://%s:%s@%s:%s/", creds.Username, creds.Password,
    creds.Host, creds.Port, creds.Path)
  return formatted, nil
}

func UsageExampleRabbitMQ() string {

  // Create a NewRuntimeConfig object to ease reading the Platform.sh environment variables.
	// You can alternatively use os.Getenv() yourself.
  config, err := psh.NewRuntimeConfig()
  if err != nil {
    panic(err)
  }

  // Get the credentials to connect to the Solr service.
  credentials, err := config.Credentials("rabbitmq")
  checkErr(err)


  // Using the amqp formatted credentials package
	formatted, err := FormattedCredentialsRabbitMQ(credentials)
	checkErr(err)

  // Connect to the RabbitMQ server
  connection, err := amqp.Dial(formatted)
  checkErr(err)

  // Make a channel
  channel, err := connection.Channel()
  checkErr(err)

  fmt.Println(channel)


  return credentials.Host
}

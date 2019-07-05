package examples

import (
  "fmt"
  "github.com/streadway/amqp"
  psh "github.com/platformsh/config-reader-go/v2"
)

func FormattedCredentialsRabbitMQ(creds psh.Credential) (string, error) {
  formatted := fmt.Sprintf("%s://%s:%s@%s:%d/", creds.Scheme, creds.Username,
    creds.Password, creds.Host, creds.Port)
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
  defer connection.Close()

  // Make a channel
  channel, err := connection.Channel()
  checkErr(err)
  defer channel.Close()

  q, err := channel.QueueDeclare(
    "deploy_days", // name
    false,         // durable
    false,         // delete when unused
    false,         // exclusive
    false,         // no-wait
    nil,           // arguments
  )

  body := "Friday"
  msg := fmt.Sprintf("Deploying on %s\n", body)

  err = channel.Publish(
    "",      // exchange
    q.Name,  // routing key
    false,   // mandatory
    false,   // immediate
    amqp.Publishing{
      ContentType: "text/plain",
      Body: []byte(msg),
    })
  checkErr(err)

  outputMSG := fmt.Sprintf("[x] Sent '%s'\n", body)

  // msgs, err := channel.Consume(
  //   q.Name,  // queue
  //   "",      // consumer
  //   true,    // auto-ack
  //   false,   // exclusive
  //   false,   // no-local
  //   false,   // no-wait
  //   nil,     // args
  // )
  // checkErr(err)
  //
  // for d := range msgs {
  //   outputMSG += fmt.Sprintf("[x] Received message: '%s'\n", d.Body)
  // }

  return outputMSG
}

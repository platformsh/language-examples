const amqp = require('amqplib');
const config = require("platformsh-config").config();

exports.usageExample = async function() {
    const credentials = config.credentials('rabbitmq');
    const connectionString = 'amqp://' + credentials.username + ':' + credentials.password + '@' + credentials.host + ':' + credentials.port;
    const connection = await amqp.connect(connectionString);
    const channel = await connection.createChannel();

    const queue = 'hello';
    const message = 'Deploy Friday!';

    channel.assertQueue(queue, {durable: false});
    channel.sendToQueue(queue, Buffer.from(message))
    channel.consume(queue, function(msg) {
        if (msg !== null) {
            console.log(msg.content.toString());
            channel.ack(msg);
        }
    });

    return '[x] Message sent: ' + message;
};

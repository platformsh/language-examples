const amqp = require('amqplib/callback_api');
const config = require("platformsh-config").config();

exports.usageExample = async function() {
    try {
        const credentials = config.credentials('rabbitmq');
        console.log(credentials);

        let connectionString = 'amqp://' + credentials.username + ':' + credentials.password + '@' + credentials.host + ':' + credentials.port;
        console.log(connectionString);

        let connection = await amqp.connect(connectionString);
        console.log(connection);

        let channel = await connection.createChannel();
        console.log(channel);

        let queue = 'hellotest';
        let message = 'Deploy Friday!';

        await channel.assertQueue(queue, {durable: false});
        await channel.sendToQueue(queue, Buffer.from(message))

        let output = 'Message sent: ' + queue + ' ' + message;

        return output;
    } catch (error) {
        console.error(error);
    }
};

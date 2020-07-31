const config = require("platformsh-config").config();
const amqp = require('amqplib/callback_api');

const credentials = config.credentials('rabbitmq');

const rabbit_connection = 'amqp://' + credentials.username + ':' + credentials.password + '@' + credentials.host + ':' + credentials.port;

amqp.connect(rabbit_connection, function(error0, connection) {
    if (error0) {
        throw error0;
    }
    connection.createChannel(function(error1, channel) {
        if (error1) {
            throw error1;
        }
        var queue = 'hello';
        var msg = 'Deploy Friday!';
        channel.assertQueue(queue, {
            durable: false
        });
        channel.sendToQueue(queue, Buffer.from(msg));
        console.log(" [x] Sent %s", msg);
    });

    setTimeout(function() {
        connection.close();
        process.exit(0);
    }, 500);
});

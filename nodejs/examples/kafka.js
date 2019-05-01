const Kafka = require('node-rdkafka');
const config = require("platformsh-config").config();

exports.usageExample = async function() {
    const credentials = config.credentials('kafka');

    // Set up the Producer.
    (() => {
        const stream = Kafka.Producer.createWriteStream({
            'metadata.broker.list': `${credentials.host}:${credentials.port}`
        }, {}, {
            topic: 'node-test'
        });

        stream.on('error', function (err) {
            // Here's where we'll know if something went wrong sending to Kafka.
            console.error('Error in the Kafka stream:');
            console.error(err);
        });

        // Enqueue a few items.
        [...Array(5).keys()].forEach((i) => {
            console.log('Enqueuing item: ' + i);
            let message = Buffer.from(JSON.stringify({
                'number': i
            }));
            let success = stream.write(message);
            console.log('Write response: ' + success);
        });
    })();

    let output = new Promise((resolve, reject) => {
        const consumer = new Kafka.KafkaConsumer({
            'group.id': 'kafka',
            'metadata.broker.list': `${credentials.host}:${credentials.port}`
        }, {});

        consumer.connect();

        console.log('Consumer connected');

        let timer;

        consumer.on('ready', function() {
            console.log('Ready fired');
            consumer.subscribe(['node-test']);

            // Read one message every 500 milliseconds
            /*
            timer = setInterval(function() {
                consumer.consume(1);
            }, 500);
            */

            consumer.consume(1, (err, message) => {
                console.log('consume callback fired');
                console.log(err);
                console.log(message);
            });


        });

        consumer.on('subscribed', (data) => {
            console.log('Subscribed fired');
            console.log(data);
        });

        console.log('ready listener added');

        let output = '';

        consumer.on('data', (data) => {
            console.log('Data fired');
            console.log(data.value.toString());
            let message = JSON.parse(data.value.toString());
            output += message.number + ", ";
            // A production consumer would not self-terminate like this,
            // but it's just for demonstration purposes.
            if (message.number >= 5) {
                consumer.disconnect();
                clearInterval(timer);
                resolve(output);
            }
        });

        console.log('data listener added');
    });

    return output;
};

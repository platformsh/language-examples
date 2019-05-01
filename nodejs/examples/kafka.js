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
            var message = Buffer.from(JSON.stringify({
                'number': i
            }));
            stream.write(message);
        });
    })();

    var output = '';

    // Set up the Consumer.
    await (() => {
        const consumer = new Kafka.KafkaConsumer({
            'group.id': 'kafka',
            'metadata.broker.list': `${credentials.host}:${credentials.port}`
        }, {});

        consumer.connect();

        consumer.on('ready', function() {
            consumer.subscribe(['node-tes']);
            consumer.consume();
        });


        consumer.on('data', function(data) {
            var message = JSON.parse(data.value.toString());
            output += number + ", ";
            // A production consumer would not self-terminate like this,
            // but it's just for demonstration purposes.
            if (number >= 5) {
                consumer.disconnect();
            }
        });
    })();


    return output;
};

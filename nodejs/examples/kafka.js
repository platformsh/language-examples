'use strict';

const { Kafka } = require('kafkajs');
const config = require("platformsh-config").config();

exports.usageExample = async function() {

    const credentials = config.credentials('kafka');

    console.log("Credentials are:");
    console.log(credentials);

    const kafka = new Kafka({
        clientId: 'my-app',
        brokers: [`${credentials.host}:${credentials.port}`]
    });

    // Set up the Producer.
    const producer = kafka.producer();
    await producer.connect();
    await producer.send({
        topic: 'kafka-node',
        messages: [
            { value: 'Hello KafkaJS user!' },
        ],
    });

    // Set up the Consumer.
    const consumer = kafka.consumer({ groupId: 'test-group' });
    await consumer.connect();
    await consumer.subscribe({ topic: 'kafka-node', fromBeginning: true });

    await consumer.run({
        eachMessage: async ({ topic, partition, message }) => {
            console.log('in callback');
            console.log({
                partition,
                offset: message.offset,
                value: message.value.toString(),
            })
        },
    });

    return output;
};

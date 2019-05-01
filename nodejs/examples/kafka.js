'use strict';

const { Kafka } = require('kafkajs');
const config = require("platformsh-config").config();

exports.usageExample = async function() {

    const kafka = new Kafka({
        clientId: 'my-app',
        brokers: [`${config.host}:${config.port}`]
    });

    // Set up the Producer.
    const producer = kafka.producer();
    await producer.connect();
    await producer.send({
        topic: 'test-topic',
        messages: [
            { value: 'Hello KafkaJS user!' },
        ],
    });

    // Set up the Consumer.
    const consumer = kafka.consumer({ groupId: 'test-group' });
    await consumer.connect();
    await consumer.subscribe({ topic: 'test-topic', fromBeginning: true });

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

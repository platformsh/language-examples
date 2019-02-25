const redis = require('redis');
const config = require("platformsh").config();

exports.run = async function() {

    const credentials = config.credentials('redis');

    var client = redis.createClient(credentials.port, credentials.host);

    let key = 'Deploy day';
    let value = 'Friday';

    // Set a value.
    client.set(key, value, redis.print);

    // Read it back.
    let test = await client.get(key);

    let output = `Found value <strong>${test}</strong> for key <strong>${key}</strong>.`;

    return output;
};

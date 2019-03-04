const influxdb = require('influxdb-nodejs');
const config = require("platformsh-config").config();

exports.usageExample = async function() {

    const credentials = config.credentials('influxdb');

    // Connecting to the InfluxDB server. By default it has no user defined, so you will need to create it.
    let connectionString = `http://${credentials.host}:${credentials.port}/`;
    let client = new influxdb(connectionString);

    let password = Math.random().toString(36).slice(-8);
    let response = await client.queryPost(`create user "deploy_user" with password \'${password}\' with all privileges`);

    // Now reconnect with an authenticated connection so that we can access a database.
    connectionString = `http://deploy_user:${password}@${credentials.host}:${credentials.port}/deploys`;
    client = new influxdb(connectionString);

    await client.createDatabase();

    // And remove the user.
    response = await client.queryPost(`delete user "deploy_user"`);

    return output;
};

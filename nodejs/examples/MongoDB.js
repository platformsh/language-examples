const config = require("platformsh").config();

exports.relationship = () => {
    const credentials = config.relationships.mongodb[0];

    return JSON.stringify(credentials, null, 2);
};

exports.run = async function() {
    const credentials = config.relationships.mongodb[0];
    const MongoClient = require('mongodb').MongoClient;
    const connectionString = `'mongodb://${credentials["username"]}:${credentials["password"]}@${credentials["host"]}:${credentials["port"]}`;

    var client = await MongoClient.connect(connectionString, { useNewUrlParser: true });

    let db = client.db(credentials["path"]);

    let collection = db.collection("startrek");

    const documents = [
        {'name': 'James Kirk', 'rank': 'Admiral'},
        {'name': 'Jean-Luc Picard', 'rank': 'Captain'},
        {'name': 'Benjamin Sisko', 'rank': 'Prophet'},
        {'name': 'Katheryn Janeway', 'rank': 'Captain'},
    ];

    await collection.insert(documents, {w: 1});

    let result = await collection.find({rank:"Captain"}).toArray();

    let output = '';

    output += `<table>
<thead>
<tr><th>Name</th><th>Rank</th></tr>
</thead>
<tbody>`;

    result.forEach((key) => {
        output += `<tr><td>${result[key].name}</td><td>${result[key].rank}</td></tr>\n`;
    });

    output += `</tbody>\n</table>\n`;

    return output;
};

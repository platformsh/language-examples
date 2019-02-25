const config = require("platformsh").config();

exports.run = async function() {
    const credentials = config.credentials('mongodb');
    const MongoClient = require('mongodb').MongoClient;
    const connectionString = `mongodb://${credentials["username"]}:${credentials["password"]}@${credentials["host"]}:${credentials["port"]}/${credentials["path"]}`;

    var client = await MongoClient.connect(connectionString);

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

    Object.keys(result).forEach((key) => {
        output += `<tr><td>${result[key].name}</td><td>${result[key].rank}</td></tr>\n`;
    });

    output += `</tbody>\n</table>\n`;

    // Clean up after ourselves.
    collection.remove();

    return output;
};

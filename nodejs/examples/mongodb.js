const mongodb = require('mongodb');
const config = require("platformsh-config").config();

exports.usageExample = async function() {
    // The 'database' relationship is generally the name of primary database of an application.
    // It could be anything, though, as in the case here here where it's called "database".
    const credentials = config.credentials('database');
    const MongoClient = mongodb.MongoClient;

    var client = await MongoClient.connect(config.formattedCredentials('database', 'mongodb'));

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

const config = require("platformsh").config();

exports.relationship = () => {
    const credentials = config.relationships.mongodb[0];

    return JSON.stringify(credentials, null, 2);
};

exports.run = async function() {

    const credentials = config.relationships.mongodb[0];
    let mongoose = require('mongoose');

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

    /*
    // Mongoose connection to MongoDB
    mongoose.connect(`'mongodb://${credentials["username"]}:${credentials['password']}@${credentials['host']}:${credentials['port']}/${credentials['path']}`, function (err) {
        if (err) {
            if (err) console.error(err);
        }
    });
    var thingSchema = new mongoose.Schema({
        title: { type: String }
    });
    var Thing = mongoose.model('Thing', thingSchema);
    var foo = new Thing({
        title: 'Platform.sh'
    });
    await foo.save(function(err, foo) {
        if (err) console.error(err);
    });
    // Thing.find({}, function(err, foo) {
    //     if (err) { console.error(err) } else { resp = JSON.stringify(foo, null, 4) };
    // });
    let things = await Thing.find();

    console.debug(things);
    */
    
    //return "Some output";
};

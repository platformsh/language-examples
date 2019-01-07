const config = require("platformsh").config();

exports.relationship = () => {
    const credentials = config.relationships.mongodb[0];

    return JSON.stringify(credentials, null, 2);
};

exports.run = async function() {

    // Do various mongoDB calls, using await on them.
    // Then construct and return a string of output at the end.

    const credentials = config.relationships.mongodb[0];
    let mongoose = require('mongoose');

    // Mongoose connection to MongoDB
    mongoose.connect(`'mongodb://${db["username"]}:${db['password']}@${db['host']}:${db['port']}/${db['path']}`, function (err) {
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
    foo.save(function(err, foo) {
        if (err) console.error(err);
    });
    Thing.find({}, function(err, foo) {
        if (err) { console.error(err) } else { resp = JSON.stringify(foo, null, 4) };
    });
    
    
    return "Some output";
};

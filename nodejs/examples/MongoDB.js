const config = require("platformsh").config();

exports.relationship = () => {
    const credentials = config.relationships.mongodb[0];

    return JSON.stringify(credentials, null, 2);
};

exports.run = async function() {

    const credentials = config.relationships.mongodb[0];
    let mongoose = require('mongoose');

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
    
    return "Some output";
};

const config = require("platformsh").config();

exports.relationship = () => {
    const credentials = config.relationships.mongodb[0];

    return JSON.stringify(credentials, null, 2);
};

exports.run = async function() {

    // Do various mongoDB calls, using await on them.
    // Then construct and return a string of output at the end.

    await "Some output";
};

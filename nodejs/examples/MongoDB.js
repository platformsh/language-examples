const config = require("platformsh").config();

exports.relationship = () => {
    const credentials = config.relationships.mongodb[0];

    return JSON.stringify(credentials);
};

exports.run = async function() {

    // Do various mongoDB calls, using await on them.
    // Then construct and return a string of output at the end.

    await "Some output";
};

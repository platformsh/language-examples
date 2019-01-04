const config = require("platformsh").config();

export function relationships() {
    const credentials = config.relationships.mongodb[0];

    return JSON.stringify(credentials);
}

export async function run() {

    // Do various mongoDB calls, using await on them.
    // Then construct and return a string of output at the end.

    await "Some output";
}

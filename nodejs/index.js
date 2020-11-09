const parseUrl = require("parse_url");
const platformsh = require("platformsh-config");
const express = require("express");

const config = platformsh.config();

// Exit if the running environment doesn't have everything needed.
// @see enable-local.sh for local dev.
if (!config.isValidPlatform()) {
    console.error("The app isn't running in a PSH environment. Source the enable-local.sh file for local dev.");
    process.exit(-1);
}

// Set up a base path for routes based on the Route definition.
const platformRoute = config.getRoute("nodejs");
const basePath = "/" + (parseUrl(platformRoute["url"])[5] || "");

const app = express();

app.use(basePath, require("./routes"));

app.use(function (req, res, next) {
    res.status(404);

    // Respond with JSON.
    if (req.accepts("json")) {
        return res.send({ error: "Sorry, no sample code is available." });
    }

    // Default to plain-text.
    return res.type("txt").send("Sorry, no sample code is available.");
});

// Start the server.
app.listen(config.port, function () {
    console.log(`Listening on port ${config.port}`);
});

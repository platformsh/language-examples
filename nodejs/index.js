const express = require('express');
const parseUrl = require('parse_url');
const platformsh = require('platformsh-config');

let config = platformsh.config();

if (process.env.NODE_ENV === 'test') {

    config = {
        applicationName: 'test',
        port: 8080,
        getRoute: (id) => {
            return {url: 'http://localhost/nodejs'}
        }
    };
}
else {
}

function sleep(milliseconds) {
    const date = Date.now();
    let currentDate = null;
    do {
        currentDate = Date.now();
    } while (currentDate - date < milliseconds);
}

console.log("Waiting for services to be ready.");
sleep(2000);

var app = express();

// Set up a base path for routes based on the Route definition.
let basePath = '';
if (config.isValidPlatform()) {
    const platformRoute = config.getRoute('nodejs');
    basePath = '/' + (parseUrl(platformRoute['url'])[5] || '');
}

app.use(basePath, require('./routes'));

app.use(function(req, res, next){
    res.status(404);

    // Respond with JSON.
    if (req.accepts('json')) {
        res.send({ error: 'Sorry, no sample code is available.' });
        return;
    }

    // Default to plain-text.
    res.type('txt').send('Sorry, no sample code is available.');
});

// Start the server.
app.listen(config.port, function() {
    console.log(`Listening on port ${config.port}`);
});

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

var app = express();

// Set up a base path for routes based on the Route definition.
const platformRoute = config.getRoute('nodejs');
const basePath = '/' + (parseUrl(platformRoute['url'])[5] || '');
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
    console.log(`Listening on port ${config.port}`)
});

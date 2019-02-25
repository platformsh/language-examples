const express = require('express');
const router = express.Router();
const fs = require('fs');

var data = {};

// @todo Do this for all services.

let services = {
    elasticsearch: 'Elasticsearch',
    memcached: 'MemcacheD',
    mongodb: 'MongoDB',
    redis: 'Redis',
};

Object.keys(services).forEach((key) => {
    data[key] = require(`./examples/${key}.js`);
    data[key].source = escapeHtml(fs.readFileSync(`./examples/${key}.js`, 'utf8'));
    data[key].label = services[key];
});


function escapeHtml(s) {
    return s.replace(/[^0-9A-Za-z ]/g, function(c) {
        return "&#" + c.charCodeAt(0) + ";";
    });
}

// Call all of the run() methods of all services, and store their output once.
async function runData(key) {
    let value = undefined;
    try{
        const method = data[key].run;
        value = await method();
    } catch (err) {
        console.error(err);
    }
    if (value) {
        data[key].output = value;
    }
}

// array of Promise<void>
const promises = Object.keys(data).map(runData);


async function index(req, res) {

    try {
        await Promise.all(promises);
    }
    catch (error) {
        console.error(error);
    }

    res.writeHead(200, {"Content-Type": "text/html"});

    res.write(`<html>
<head>
    <title>Platform.sh Node.js service examples</title>
    <style type="text/css">
        details {
            margin-top: 1em;
            border: 1px solid #aaa;
            border-radius: 4px;
            padding: 0.5em;
            wdith: 90%;
        }

        summary {
            font-weight: bold;
            margin: -.5em -.5em 0;
            padding: .5em;
        }

        details[open] {
            padding: .5em;
        }

        details[open] summary {
            border-bottom: 1px solid #aaa;
            margin-bottom: .5em;
        }

        table, table td, table th {
            border: 1px solid black;
        }
    </style>
</head>
<body>
<h1>Service examples for Node.js</h1>
`);

    Object.keys(data).forEach ((key) => {
        let name = key;
        res.write(`<details>
      <summary>${data[key].label} Sample Code</summary>
      <section>
      <h3>Source</h3>
      <pre>${data[key].source}</pre>
      </section>
      <section>
      <h3>Output</h3>
      ${data[key].output}
      </section>
      </details>
      `);
    });

    res.end(`</body></html>`);
}


router.get('/', index);

router.get('/:service', (req, res) => {

    let options = {
        root: __dirname + '/examples/',
        dotfiles: 'deny',
        headers: {
            'Content-Type': 'text/plain',
        }
    };

    res.sendFile(`${req.params.service}.js`, options);
});

router.get('/:service/output', async (req, res) => {
    try {
        await Promise.all(promises);
    }
    catch (error) {
        console.error(error);
    }

    res.end(data[req.params.service].output);
});

module.exports = router;

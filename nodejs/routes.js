const express = require('express');
const router = express.Router();
const fs = require('fs');

var data = {};

let services = {
    elasticsearch: 'Elasticsearch',
    influxdb: 'InfluxDB',
    memcached: 'Memcached',
    mongodb: 'MongoDB',
    mysql: 'MySQL',
//    oraclemysql: 'Oracle MySQL',
    opensearch: 'OpenSearch',
    postgresql: 'PostgreSQL',
    redis: 'Redis',
    solr: 'Solr',
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
    try{
        const method = data[key].usageExample;
        const value = await method();
        if (value) {
            data[key].output = value;
        }
        return Promise.resolve();
    } catch (err) {
        console.error(err);
    }
}

async function index(req, res) {
    try {
        await Promise.all(Object.keys(data).map(runData));
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

    Object.values(data).forEach (({label, source, output}) => {
        res.write(`<details>
      <summary>${label} Sample Code</summary>
      <section>
      <h3>Source</h3>
      <pre>${source}</pre>
      </section>
      <section>
      <h3>Output</h3>
      ${output}
      </section>
      </details>
      `);
    });

    res.end(`</body></html>`);
}


router.get('/', index);

router.get('/:service', (req, res) => {

    const file = __dirname + '/examples/' + req.params.service + '.js';

    let options = {
        dotfiles: 'deny',
        headers: {
            'Content-Type': 'text/plain',
        }
    };

    fs.access(file, fs.F_OK, (err) => {
        if (err) {
            res.end('Sorry, no sample code is available.')
        }
        res.sendFile(file, options);
    });
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
